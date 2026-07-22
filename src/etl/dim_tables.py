import pandas as pd


def build_dim_customer(customers: pd.DataFrame) -> pd.DataFrame:
    """Create a cleaned customer dimension from the raw customer file."""
    df = customers.copy()
    df = df.drop_duplicates(subset=["customer_unique_id"]).copy()
    df = df.rename(columns={"customer_unique_id": "customer_unique_id"})
    return df[["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"]]


def build_dim_product(products: pd.DataFrame, translation: pd.DataFrame) -> pd.DataFrame:
    """Create a product dimension with English category names."""
    df = products.merge(translation, on="product_category_name", how="left")
    df = df.drop_duplicates(subset=["product_id"]).copy()
    df["product_category_name_english"] = df["product_category_name_english"].fillna(df["product_category_name"])
    return df[
        [
            "product_id",
            "product_category_name",
            "product_category_name_english",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ]
    ]


def build_dim_seller(sellers: pd.DataFrame) -> pd.DataFrame:
    """Create a cleaned seller dimension."""
    df = sellers.copy()
    df = df.drop_duplicates(subset=["seller_id"]).copy()
    return df[["seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"]]


def build_dim_date(orders: pd.DataFrame, date_col: str = "order_purchase_timestamp") -> pd.DataFrame:
    """Create a lightweight date dimension from purchase timestamps."""
    dates = pd.to_datetime(orders[date_col], errors="coerce").dropna().dt.normalize()
    df = pd.DataFrame({"date": dates.unique()})
    df["date_key"] = df["date"].dt.strftime("%Y%m%d").astype(int)
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    return df.sort_values("date").reset_index(drop=True)
