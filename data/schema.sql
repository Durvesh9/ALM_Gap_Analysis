-- schema.sql
-- Drop existing table to ensure a clean run
DROP TABLE IF EXISTS alm_cashflows;

CREATE TABLE IF NOT EXISTS alm_cashflows (
    id SERIAL PRIMARY KEY,
    deal_id VARCHAR(50) NOT NULL,
    type VARCHAR(10) NOT NULL,
    product VARCHAR(50) NOT NULL,
    amount NUMERIC(20, 2) NOT NULL,
    interest_rate NUMERIC(8, 4) NOT NULL,
    maturity_date DATE NOT NULL,
    repricing_date DATE NOT NULL
);