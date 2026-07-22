import pandas as pd

from src.etl.dim_tables import build_dim_customer, build_dim_product, build_dim_seller, build_dim_date
from src.etl.fact_tables import build_fact_sales, build_fact_payments, build_fact_reviews


def test_build_dim_customer_returns_expected_columns_and_keys():
    customers = pd.DataFrame(
        [
            {
                "customer_id": "c1",
                "customer_unique_id": "u1",
                "customer_zip_code_prefix": 1356,
                "customer_city": "Sao Paulo",
                "customer_state": "SP",
            }
        ]
    )

    result = build_dim_customer(customers)

    assert {"customer_unique_id", "customer_city", "customer_state"}.issubset(result.columns)
    assert result.iloc[0]["customer_unique_id"] == "u1"


def test_build_fact_sales_joins_order_items_and_orders():
    order_items = pd.DataFrame(
        [{"order_id": "o1", "product_id": "p1", "seller_id": "s1", "price": 100.0, "freight_value": 10.0}]
    )
    orders = pd.DataFrame(
        [{"order_id": "o1", "customer_id": "c1", "order_purchase_timestamp": "2018-01-01 00:00:00"}]
    )

    result = build_fact_sales(order_items, orders)

    assert result.iloc[0]["order_id"] == "o1"
    assert result.iloc[0]["total_value"] == 110.0
    assert result.iloc[0]["customer_id"] == "c1"


def test_build_fact_payments_and_reviews_are_created():
    payments = pd.DataFrame([{"order_id": "o1", "payment_type": "credit_card", "payment_value": 110.0}])
    reviews = pd.DataFrame([{"order_id": "o1", "review_score": 5, "review_creation_date": "2018-01-02"}])

    payment_result = build_fact_payments(payments)
    review_result = build_fact_reviews(reviews)

    assert payment_result.iloc[0]["payment_type"] == "credit_card"
    assert review_result.iloc[0]["review_score"] == 5
