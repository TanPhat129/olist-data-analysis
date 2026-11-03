"""Export customer-experience tables from the public Olist CSVs."""
import argparse
from pathlib import Path

import pandas as pd

REGIONS = {
    state: region
    for region, states in {
        "North": "AC AP AM PA RO RR TO",
        "Northeast": "AL BA CE MA PB PE PI RN SE",
        "Central-West": "DF GO MT MS",
        "Southeast": "ES MG RJ SP",
        "South": "PR RS SC",
    }.items()
    for state in states.split()
}


def summarize(frame, by):
    result = frame.groupby(by, dropna=False, observed=True).agg(
        orders=("order_id", "size"),
        reviewed_orders=("negative_review", "count"),
        negative_orders=("negative_review", "sum"),
        avg_review_score=("review_score", "mean"),
        measurable_deliveries=("late_delivery", "count"),
        late_orders=("late_delivery", "sum"),
        item_value_brl=("item_value_brl", "sum"),
    ).reset_index()
    result["negative_review_rate"] = result["negative_orders"].div(
        result["reviewed_orders"].where(result["reviewed_orders"].gt(0))
    )
    result["late_delivery_rate"] = result["late_orders"].div(
        result["measurable_deliveries"].where(result["measurable_deliveries"].gt(0))
    )
    return result


def build_reports(raw_dir):
    def read(name, columns):
        return pd.read_csv(raw_dir / f"olist_{name}_dataset.csv", usecols=columns)

    dates = ["order_purchase_timestamp", "order_delivered_customer_date",
             "order_estimated_delivery_date"]
    orders = read("orders", ["order_id", "customer_id", "order_status", *dates])
    customers = read("customers", ["customer_id", "customer_unique_id", "customer_state"])
    reviews = read("order_reviews", ["order_id", "review_id", "review_score",
                                    "review_answer_timestamp"])
    items = read("order_items", ["order_id", "seller_id", "product_id", "price"])
    products = read("products", ["product_id", "product_category_name"])
    translations = pd.read_csv(raw_dir / "product_category_name_translation.csv")

    reviews = reviews.loc[reviews["review_score"].isin(range(1, 6))].copy()
    reviews["review_answer_timestamp"] = pd.to_datetime(
        reviews["review_answer_timestamp"], errors="coerce"
    )
    reviews = reviews.sort_values(["review_answer_timestamp", "review_id"], na_position="first")
    reviews = reviews.drop_duplicates("order_id", keep="last")
    order_value = items.groupby("order_id")["price"].sum().rename("item_value_brl")
    orders = orders.merge(customers, on="customer_id", how="left", validate="many_to_one")
    orders = orders.merge(reviews[["order_id", "review_score"]], on="order_id",
                          how="left", validate="one_to_one")
    orders = orders.join(order_value, on="order_id")
    for column in dates:
        orders[column] = pd.to_datetime(orders[column], errors="coerce")
    purchase, delivered, estimate = (orders[column] for column in dates)
    orders["order_month"] = purchase.dt.strftime("%Y-%m")
    orders["customer_region"] = orders["customer_state"].map(REGIONS)
    orders["negative_review"] = orders["review_score"].le(2).where(
        orders["review_score"].notna()
    ).astype("Float64")
    completed = orders["order_status"].eq("delivered")
    duration = (delivered - purchase).dt.total_seconds().div(86400)
    orders["delivery_days"] = duration.where(completed & duration.ge(0))
    # Promised dates are calendar days, so delivery later on the same day is on time.
    orders["late_delivery"] = delivered.dt.normalize().gt(estimate.dt.normalize()).where(
        orders["delivery_days"].notna() & estimate.notna()
    ).astype("Float64")
    orders["delivery_outcome"] = orders["order_status"].mask(completed, "unknown timing")
    orders.loc[orders["late_delivery"].eq(0).fillna(False), "delivery_outcome"] = "on time"
    orders.loc[orders["late_delivery"].eq(1).fillna(False), "delivery_outcome"] = "late"
    orders["delivery_band"] = pd.cut(
        orders["delivery_days"], [-1, 7, 14, 21, 25, 35, float("inf")],
        labels=["0–7", ">7–14", ">14–21", ">21–25", ">25–35", ">35"],
    )

    buyers = orders.loc[completed].groupby("customer_unique_id").agg(
        delivered_orders=("order_id", "size"),
        spend_brl=("item_value_brl", "sum"),
    )
    buyers["customer_segment"] = "Standard one-time buyer"
    top_spend = buyers["spend_brl"].quantile(0.75)
    buyers.loc[buyers["spend_brl"].ge(top_spend), "customer_segment"] = "High-value one-time buyer"
    buyers.loc[buyers["delivered_orders"].ge(2), "customer_segment"] = "Repeat buyer"
    orders = orders.join(buyers["customer_segment"], on="customer_unique_id")
    orders["customer_segment"] = orders["customer_segment"].fillna("No delivered order")

    catalog = products.merge(translations, on="product_category_name", how="left",
                             validate="many_to_one")
    catalog["category"] = catalog["product_category_name_english"].fillna(
        catalog["product_category_name"]
    )
    items = items.merge(catalog[["product_id", "category"]], on="product_id",
                        how="left", validate="many_to_one")
    reports = {
        "order_experience": orders.drop(columns=["customer_id", "customer_unique_id"]),
        "overview_monthly": summarize(orders, "order_month"),
        "customer_segments": summarize(orders, "customer_segment").merge(
            buyers.groupby("customer_segment").size().rename("customers"),
            on="customer_segment", how="left",
        ),
        "review_by_delivery_outcome": summarize(orders, "delivery_outcome"),
        "delivery_bands": summarize(orders.loc[orders["delivery_band"].notna()], "delivery_band"),
        "state_performance": summarize(orders, ["customer_region", "customer_state"]),
    }
    order_metrics = orders.drop(columns="item_value_brl")
    for key, label, minimum in [("seller_id", "seller", 50), ("category", "category", 100)]:
        # Review belongs to the order, and can appear once for each associated entity.
        pairs = items.groupby(["order_id", key], dropna=False)["price"].sum().reset_index()
        pairs = pairs.rename(columns={"price": "item_value_brl"}).merge(
            order_metrics, on="order_id", validate="many_to_one"
        )
        reports[f"{label}_order_experience"] = pairs[
            ["order_id", key, "item_value_brl"]
        ]
        stats = summarize(pairs, key)
        reports[f"{label}_quality"] = stats.loc[stats["reviewed_orders"].ge(minimum)].sort_values(
            ["negative_review_rate", "reviewed_orders"], ascending=False
        )
    return reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed/experience"))
    args = parser.parse_args()
    reports = build_reports(args.raw_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, report in reports.items():
        report.to_csv(args.output_dir / f"{name}.csv", index=False, encoding="utf-8-sig")
    print(f"Exported {len(reports)} tables to {args.output_dir}")


if __name__ == "__main__":
    main()
