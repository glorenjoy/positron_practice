# Business Analytics - Data Cleaning Script
# Purpose: Clean and validate sales data for analysis
# Author: Business Analytics Team
# Last Updated: 2024

# Load required libraries
library(dplyr)
library(lubridate)
library(readr)

# Define paths
raw_data_path <- "data/raw/sales_data.csv"
processed_data_path <- "data/processed/sales_data_cleaned.csv"

# Function to clean and validate sales data
clean_sales_data <- function(input_file, output_file) {
  
  cat("Starting data cleaning process...\n")
  
  # Read raw data
  sales_raw <- read_csv(input_file, show_col_types = FALSE)
  cat(sprintf("Loaded %d raw records\n", nrow(sales_raw)))
  
  # Data cleaning steps
  sales_cleaned <- sales_raw %>%
    # Convert date to proper date format
    mutate(date = as.Date(date)) %>%
    
    # Remove any duplicate records
    distinct() %>%
    
    # Remove records with missing critical fields
    filter(!is.na(date),
           !is.na(sales_amount),
           !is.na(units_sold),
           !is.na(region),
           !is.na(product_category)) %>%
    
    # Data validation: Remove negative values
    filter(sales_amount > 0,
           units_sold > 0) %>%
    
    # Add derived fields for analysis
    mutate(
      # Calculate unit price
      unit_price = sales_amount / units_sold,
      
      # Extract time components
      year = year(date),
      month = month(date, label = TRUE, abbr = FALSE),
      month_num = month(date),
      quarter = quarter(date),
      week = week(date),
      
      # Standardize text fields
      region = toupper(region),
      product_category = tools::toTitleCase(product_category)
    ) %>%
    
    # Arrange by date
    arrange(date)
  
  cat(sprintf("After cleaning: %d records\n", nrow(sales_cleaned)))
  cat(sprintf("Removed %d records (%.1f%%)\n", 
      nrow(sales_raw) - nrow(sales_cleaned),
      100 * (nrow(sales_raw) - nrow(sales_cleaned)) / nrow(sales_raw)))
  
  # Data quality checks
  cat("\n=== Data Quality Summary ===\n")
  cat(sprintf("Date range: %s to %s\n", 
      min(sales_cleaned$date), 
      max(sales_cleaned$date)))
  cat(sprintf("Total sales: $%.2f\n", sum(sales_cleaned$sales_amount)))
  cat(sprintf("Average transaction: $%.2f\n", mean(sales_cleaned$sales_amount)))
  cat(sprintf("Number of regions: %d\n", n_distinct(sales_cleaned$region)))
  cat(sprintf("Number of categories: %d\n", n_distinct(sales_cleaned$product_category)))
  cat(sprintf("Number of sales reps: %d\n", n_distinct(sales_cleaned$sales_rep)))
  
  # Check for outliers (using IQR method)
  Q1 <- quantile(sales_cleaned$sales_amount, 0.25)
  Q3 <- quantile(sales_cleaned$sales_amount, 0.75)
  IQR_val <- Q3 - Q1
  outliers <- sales_cleaned %>%
    filter(sales_amount < (Q1 - 1.5 * IQR_val) | 
           sales_amount > (Q3 + 1.5 * IQR_val))
  
  if (nrow(outliers) > 0) {
    cat(sprintf("\nWarning: %d potential outliers detected\n", nrow(outliers)))
  } else {
    cat("\nNo outliers detected\n")
  }
  
  # Save cleaned data
  write_csv(sales_cleaned, output_file)
  cat(sprintf("\nCleaned data saved to: %s\n", output_file))
  
  return(sales_cleaned)
}

# Main execution
if (!interactive()) {
  # Run from command line
  sales_data <- clean_sales_data(raw_data_path, processed_data_path)
} else {
  # Run interactively
  cat("To clean data, run: sales_data <- clean_sales_data(raw_data_path, processed_data_path)\n")
}
