"""
Simple data cleaning script to prepare data for testing
This mimics the R cleaning script but in Python
"""
import pandas as pd
import os

# Read raw data
raw_data_path = "data/raw/sales_data.csv"
processed_data_path = "data/processed/sales_data_cleaned.csv"

print("Loading raw data...")
df = pd.read_csv(raw_data_path)
print(f"Loaded {len(df)} raw records")

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Remove duplicates
df = df.drop_duplicates()

# Remove records with missing critical fields
df = df.dropna(subset=['date', 'sales_amount', 'units_sold', 'region', 'product_category'])

# Remove negative values
df = df[(df['sales_amount'] > 0) & (df['units_sold'] > 0)]

# Add derived fields
df['unit_price'] = df['sales_amount'] / df['units_sold']
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month_name()
df['month_num'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter
df['week'] = df['date'].dt.isocalendar().week

# Standardize text fields
df['region'] = df['region'].str.upper()
df['product_category'] = df['product_category'].str.title()

# Sort by date
df = df.sort_values('date')

print(f"After cleaning: {len(df)} records")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")

# Save cleaned data
os.makedirs("data/processed", exist_ok=True)
df.to_csv(processed_data_path, index=False)
print(f"\nCleaned data saved to: {processed_data_path}")
