from pathlib import Path
import pandas as pd

from src.etl.dim_tables import build_dim_customer, build_dim_date, build_dim_product, build_dim_seller
from src.etl.fact_tables import build_fact_payments, build_fact_reviews, build_fact_sales


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def run_pipeline() -> None:
    customers = pd.read_csv(RAW_DIR / "olist_customers_dataset.csv")
    products = pd.read_csv(RAW_DIR / "olist_products_dataset.csv")
    sellers = pd.read_csv(RAW_DIR / "olist_sellers_dataset.csv")
    orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
    order_items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
    payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")
    reviews = pd.read_csv(RAW_DIR / "olist_order_reviews_dataset.csv")
    translation = pd.read_csv(RAW_DIR / "product_category_name_translation.csv")

    dim_customer = build_dim_customer(customers)
    dim_product = build_dim_product(products, translation)
    dim_seller = build_dim_seller(sellers)
    dim_date = build_dim_date(orders)

    fact_sales = build_fact_sales(order_items, orders)
    fact_payments = build_fact_payments(payments)
    fact_reviews = build_fact_reviews(reviews)

    dim_customer.to_parquet(PROCESSED_DIR / "dim_customer.parquet", index=False)
    dim_product.to_parquet(PROCESSED_DIR / "dim_product.parquet", index=False)
    dim_seller.to_parquet(PROCESSED_DIR / "dim_seller.parquet", index=False)
    dim_date.to_parquet(PROCESSED_DIR / "dim_date.parquet", index=False)

    fact_sales.to_parquet(PROCESSED_DIR / "fact_sales.parquet", index=False)
    fact_payments.to_parquet(PROCESSED_DIR / "fact_payments.parquet", index=False)
    fact_reviews.to_parquet(PROCESSED_DIR / "fact_reviews.parquet", index=False)

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
