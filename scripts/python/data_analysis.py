"""
Business Analytics - Data Analysis Script (Python)
Purpose: Perform statistical analysis on sales data using pandas
Author: Business Analytics Team
Last Updated: 2024
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

# Configuration
RAW_DATA_PATH = "data/raw/sales_data.csv"
PROCESSED_DATA_PATH = "data/processed/sales_data_cleaned.csv"
OUTPUT_PATH = "output/tables"

def load_sales_data():
    """Load cleaned sales data"""
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"Error: Cleaned data not found at {PROCESSED_DATA_PATH}")
        print("Please run R data_cleaning.R first or check the path.")
        return None
    
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])
    print(f"✓ Loaded {len(df)} records")
    return df

def calculate_kpis(df):
    """Calculate key performance indicators"""
    print("\n" + "="*60)
    print("KEY PERFORMANCE INDICATORS (KPIs)")
    print("="*60)
    
    kpis = {
        'Total Revenue': f"${df['sales_amount'].sum():,.2f}",
        'Average Transaction Value': f"${df['sales_amount'].mean():,.2f}",
        'Median Transaction Value': f"${df['sales_amount'].median():,.2f}",
        'Total Units Sold': f"{df['units_sold'].sum():,}",
        'Number of Transactions': f"{len(df):,}",
        'Number of Unique Customers': f"{df['customer_id'].nunique():,}",
        'Average Units per Transaction': f"{df['units_sold'].mean():.2f}",
        'Date Range': f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}"
    }
    
    for key, value in kpis.items():
        print(f"{key:.<40} {value}")
    
    return kpis

def analyze_by_region(df):
    """Analyze sales performance by region"""
    print("\n" + "="*60)
    print("REGIONAL ANALYSIS")
    print("="*60)
    
    region_analysis = df.groupby('region').agg({
        'sales_amount': ['sum', 'mean', 'count'],
        'units_sold': 'sum',
        'customer_id': 'nunique'
    }).round(2)
    
    region_analysis.columns = ['Total Sales', 'Avg Transaction', 'Num Transactions', 
                                'Total Units', 'Unique Customers']
    
    # Calculate market share
    region_analysis['Market Share %'] = (
        region_analysis['Total Sales'] / region_analysis['Total Sales'].sum() * 100
    ).round(2)
    
    # Sort by total sales
    region_analysis = region_analysis.sort_values('Total Sales', ascending=False)
    
    print(region_analysis.to_string())
    
    return region_analysis

def analyze_by_category(df):
    """Analyze sales by product category"""
    print("\n" + "="*60)
    print("PRODUCT CATEGORY ANALYSIS")
    print("="*60)
    
    category_analysis = df.groupby('product_category').agg({
        'sales_amount': ['sum', 'mean', 'count'],
        'units_sold': 'sum',
        'unit_price': 'mean'
    }).round(2)
    
    category_analysis.columns = ['Total Sales', 'Avg Transaction', 'Num Transactions', 
                                  'Total Units', 'Avg Unit Price']
    
    # Calculate contribution percentage
    category_analysis['Revenue Contribution %'] = (
        category_analysis['Total Sales'] / category_analysis['Total Sales'].sum() * 100
    ).round(2)
    
    category_analysis = category_analysis.sort_values('Total Sales', ascending=False)
    
    print(category_analysis.to_string())
    
    return category_analysis

def analyze_time_series(df):
    """Perform time series analysis"""
    print("\n" + "="*60)
    print("TIME SERIES ANALYSIS")
    print("="*60)
    
    # Monthly aggregation
    monthly = df.groupby('month').agg({
        'sales_amount': ['sum', 'mean', 'count']
    }).round(2)
    
    monthly.columns = ['Total Sales', 'Avg Transaction', 'Num Transactions']
    
    # Calculate growth rates
    monthly['Growth %'] = monthly['Total Sales'].pct_change() * 100
    monthly['Growth %'] = monthly['Growth %'].round(2)
    
    print("\nMonthly Performance:")
    print(monthly.to_string())
    
    # Weekly patterns
    df['day_of_week'] = df['date'].dt.day_name()
    weekly = df.groupby('day_of_week')['sales_amount'].agg(['sum', 'mean', 'count'])
    weekly.columns = ['Total Sales', 'Avg Transaction', 'Num Transactions']
    
    # Reorder days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly = weekly.reindex([day for day in day_order if day in weekly.index])
    
    print("\nWeekly Pattern (by day of week):")
    print(weekly.to_string())
    
    return monthly, weekly

def analyze_sales_reps(df):
    """Analyze sales representative performance"""
    print("\n" + "="*60)
    print("SALES REPRESENTATIVE PERFORMANCE")
    print("="*60)
    
    rep_analysis = df.groupby('sales_rep').agg({
        'sales_amount': ['sum', 'mean', 'count'],
        'customer_id': 'nunique'
    }).round(2)
    
    rep_analysis.columns = ['Total Sales', 'Avg Sale', 'Num Sales', 'Unique Customers']
    
    # Calculate performance metrics
    rep_analysis['Sales per Customer'] = (
        rep_analysis['Total Sales'] / rep_analysis['Unique Customers']
    ).round(2)
    
    rep_analysis = rep_analysis.sort_values('Total Sales', ascending=False)
    
    print(rep_analysis.to_string())
    
    # Identify top performer
    top_rep = rep_analysis.index[0]
    print(f"\n🏆 Top Performer: {top_rep} with ${rep_analysis.loc[top_rep, 'Total Sales']:,.2f} in sales")
    
    return rep_analysis

def generate_summary_statistics(df):
    """Generate detailed summary statistics"""
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    
    print("\nSales Amount Distribution:")
    print(df['sales_amount'].describe().round(2))
    
    print("\nUnits Sold Distribution:")
    print(df['units_sold'].describe().round(2))
    
    # Correlation analysis
    numeric_cols = ['sales_amount', 'units_sold', 'unit_price']
    correlation = df[numeric_cols].corr().round(3)
    
    print("\nCorrelation Matrix:")
    print(correlation.to_string())
    
    return correlation

def save_analysis_results(kpis, region_analysis, category_analysis, rep_analysis):
    """Save analysis results to CSV files"""
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    # Save KPIs
    kpi_df = pd.DataFrame(list(kpis.items()), columns=['Metric', 'Value'])
    kpi_df.to_csv(f"{OUTPUT_PATH}/kpis.csv", index=False)
    print(f"\n✓ Saved KPIs to {OUTPUT_PATH}/kpis.csv")
    
    # Save regional analysis
    region_analysis.to_csv(f"{OUTPUT_PATH}/regional_analysis.csv")
    print(f"✓ Saved regional analysis to {OUTPUT_PATH}/regional_analysis.csv")
    
    # Save category analysis
    category_analysis.to_csv(f"{OUTPUT_PATH}/category_analysis.csv")
    print(f"✓ Saved category analysis to {OUTPUT_PATH}/category_analysis.csv")
    
    # Save rep analysis
    rep_analysis.to_csv(f"{OUTPUT_PATH}/rep_analysis.csv")
    print(f"✓ Saved rep analysis to {OUTPUT_PATH}/rep_analysis.csv")

def main():
    """Main analysis workflow"""
    print("Starting Business Analytics Analysis...")
    print("="*60)
    
    # Load data
    df = load_sales_data()
    if df is None:
        return
    
    # Perform analyses
    kpis = calculate_kpis(df)
    region_analysis = analyze_by_region(df)
    category_analysis = analyze_by_category(df)
    monthly, weekly = analyze_time_series(df)
    rep_analysis = analyze_sales_reps(df)
    correlation = generate_summary_statistics(df)
    
    # Save results
    save_analysis_results(kpis, region_analysis, category_analysis, rep_analysis)
    
    print("\n" + "="*60)
    print("Analysis Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
