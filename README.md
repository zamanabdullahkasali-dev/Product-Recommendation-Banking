# Financial Product Recommendation System

A deep learning-based recommendation system that predicts and recommends suitable financial products to customers based on their profiles, transaction behavior, financial activity, and historical product interactions.

## Project Overview

This project uses **Neural Collaborative Filtering (NCF)** to learn customer and product representations and generate personalized financial product recommendations.

The project uses synthetic banking data designed to simulate realistic customer behavior while avoiding the use of real financial customer information.

## Data Pipeline

The repository includes a reproducible synthetic banking data generator and a local MySQL pipeline.

```text
Synthetic Data Generator
        │
        ├── Customers
        ├── Transactions
        ├── Merchants
        ├── Products
        ├── Customer Products
        └── Monthly Summaries
                │
                ▼
          Local MySQL
                │
                ▼
      ML / Recommendation Pipeline
```

### Generate data

```bash
pip install -r requirements.txt
python data_generator/generate_data.py --customers 10000 --months 12 --tx-per-customer-month 8
```

### Create the MySQL database

Run `database/schema.sql` in your local MySQL instance.

Then load the generated CSV files:

```bash
python database/load_mysql.py \
  --user root \
  --password YOUR_MYSQL_PASSWORD \
  --database banking_recommendation
```

The default generator creates 10,000 customers and 12 months of activity. Increase `--customers`, `--months`, and `--tx-per-customer-month` when you need a larger training dataset.

### Read data from MySQL

Downstream notebooks and ML code can reuse the query helpers in `database/query_mysql.py` instead of loading raw CSV files directly.

## Objectives

* Generate realistic synthetic banking data.
* Analyze customer financial behavior.
* Build customer and product features.
* Implement traditional recommendation baselines.
* Build a Neural Collaborative Filtering model.
* Generate personalized Top-K financial product recommendations.
* Evaluate recommendation performance using ranking metrics.

## Financial Products

* Credit Cards
* Premium Credit Cards
* Personal Loans
* Home Loans
* Auto Loans
* Fixed Deposits
* Mutual Funds
* SIPs
* Health Insurance
* Life Insurance
* Travel Insurance

## Architecture

```text
Customer Data
      │
      ▼
Feature Engineering
      │
      ▼
Customer-Product Interactions
      │
      ▼
User Embedding ───┐
                  ├──► Neural Network ───► Prediction
Product Embedding ┘
      │
      ▼
Top-K Recommendations
```

## Models

### Baseline Models

* Popularity-Based Recommendation
* Collaborative Filtering
* Matrix Factorization

### Deep Learning

* Neural Collaborative Filtering (NCF)

### Planned

* Wide & Deep
* DeepFM
* Two-Tower Recommendation Model
* Sequential Recommendation using Transformers

## Evaluation

* Precision@K
* Recall@K
* Hit Rate@K
* MRR
* MAP
* NDCG@K

## Tech Stack

* Python
* SQL
* MySQL
* Pandas
* NumPy
* Scikit-learn
* PyTorch
* Power BI
* FastAPI

## Project Structure

```text
financial-product-recommendation/
│
├── data_generator/
│   ├── config.py
│   └── generate_data.py
│
├── data/
│   └── generated/          # local generated files; do not commit datasets
│
├── database/
│   ├── schema.sql
│   ├── load_mysql.py
│   └── query_mysql.py
│
├── notebooks/
├── features/
├── models/
├── training/
├── inference/
├── api/
├── dashboard/
│
├── .env.example
├── requirements.txt
└── README.md
```

## Disclaimer

This project uses **synthetic financial data** for educational and research purposes. No real customer or financial information is used.
