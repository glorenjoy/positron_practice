"""
Business Analytics - Data Visualization Script (Python)
Purpose: Create business visualizations using matplotlib and seaborn
Author: Business Analytics Team
Last Updated: 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import os

# Set style for professional-looking charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'

# Configuration
PROCESSED_DATA_PATH = "data/processed/sales_data_cleaned.csv"
OUTPUT_PATH = "output/figures"

# Color palette
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#06A77D',
    'warning': '#F77F00'
}

def load_data():
    """Load cleaned sales data"""
    if not os.path.exists(PROCESSED_DATA_PATH):
        print(f"Error: Cleaned data not found at {PROCESSED_DATA_PATH}")
        print("Please run R data_cleaning.R first.")
        return None
    
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])
    print(f"✓ Loaded {len(df)} records for visualization")
    return df

def plot_revenue_heatmap(df):
    """Create heatmap of revenue by region and category"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Pivot data
    heatmap_data = df.pivot_table(
        values='sales_amount',
        index='region',
        columns='product_category',
        aggfunc='sum'
    )
    
    # Create heatmap
    sns.heatmap(heatmap_data, annot=True, fmt=',.0f', cmap='YlOrRd',
                cbar_kws={'label': 'Total Sales ($)'}, ax=ax)
    
    ax.set_title('Revenue Heatmap: Region × Product Category', pad=20)
    ax.set_xlabel('Product Category', fontweight='bold')
    ax.set_ylabel('Region', fontweight='bold')
    
    plt.tight_layout()
    return fig

def plot_sales_distribution(df):
    """Create distribution plot of sales amounts"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Histogram with KDE
    ax1.hist(df['sales_amount'], bins=30, color=COLORS['primary'], 
             alpha=0.7, edgecolor='black')
    ax1.axvline(df['sales_amount'].mean(), color=COLORS['warning'], 
                linestyle='--', linewidth=2, label=f"Mean: ${df['sales_amount'].mean():.2f}")
    ax1.axvline(df['sales_amount'].median(), color=COLORS['success'], 
                linestyle='--', linewidth=2, label=f"Median: ${df['sales_amount'].median():.2f}")
    ax1.set_xlabel('Sales Amount ($)', fontweight='bold')
    ax1.set_ylabel('Frequency', fontweight='bold')
    ax1.set_title('Sales Amount Distribution', pad=15)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Box plot by category
    df.boxplot(column='sales_amount', by='product_category', ax=ax2, 
               patch_artist=True, grid=True)
    ax2.set_xlabel('Product Category', fontweight='bold')
    ax2.set_ylabel('Sales Amount ($)', fontweight='bold')
    ax2.set_title('Sales Distribution by Category', pad=15)
    plt.suptitle('')  # Remove default title
    
    plt.tight_layout()
    return fig

def plot_time_series_advanced(df):
    """Create advanced time series visualization"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Daily sales with moving average
    daily_sales = df.groupby('date')['sales_amount'].sum().reset_index()
    daily_sales['MA_7'] = daily_sales['sales_amount'].rolling(window=7, min_periods=1).mean()
    
    ax1.plot(daily_sales['date'], daily_sales['sales_amount'], 
             color=COLORS['primary'], alpha=0.5, linewidth=1, label='Daily Sales')
    ax1.plot(daily_sales['date'], daily_sales['MA_7'], 
             color=COLORS['secondary'], linewidth=2.5, label='7-Day Moving Average')
    ax1.fill_between(daily_sales['date'], daily_sales['sales_amount'], 
                      alpha=0.2, color=COLORS['primary'])
    ax1.set_xlabel('Date', fontweight='bold')
    ax1.set_ylabel('Sales Amount ($)', fontweight='bold')
    ax1.set_title('Daily Sales Trend with Moving Average', pad=15)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Cumulative sales by category
    for category in df['product_category'].unique():
        cat_data = df[df['product_category'] == category].sort_values('date')
        cumulative = cat_data.groupby('date')['sales_amount'].sum().cumsum()
        ax2.plot(cumulative.index, cumulative.values, linewidth=2.5, 
                label=category, marker='o', markersize=3)
    
    ax2.set_xlabel('Date', fontweight='bold')
    ax2.set_ylabel('Cumulative Sales ($)', fontweight='bold')
    ax2.set_title('Cumulative Sales by Product Category', pad=15)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig

def plot_regional_comparison(df):
    """Create comprehensive regional comparison"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Total sales by region (bar chart)
    region_sales = df.groupby('region')['sales_amount'].sum().sort_values(ascending=True)
    colors_bar = [COLORS['primary'] if x == region_sales.max() else COLORS['secondary'] 
                  for x in region_sales]
    region_sales.plot(kind='barh', ax=ax1, color=colors_bar, alpha=0.8)
    ax1.set_xlabel('Total Sales ($)', fontweight='bold')
    ax1.set_ylabel('Region', fontweight='bold')
    ax1.set_title('Total Sales by Region', pad=15)
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for i, v in enumerate(region_sales.values):
        ax1.text(v + 1000, i, f'${v:,.0f}', va='center', fontweight='bold')
    
    # 2. Average transaction value by region
    region_avg = df.groupby('region')['sales_amount'].mean().sort_values(ascending=True)
    region_avg.plot(kind='barh', ax=ax2, color=COLORS['accent'], alpha=0.8)
    ax2.set_xlabel('Average Transaction ($)', fontweight='bold')
    ax2.set_ylabel('Region', fontweight='bold')
    ax2.set_title('Average Transaction Value by Region', pad=15)
    ax2.grid(True, alpha=0.3, axis='x')
    
    # 3. Number of transactions by region (pie chart)
    region_count = df.groupby('region').size()
    colors_pie = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['success']]
    ax3.pie(region_count.values, labels=region_count.index, autopct='%1.1f%%',
            startangle=90, colors=colors_pie, textprops={'fontweight': 'bold'})
    ax3.set_title('Transaction Distribution by Region', pad=15)
    
    # 4. Sales by region and month (stacked bar)
    region_month = df.pivot_table(values='sales_amount', index='month_num', 
                                    columns='region', aggfunc='sum')
    region_month.plot(kind='bar', stacked=True, ax=ax4, 
                      color=[COLORS['primary'], COLORS['secondary'], 
                            COLORS['accent'], COLORS['success']], alpha=0.8)
    ax4.set_xlabel('Month', fontweight='bold')
    ax4.set_ylabel('Total Sales ($)', fontweight='bold')
    ax4.set_title('Monthly Sales Trend by Region', pad=15)
    ax4.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.tick_params(axis='x', rotation=0)
    
    plt.tight_layout()
    return fig

def plot_category_performance(df):
    """Create category performance dashboard"""
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # 1. Revenue by category
    ax1 = fig.add_subplot(gs[0, :])
    category_revenue = df.groupby('product_category').agg({
        'sales_amount': 'sum',
        'units_sold': 'sum'
    }).sort_values('sales_amount', ascending=False)
    
    x = np.arange(len(category_revenue.index))
    width = 0.35
    
    ax1_twin = ax1.twinx()
    bars1 = ax1.bar(x - width/2, category_revenue['sales_amount'], width, 
                     label='Revenue', color=COLORS['primary'], alpha=0.8)
    bars2 = ax1_twin.bar(x + width/2, category_revenue['units_sold'], width, 
                          label='Units Sold', color=COLORS['accent'], alpha=0.8)
    
    ax1.set_xlabel('Product Category', fontweight='bold')
    ax1.set_ylabel('Revenue ($)', fontweight='bold', color=COLORS['primary'])
    ax1_twin.set_ylabel('Units Sold', fontweight='bold', color=COLORS['accent'])
    ax1.set_title('Category Performance: Revenue vs Units Sold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(category_revenue.index, rotation=0)
    ax1.tick_params(axis='y', labelcolor=COLORS['primary'])
    ax1_twin.tick_params(axis='y', labelcolor=COLORS['accent'])
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    # 2. Unit price analysis
    ax2 = fig.add_subplot(gs[1, 0])
    category_price = df.groupby('product_category')['unit_price'].agg(['mean', 'min', 'max'])
    category_price.plot(kind='bar', ax=ax2, color=[COLORS['primary'], COLORS['secondary'], COLORS['accent']], 
                        alpha=0.8)
    ax2.set_xlabel('Product Category', fontweight='bold')
    ax2.set_ylabel('Unit Price ($)', fontweight='bold')
    ax2.set_title('Unit Price Analysis by Category', pad=15)
    ax2.legend(['Average', 'Minimum', 'Maximum'])
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Category trend over time
    ax3 = fig.add_subplot(gs[1, 1])
    for category in df['product_category'].unique():
        cat_daily = df[df['product_category'] == category].groupby('date')['sales_amount'].sum()
        ax3.plot(cat_daily.index, cat_daily.values, linewidth=2, label=category, marker='o', markersize=2)
    ax3.set_xlabel('Date', fontweight='bold')
    ax3.set_ylabel('Daily Sales ($)', fontweight='bold')
    ax3.set_title('Daily Sales Trend by Category', pad=15)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(axis='x', rotation=45)
    
    # 4. Category mix by region
    ax4 = fig.add_subplot(gs[2, :])
    category_region = df.pivot_table(values='sales_amount', index='region', 
                                      columns='product_category', aggfunc='sum')
    category_region_pct = category_region.div(category_region.sum(axis=1), axis=0) * 100
    category_region_pct.plot(kind='bar', stacked=True, ax=ax4, 
                              color=[COLORS['primary'], COLORS['secondary'], COLORS['accent']], 
                              alpha=0.8)
    ax4.set_xlabel('Region', fontweight='bold')
    ax4.set_ylabel('Percentage (%)', fontweight='bold')
    ax4.set_title('Product Category Mix by Region', pad=15)
    ax4.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.tick_params(axis='x', rotation=0)
    
    return fig

def save_all_visualizations():
    """Generate and save all visualizations"""
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    print("\nGenerating Python visualizations...")
    print("="*60)
    
    # Generate and save plots
    plots = {
        'revenue_heatmap_py.png': plot_revenue_heatmap,
        'sales_distribution_py.png': plot_sales_distribution,
        'time_series_advanced_py.png': plot_time_series_advanced,
        'regional_comparison_py.png': plot_regional_comparison,
        'category_performance_py.png': plot_category_performance
    }
    
    for filename, plot_func in plots.items():
        try:
            fig = plot_func(df)
            filepath = os.path.join(OUTPUT_PATH, filename)
            fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close(fig)
            print(f"✓ Saved: {filename}")
        except Exception as e:
            print(f"✗ Error creating {filename}: {str(e)}")
    
    print(f"\nAll visualizations saved to {OUTPUT_PATH}/")
    print("="*60)

def main():
    """Main execution"""
    save_all_visualizations()

if __name__ == "__main__":
    main()
