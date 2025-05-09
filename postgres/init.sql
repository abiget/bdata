-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User information
CREATE TABLE IF NOT EXISTS users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product information
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(255) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Competitor information
CREATE TABLE IF NOT EXISTS competitors (
    competitor_id SERIAL PRIMARY KEY,
    competitor_name VARCHAR(255) UNIQUE NOT NULL,
    competitor_url VARCHAR(255) UNIQUE NOT NULL,
    importance_weight DECIMAL(3, 2) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Price history information
CREATE TABLE IF NOT EXISTS price_history (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(255) NOT NULL, -- Changed to match products table
    competitor_id INTEGER NOT NULL,   -- Changed to match competitors table type
    price DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    availability BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    url VARCHAR(255),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
);

-- Add indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_price_history_product 
ON price_history(product_id);

CREATE INDEX IF NOT EXISTS idx_price_history_competitor 
ON price_history(competitor_id);

CREATE INDEX IF NOT EXISTS idx_price_history_created_at 
ON price_history(created_at);