"""Load generated CSV files into a local MySQL database."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


TABLE_ORDER = [
    "customers",
    "products",
    "merchants",
    "transactions",
    "customer_products",
    "monthly_customer_summary",
]


def build_engine(user: str, password: str, host: str, port: int, database: str):
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url, pool_pre_ping=True)


def load(engine, data_dir: str, chunksize: int = 10_000):
    path = Path(data_dir)
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        for table in TABLE_ORDER:
            csv_path = path / f"{table}.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"Missing generated file: {csv_path}")
            # Replace dimensions/derived tables on each dataset refresh.
            # Transactions are also replaced so the database always matches
            # the current synthetic dataset exactly.
            frame = pd.read_csv(csv_path)
            if table == "transactions":
                frame["transaction_timestamp"] = pd.to_datetime(frame["transaction_timestamp"])
            elif table == "customer_products":
                frame["purchase_date"] = pd.to_datetime(frame["purchase_date"]).dt.date
            conn.execute(text(f"TRUNCATE TABLE `{table}`"))
            frame.to_sql(table, conn, if_exists="append", index=False, chunksize=chunksize, method="multi")
            print(f"loaded {table}: {len(frame):,} rows")
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def main():
    parser = argparse.ArgumentParser(description="Load synthetic banking CSVs into MySQL")
    parser.add_argument("--user", default="root")
    parser.add_argument("--password", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--database", default="banking_recommendation")
    parser.add_argument("--data-dir", default="data/generated")
    parser.add_argument("--chunksize", type=int, default=10_000)
    args = parser.parse_args()

    engine = build_engine(args.user, args.password, args.host, args.port, args.database)
    load(engine, args.data_dir, args.chunksize)
    print("MySQL load completed successfully.")


if __name__ == "__main__":
    main()
