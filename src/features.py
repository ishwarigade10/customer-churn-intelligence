import os
import pandas as pd
from sqlalchemy import create_engine

# Connect to the SQLite database
DB_PATH = os.path.join("data", "olist.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}")

# SQL query using Common Table Expressions (CTEs)
FEATURE_QUERY = """
WITH customer_orders AS (
    SELECT 
        c.customer_unique_id,
        o.order_id,
        o.order_purchase_timestamp,
        i.price,
        i.freight_value,
        r.review_score
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN items i ON o.order_id = i.order_id
    LEFT JOIN reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
),
customer_summary AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(price), 2) AS total_spend,
        ROUND(SUM(freight_value), 2) AS total_freight,
        ROUND(AVG(review_score), 2) AS avg_review_score,
        MIN(order_purchase_timestamp) AS first_order_date,
        MAX(order_purchase_timestamp) AS last_order_date,
        -- Define churn target:
        -- 1 = Churned (bought only once, never returned)
        -- 0 = Repeat Customer (returned and placed 2 or more orders)
        CASE 
            WHEN COUNT(DISTINCT order_id) = 1 THEN 1 
            ELSE 0 
        END AS is_churn
    FROM customer_orders
    GROUP BY customer_unique_id
)
SELECT 
    customer_unique_id,
    total_orders,
    total_spend,
    total_freight,
    ROUND(total_freight / (total_spend + 0.01), 3) AS freight_ratio,
    avg_review_score,
    first_order_date,
    last_order_date,
    is_churn
FROM customer_summary;
"""

def extract_features():
    print("Executing SQL feature engineering query...")
    df = pd.read_sql(FEATURE_QUERY, con=ENGINE)
    
    print(f"Features extracted successfully! Shape: {df.shape}")
    print("\nClass distribution (is_churn):")
    print(df['is_churn'].value_counts(normalize=True).round(3))
    
    # Save the aggregated features for machine learning
    output_path = os.path.join("data", "customer_features.parquet")
    df.to_parquet(output_path, index=False)
    print(f"\nFeatures saved to: {output_path}")

if __name__ == "__main__":
    extract_features()