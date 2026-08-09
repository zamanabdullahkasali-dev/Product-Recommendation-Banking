# Financial Product Recommendation System

A deep learning-based recommendation system that predicts and recommends suitable financial products to customers based on their profiles, transaction behavior, financial activity, and historical product interactions.

## Project Overview

This project uses **Neural Collaborative Filtering (NCF)** to learn customer and product representations and generate personalized financial product recommendations.

The project uses synthetic banking data designed to simulate realistic customer behavior while avoiding the use of real financial customer information.

## Objectives

* Generate realistic synthetic banking data.
* Analyze customer financial behavior.
* Build customer and product features.
* Implement traditional recommendation baselines.
* Build a Neural Collaborative Filtering model.
* Generate personalized Top-K financial product recommendations.
* Evaluate recommendation performance using ranking metrics.

## Financial Products

The system can recommend products such as:

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

## Dataset

The project uses a synthetic banking dataset containing:

* Customer profiles
* Transactions
* Financial products
* Product ownership
* Loans
* Investments
* Insurance
* Credit information
* Customer-product interactions

The data generator is designed to create realistic relationships between customer attributes, financial behavior, and product adoption.

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

## Features

Example features include:

* Income
* Credit Score
* Average Monthly Spend
* Savings Rate
* Debt-to-Income Ratio
* Credit Utilization
* Investment Ratio
* Transaction Frequency
* Travel Frequency
* Shopping Frequency
* Number of Existing Products
* Customer Recency
* Customer Frequency
* Monetary Value

## Evaluation

Recommendation performance will be evaluated using:

* Precision@K
* Recall@K
* Hit Rate@K
* MRR
* MAP
* NDCG@K

## Tech Stack

* Python
* SQL
* PostgreSQL
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
├── data/
├── database/
├── notebooks/
├── features/
├── models/
├── training/
├── inference/
├── api/
├── dashboard/
│
├── requirements.txt
└── README.md
```

## Disclaimer

This project uses **synthetic financial data** for educational and research purposes. No real customer or financial information is used.

