CREATE DATABASE IF NOT EXISTS banking_recommendation
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE banking_recommendation;

CREATE TABLE IF NOT EXISTS customers (
    customer_id BIGINT PRIMARY KEY,
    age TINYINT UNSIGNED NOT NULL,
    gender VARCHAR(10) NOT NULL,
    marital_status VARCHAR(20) NOT NULL,
    education VARCHAR(30) NOT NULL,
    occupation VARCHAR(60) NOT NULL,
    employment_type VARCHAR(30) NOT NULL,
    monthly_income DECIMAL(14,2) NOT NULL,
    city VARCHAR(60) NOT NULL,
    state VARCHAR(60) NOT NULL,
    credit_score SMALLINT UNSIGNED NOT NULL,
    risk_profile VARCHAR(20) NOT NULL,
    customer_segment VARCHAR(30) NOT NULL,
    average_monthly_balance DECIMAL(14,2) NOT NULL,
    relationship_tenure_months SMALLINT UNSIGNED NOT NULL,
    digital_banking_score DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(30) NOT NULL,
    annual_fee DECIMAL(12,2) NOT NULL,
    interest_rate DECIMAL(6,2) NOT NULL,
    risk_level VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS merchants (
    merchant_id VARCHAR(20) PRIMARY KEY,
    merchant_name VARCHAR(100) NOT NULL,
    category VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(30) PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    merchant_id VARCHAR(20) NOT NULL,
    merchant_category VARCHAR(40) NOT NULL,
    transaction_amount DECIMAL(14,2) NOT NULL,
    transaction_timestamp DATETIME NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    INDEX idx_transactions_customer_date (customer_id, transaction_timestamp),
    INDEX idx_transactions_category (merchant_category),
    CONSTRAINT fk_transactions_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT fk_transactions_merchant FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
);

CREATE TABLE IF NOT EXISTS customer_products (
    customer_id BIGINT NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    purchase_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    PRIMARY KEY (customer_id, product_id),
    INDEX idx_customer_products_product (product_id),
    CONSTRAINT fk_customer_products_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT fk_customer_products_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE IF NOT EXISTS monthly_customer_summary (
    customer_id BIGINT NOT NULL,
    month CHAR(7) NOT NULL,
    transaction_count INT UNSIGNED NOT NULL,
    total_spend DECIMAL(16,2) NOT NULL,
    average_transaction_amount DECIMAL(14,2) NOT NULL,
    shopping_spend DECIMAL(16,2) NOT NULL,
    travel_spend DECIMAL(16,2) NOT NULL,
    investment_spend DECIMAL(16,2) NOT NULL,
    savings_rate_proxy DECIMAL(8,4) NOT NULL,
    debt_to_income_proxy DECIMAL(8,4) NOT NULL,
    monthly_income DECIMAL(14,2) NOT NULL,
    PRIMARY KEY (customer_id, month),
    INDEX idx_summary_month (month),
    CONSTRAINT fk_summary_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
