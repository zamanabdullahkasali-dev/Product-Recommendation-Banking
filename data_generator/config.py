"""Configuration for the synthetic banking data generator."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GeneratorConfig:
    seed: int = 42
    n_customers: int = 10_000
    months: int = 12
    transactions_per_customer_per_month: int = 8
    output_dir: str = "data/generated"

    # Change these when you want a larger training dataset.
    # Example: n_customers=100_000, months=24.
    min_age: int = 18
    max_age: int = 75

    @property
    def start_date(self):
        from datetime import date

        return date(2025, 1, 1)


PRODUCTS = [
    ("P001", "Basic Credit Card", "credit_card", 0.0, 18.0, "low"),
    ("P002", "Cashback Credit Card", "credit_card", 999.0, 18.0, "low"),
    ("P003", "Travel Rewards Credit Card", "credit_card", 1999.0, 18.0, "medium"),
    ("P004", "Premium Credit Card", "credit_card", 4999.0, 16.0, "medium"),
    ("P005", "Personal Loan", "loan", 0.0, 12.5, "medium"),
    ("P006", "Home Loan", "loan", 0.0, 8.5, "low"),
    ("P007", "Auto Loan", "loan", 0.0, 9.5, "low"),
    ("P008", "Gold Loan", "loan", 0.0, 11.0, "medium"),
    ("P009", "Fixed Deposit", "deposit", 0.0, 7.0, "low"),
    ("P010", "Recurring Deposit", "deposit", 0.0, 6.5, "low"),
    ("P011", "Equity Mutual Fund", "investment", 0.0, 0.0, "high"),
    ("P012", "Balanced Mutual Fund", "investment", 0.0, 0.0, "medium"),
    ("P013", "SIP", "investment", 0.0, 0.0, "medium"),
    ("P014", "Life Insurance", "insurance", 0.0, 0.0, "low"),
    ("P015", "Health Insurance", "insurance", 0.0, 0.0, "low"),
    ("P016", "Travel Insurance", "insurance", 0.0, 0.0, "low"),
]

MERCHANT_CATEGORIES = [
    ("salary", 0.03),
    ("groceries", 0.14),
    ("shopping", 0.12),
    ("food_delivery", 0.08),
    ("restaurants", 0.07),
    ("fuel", 0.07),
    ("travel", 0.04),
    ("utilities", 0.09),
    ("rent", 0.05),
    ("healthcare", 0.04),
    ("entertainment", 0.06),
    ("education", 0.03),
    ("electronics", 0.04),
    ("insurance", 0.02),
    ("investment", 0.02),
]
