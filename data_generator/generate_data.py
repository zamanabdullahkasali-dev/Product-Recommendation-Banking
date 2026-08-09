"""Generate realistic, reproducible synthetic banking data.

The generator deliberately uses relationships between customer attributes,
financial behavior, product eligibility, and product adoption. It does not
use real customer information.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from config import GeneratorConfig, MERCHANT_CATEGORIES, PRODUCTS


CITIES = [
    ("Chennai", "Tamil Nadu"),
    ("Bengaluru", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Mumbai", "Maharashtra"),
    ("Pune", "Maharashtra"),
    ("Delhi", "Delhi"),
    ("Kolkata", "West Bengal"),
    ("Ahmedabad", "Gujarat"),
    ("Kochi", "Kerala"),
    ("Coimbatore", "Tamil Nadu"),
]

OCCUPATIONS = [
    "Software Engineer", "Government Employee", "Business Owner", "Doctor",
    "Teacher", "Accountant", "Sales Professional", "Consultant",
    "Freelancer", "Student", "Retired", "Lawyer",
]

MERCHANTS = {
    "groceries": ["Reliance Smart", "DMart", "Local Supermarket"],
    "shopping": ["Amazon", "Flipkart", "Myntra", "Retail Store"],
    "food_delivery": ["Swiggy", "Zomato"],
    "restaurants": ["Restaurant", "Cafe", "Fast Food"],
    "fuel": ["IndianOil", "HPCL", "BPCL"],
    "travel": ["Airline", "IRCTC", "Hotel", "Travel Portal"],
    "utilities": ["Electricity Board", "Water Board", "Internet Provider"],
    "rent": ["Property Rent"],
    "healthcare": ["Hospital", "Pharmacy", "Diagnostic Centre"],
    "entertainment": ["Netflix", "Spotify", "Cinema", "Gaming"],
    "education": ["University", "Training Institute", "Online Learning"],
    "electronics": ["Croma", "Reliance Digital", "Electronics Store"],
    "insurance": ["Insurance Premium"],
    "investment": ["Mutual Fund SIP", "Brokerage"],
}


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


def weighted_choice(rng, values, probabilities, size):
    probabilities = np.asarray(probabilities, dtype=float)
    probabilities /= probabilities.sum()
    return rng.choice(values, size=size, p=probabilities)


def make_customers(cfg: GeneratorConfig, rng: np.random.Generator) -> pd.DataFrame:
    n = cfg.n_customers
    customer_id = np.arange(1, n + 1)
    age = rng.integers(cfg.min_age, cfg.max_age + 1, n)
    occupation = rng.choice(OCCUPATIONS, n)
    city_idx = rng.integers(0, len(CITIES), n)
    city = np.array([CITIES[i][0] for i in city_idx])
    state = np.array([CITIES[i][1] for i in city_idx])

    # Income is correlated with age, occupation and experience rather than
    # sampled independently.
    occupation_income = {
        "Student": 18000, "Retired": 35000, "Teacher": 55000,
        "Government Employee": 75000, "Software Engineer": 110000,
        "Doctor": 180000, "Business Owner": 160000, "Lawyer": 120000,
        "Consultant": 130000, "Accountant": 70000,
        "Sales Professional": 65000, "Freelancer": 70000,
    }
    base_income = np.array([occupation_income[o] for o in occupation], dtype=float)
    income = base_income * rng.lognormal(0, 0.28, n)
    income *= np.where(age < 25, 0.75, np.where(age > 55, 0.9, 1.0))
    income = np.maximum(income, 12000).round(2)

    credit_score = np.clip(
        660 + 0.00018 * income + 0.8 * (age - 35) + rng.normal(0, 45, n),
        300, 850,
    ).round().astype(int)
    monthly_balance = np.maximum(income * rng.lognormal(-1.2, 0.45, n), 1000).round(2)
    employment = np.where(
        np.isin(occupation, ["Student", "Retired"]), "Not employed", "Employed"
    )
    risk = np.select(
        [credit_score >= 760, credit_score >= 680],
        ["low", "medium"],
        default="high",
    )
    segment = np.select(
        [income >= 200000, income >= 100000, income >= 50000],
        ["high_net_worth", "affluent", "mass_affluent"],
        default="mass_market",
    )

    return pd.DataFrame({
        "customer_id": customer_id,
        "age": age,
        "gender": rng.choice(["M", "F", "Other"], n, p=[0.48, 0.50, 0.02]),
        "marital_status": np.where(
            age < 25, "Single", rng.choice(["Single", "Married"], n, p=[0.25, 0.75])
        ),
        "education": rng.choice(["High School", "Graduate", "Postgraduate"], n, p=[0.15, 0.55, 0.30]),
        "occupation": occupation,
        "employment_type": employment,
        "monthly_income": income,
        "city": city,
        "state": state,
        "credit_score": credit_score,
        "risk_profile": risk,
        "customer_segment": segment,
        "average_monthly_balance": monthly_balance,
        "relationship_tenure_months": rng.integers(3, 181, n),
        "digital_banking_score": np.clip(
            45 + 0.55 * (age < 40) * 50 + rng.normal(0, 15, n), 0, 100
        ).round(2),
    })


def make_products() -> pd.DataFrame:
    return pd.DataFrame(PRODUCTS, columns=[
        "product_id", "product_name", "category", "annual_fee", "interest_rate", "risk_level"
    ])


def make_merchants() -> pd.DataFrame:
    rows = []
    merchant_id = 1
    for category, _ in MERCHANT_CATEGORIES:
        for name in MERCHANTS.get(category, [category.title()]):
            rows.append((f"M{merchant_id:04d}", name, category))
            merchant_id += 1
    return pd.DataFrame(rows, columns=["merchant_id", "merchant_name", "category"])


def make_transactions(customers: pd.DataFrame, merchants: pd.DataFrame, cfg: GeneratorConfig, rng: np.random.Generator) -> pd.DataFrame:
    n = len(customers)
    rows = []
    category_names = [x[0] for x in MERCHANT_CATEGORIES]
    category_probs = [x[1] for x in MERCHANT_CATEGORIES]
    merchant_by_category = {
        c: merchants.loc[merchants.category == c, "merchant_id"].to_numpy() for c in category_names
    }

    for month in range(cfg.months):
        month_start = pd.Timestamp(cfg.start_date) + pd.DateOffset(months=month)
        customer_ids = customers.customer_id.to_numpy()
        repeats = cfg.transactions_per_customer_per_month
        ids = np.repeat(customer_ids, repeats)
        idx = np.repeat(np.arange(n), repeats)
        categories = weighted_choice(rng, category_names, category_probs, len(ids))
        income = customers.monthly_income.to_numpy()[idx]

        # Log-normal spend with category multipliers and income sensitivity.
        multipliers = {
            "salary": 0.55, "groceries": 0.025, "shopping": 0.045,
            "food_delivery": 0.018, "restaurants": 0.022, "fuel": 0.025,
            "travel": 0.06, "utilities": 0.04, "rent": 0.18,
            "healthcare": 0.025, "entertainment": 0.015, "education": 0.025,
            "electronics": 0.05, "insurance": 0.035, "investment": 0.08,
        }
        amounts = np.empty(len(ids))
        for category, multiplier in multipliers.items():
            mask = categories == category
            if mask.any():
                amounts[mask] = income[mask] * multiplier * rng.lognormal(0, 0.45, mask.sum())
        amounts = np.maximum(amounts, 20).round(2)
        salary_mask = categories == "salary"
        amounts[salary_mask] = (income[salary_mask] * rng.normal(1.0, 0.04, salary_mask.sum())).round(2)

        merchant_ids = np.array([
            rng.choice(merchant_by_category[c]) for c in categories
        ])
        days = rng.integers(0, 28, len(ids))
        hours = rng.integers(7, 23, len(ids))
        timestamps = month_start + pd.to_timedelta(days, unit="D") + pd.to_timedelta(hours, unit="h")
        payment = rng.choice(["UPI", "Debit Card", "Credit Card", "NEFT", "IMPS"], len(ids), p=[0.40, 0.20, 0.22, 0.08, 0.10])

        rows.append(pd.DataFrame({
            "transaction_id": [f"T{month:02d}{i:08d}" for i in range(len(ids))],
            "customer_id": ids,
            "merchant_id": merchant_ids,
            "merchant_category": categories,
            "transaction_amount": amounts,
            "transaction_timestamp": timestamps,
            "payment_method": payment,
        }))

    return pd.concat(rows, ignore_index=True)


def make_customer_products(customers: pd.DataFrame, products: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    product_ids = products.product_id.to_numpy()
    for customer in customers.itertuples(index=False):
        income = customer.monthly_income
        score = customer.credit_score
        age = customer.age
        # Base adoption probability. Features then modify product-specific demand.
        for pid in product_ids:
            p = 0.015
            if pid in {"P001", "P002"}: p += 0.12
            if pid == "P003": p += 0.10 * (customer.digital_banking_score / 100)
            if pid == "P004": p += 0.12 * sigmoid((income - 150000) / 50000)
            if pid == "P005": p += 0.12 * sigmoid((income - 60000) / 30000) * (score >= 650)
            if pid == "P006": p += 0.08 * (age >= 28) * sigmoid((income - 80000) / 40000)
            if pid == "P007": p += 0.07 * (age >= 25)
            if pid == "P008": p += 0.05 * (score < 700)
            if pid in {"P009", "P010"}: p += 0.12 * sigmoid((customer.average_monthly_balance - 50000) / 30000)
            if pid in {"P011", "P012", "P013"}: p += 0.08 * sigmoid((income - 70000) / 35000)
            if pid == "P014": p += 0.07 * (age >= 30)
            if pid == "P015": p += 0.07 * (age >= 28)
            if pid == "P016": p += 0.12 * (customer.digital_banking_score / 100)
            if rng.random() < min(p, 0.85):
                rows.append((customer.customer_id, pid, pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365), unit="D"), "active"))
    return pd.DataFrame(rows, columns=["customer_id", "product_id", "purchase_date", "status"])


def make_monthly_summary(customers: pd.DataFrame, transactions: pd.DataFrame) -> pd.DataFrame:
    tx = transactions.copy()
    tx["month"] = tx.transaction_timestamp.dt.to_period("M").astype(str)
    summary = tx.groupby(["customer_id", "month"]).agg(
        transaction_count=("transaction_id", "count"),
        total_spend=("transaction_amount", "sum"),
        average_transaction_amount=("transaction_amount", "mean"),
        shopping_spend=("transaction_amount", lambda x: x[tx.loc[x.index, "merchant_category"].eq("shopping")].sum()),
        travel_spend=("transaction_amount", lambda x: x[tx.loc[x.index, "merchant_category"].eq("travel")].sum()),
        investment_spend=("transaction_amount", lambda x: x[tx.loc[x.index, "merchant_category"].eq("investment")].sum()),
    ).reset_index()
    summary = summary.merge(customers[["customer_id", "monthly_income"]], on="customer_id", how="left")
    summary["savings_rate_proxy"] = np.clip(
        (summary.monthly_income - summary.total_spend) / summary.monthly_income, -1, 1
    )
    summary["debt_to_income_proxy"] = 0.0
    return summary


def generate(cfg: GeneratorConfig) -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(cfg.seed)
    customers = make_customers(cfg, rng)
    products = make_products()
    merchants = make_merchants()
    transactions = make_transactions(customers, merchants, cfg, rng)
    customer_products = make_customer_products(customers, products, rng)
    monthly_summary = make_monthly_summary(customers, transactions)
    return {
        "customers": customers,
        "products": products,
        "merchants": merchants,
        "transactions": transactions,
        "customer_products": customer_products,
        "monthly_customer_summary": monthly_summary,
    }


def save_tables(tables: dict[str, pd.DataFrame], output_dir: str) -> None:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    for name, frame in tables.items():
        frame.to_csv(path / f"{name}.csv", index=False)
        print(f"saved {name}: {len(frame):,} rows")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic banking data")
    parser.add_argument("--customers", type=int, default=10_000)
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--tx-per-customer-month", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", default="data/generated")
    args = parser.parse_args()
    cfg = GeneratorConfig(
        seed=args.seed,
        n_customers=args.customers,
        months=args.months,
        transactions_per_customer_per_month=args.tx_per_customer_month,
        output_dir=args.output_dir,
    )
    save_tables(generate(cfg), cfg.output_dir)


if __name__ == "__main__":
    main()
