import os
import pandas as pd
from sqlalchemy import create_engine

# Path to the database file inside the data folder
DB_PATH = os.path.join("data", "olist.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}")

# Mapping table names to CSV files
DATA_FILES = {
    "customers": os.path.join("data", "raw", "olist_customers_dataset.csv"),
    "orders": os.path.join("data", "raw", "olist_orders_dataset.csv"),
    "items": os.path.join("data", "raw", "olist_order_items_dataset.csv"),
    "reviews": os.path.join("data", "raw", "olist_order_reviews_dataset.csv")
}

def load_data():
    print("Starting database ingestion...")
    for table_name, file_path in DATA_FILES.items():
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing file: {file_path}. Please check your data/raw/ folder.")
        
        print(f"Loading '{table_name}' from {file_path}...")
        df = pd.read_csv(file_path)
        # Write to SQLite database
        df.to_sql(table_name, con=ENGINE, if_exists="replace", index=False)
        print(f"Table '{table_name}' successfully loaded ({len(df):,} rows).")
        
    print("\nAll tables successfully written to data/olist.db!")

if __name__ == "__main__":
    load_data()