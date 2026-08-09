"""Reusable read-only helpers for downstream ML/analytics code."""

from __future__ import annotations

import pandas as pd
from sqlalchemy import create_engine, text


def get_engine(user: str, password: str, host: str = "127.0.0.1", port: int = 3306, database: str = "banking_recommendation"):
    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
        pool_pre_ping=True,
    )


def read_customer_features(engine, limit: int | None = None) -> pd.DataFrame:
    sql = """
        SELECT
            c.customer_id,
            c.age,
            c.gender,
            c.occupation,
            c.monthly_income,
            c.credit_score,
            c.risk_profile,
            c.customer_segment,
            c.average_monthly_balance,
            c.relationship_tenure_months,
            c.digital_banking_score,
            COALESCE(SUM(t.transaction_amount), 0) AS total_spend,
            COUNT(t.transaction_id) AS transaction_count,
            COUNT(DISTINCT cp.product_id) AS existing_product_count
        FROM customers c
        LEFT JOIN transactions t ON t.customer_id = c.customer_id
        LEFT JOIN customer_products cp ON cp.customer_id = c.customer_id
        GROUP BY c.customer_id
        ORDER BY c.customer_id
    """
    if limit:
        sql += " LIMIT :limit"
        return pd.read_sql(text(sql), engine, params={"limit": limit})
    return pd.read_sql(text(sql), engine)


def read_interactions(engine) -> pd.DataFrame:
    """Return positive customer-product interactions for recommender training."""
    return pd.read_sql(
        text("""
            SELECT customer_id, product_id, purchase_date, status
            FROM customer_products
            WHERE status = 'active'
        """),
        engine,
    )


def read_transaction_history(engine, customer_id: int | None = None) -> pd.DataFrame:
    sql = """
        SELECT customer_id, transaction_timestamp, merchant_category,
               transaction_amount, payment_method
        FROM transactions
    """
    params = {}
    if customer_id is not None:
        sql += " WHERE customer_id = :customer_id"
        params["customer_id"] = customer_id
    sql += " ORDER BY transaction_timestamp"
    return pd.read_sql(text(sql), engine, params=params)
