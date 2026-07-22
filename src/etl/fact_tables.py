import pandas as pd


def _ensure_column(df: pd.DataFrame, column: str, default_value=None) -> pd.DataFrame:
    if column not in df.columns:
        df[column] = default_value
    return df


def build_fact_sales(order_items: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    """Build the sales fact table from orders and order items."""
    df = order_items.copy()
    df = _ensure_column(df, "order_item_id", 1)
    df = _ensure_column(df, "price", 0.0)
    df = _ensure_column(df, "freight_value", 0.0)

    if "order_id" in df.columns and "order_id" in orders.columns:
        df = df.merge(orders[["order_id", "customer_id", "order_purchase_timestamp"]], on="order_id", how="left")
    else:
        df["customer_id"] = pd.NA
        df["order_purchase_timestamp"] = pd.NaT

    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)
    df["freight_value"] = pd.to_numeric(df["freight_value"], errors="coerce").fillna(0.0)
    df["total_value"] = df["price"] + df["freight_value"]
    df["order_purchase_date"] = pd.to_datetime(df["order_purchase_timestamp"], errors="coerce").dt.normalize()

    return df[
        [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "customer_id",
            "order_purchase_date",
            "price",
            "freight_value",
            "total_value",
        ]
    ]


def build_fact_payments(payments: pd.DataFrame) -> pd.DataFrame:
    """Create a payment fact table with one row per payment event."""
    df = payments.copy()
    df = _ensure_column(df, "payment_sequential", 1)
    df = _ensure_column(df, "payment_installments", 1)
    df["payment_value"] = pd.to_numeric(df["payment_value"], errors="coerce")
    return df[["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"]]


def build_fact_reviews(reviews: pd.DataFrame) -> pd.DataFrame:
    """Create a review fact table with one row per review."""
    df = reviews.copy()
    df = _ensure_column(df, "review_id", range(len(df)))
    df["review_creation_date"] = pd.to_datetime(df["review_creation_date"], errors="coerce")
    return df[["review_id", "order_id", "review_score", "review_creation_date"]]
