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
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    brand VARCHAR(100),
    description TEXT,
    features JSONB  -- Flexible storage for product attributes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

-- Competitor information
CREATE TABLE competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    importance_weight DECIMAL(3, 2) DEFAULT 1.0,
    url VARCHAR(255),
    -- tier VARCHAR(50)  -- Budget, mid-range, premium, etc. tier: Classification by market positioning (budget, mid-range, premium).
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

-- Price history information
CREATE TABLE price_history (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    competitor_id VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    availability BOOLEAN DEFAULT TRUE, -- true if available, false if not but i need to think about this
    created_at TIMESTAMP NOT NULL,
    url VARCHAR(255), -- URL to the product page on the competitor's site
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT fk_competitor FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
);

-- Sales data information
CREATE TABLE sales_data (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    units_sold INTEGER,
    revenue DECIMAL(12, 2),
    
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);


-- Price analysis information opitionally
-- CREATE TABLE price_analysis (
--     id SERIAL PRIMARY KEY,
--     product_id VARCHAR(50) NOT NULL,
--     analysis_date DATE NOT NULL,
--     avg_market_price DECIMAL(10, 2),
--     min_market_price DECIMAL(10, 2),
--     max_market_price DECIMAL(10, 2),
--     price_volatility DECIMAL(5, 2),  -- Standard deviation
--     price_trend DECIMAL(5, 2),  -- Slope of trend line
    
--     CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(product_id)
-- );


CREATE TABLE price_recommendations (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    generation_date DATE NOT NULL,
    current_price DECIMAL(10, 2),
    recommended_price DECIMAL(10, 2),
    expected_profit_change DECIMAL(5, 2),  -- Percentage
    confidence_score DECIMAL(3, 2),  -- 0-1 value
    -- reasoning TEXT,
    
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);


CREATE TABLE customer_actions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50),  -- Can be anonymous ID
    product_id VARCHAR(50) NOT NULL,
    action_type VARCHAR(20) NOT NULL, -- view, search, wishlist_add, cart_add, checkout_start, purchase
    price_at_action DECIMAL(10, 2) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    session_id VARCHAR(100),
    device_type VARCHAR(50),  -- desktop, mobile, tablet
    
    CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(product_id)
);