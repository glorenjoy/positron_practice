# Business Analytics - Data Visualization Script (R)
# Purpose: Create business visualizations using ggplot2
# Author: Business Analytics Team
# Last Updated: 2024

# Load required libraries
library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)
library(readr)

# Custom theme for business charts
theme_business <- function() {
  theme_minimal() +
    theme(
      plot.title = element_text(size = 14, face = "bold", hjust = 0.5),
      plot.subtitle = element_text(size = 10, hjust = 0.5, color = "gray40"),
      axis.title = element_text(size = 10, face = "bold"),
      axis.text = element_text(size = 9),
      legend.position = "bottom",
      legend.title = element_text(face = "bold"),
      panel.grid.minor = element_blank(),
      plot.margin = margin(10, 10, 10, 10)
    )
}

# Load cleaned data
data_path <- "data/processed/sales_data_cleaned.csv"

if (file.exists(data_path)) {
  sales_data <- read_csv(data_path, show_col_types = FALSE)
} else {
  cat("Error: Cleaned data not found. Run data_cleaning.R first.\n")
  stop()
}

# 1. Sales by Region (Bar Chart)
plot_sales_by_region <- function(data) {
  region_summary <- data %>%
    group_by(region) %>%
    summarise(
      total_sales = sum(sales_amount),
      avg_transaction = mean(sales_amount),
      .groups = 'drop'
    ) %>%
    arrange(desc(total_sales))
  
  p <- ggplot(region_summary, aes(x = reorder(region, total_sales), y = total_sales)) +
    geom_bar(stat = "identity", fill = "#2E86AB", alpha = 0.8) +
    geom_text(aes(label = dollar(total_sales)), 
              hjust = -0.1, size = 3.5, fontface = "bold") +
    coord_flip() +
    scale_y_continuous(labels = dollar_format(), expand = expansion(mult = c(0, 0.15))) +
    labs(
      title = "Total Sales by Region",
      subtitle = "Q1 2024 Performance",
      x = "Region",
      y = "Total Sales ($)"
    ) +
    theme_business()
  
  return(p)
}

# 2. Sales Trend Over Time (Line Chart)
plot_sales_trend <- function(data) {
  daily_sales <- data %>%
    group_by(date) %>%
    summarise(daily_total = sum(sales_amount), .groups = 'drop')
  
  p <- ggplot(daily_sales, aes(x = date, y = daily_total)) +
    geom_line(color = "#A23B72", size = 1) +
    geom_point(color = "#A23B72", size = 2) +
    geom_smooth(method = "loess", se = TRUE, color = "#F18F01", alpha = 0.2) +
    scale_y_continuous(labels = dollar_format()) +
    scale_x_date(date_breaks = "1 week", date_labels = "%b %d") +
    labs(
      title = "Daily Sales Trend",
      subtitle = "With trend line (LOESS smoothing)",
      x = "Date",
      y = "Daily Sales ($)"
    ) +
    theme_business() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  return(p)
}

# 3. Sales by Product Category (Pie Chart alternative - Donut)
plot_sales_by_category <- function(data) {
  category_summary <- data %>%
    group_by(product_category) %>%
    summarise(total_sales = sum(sales_amount), .groups = 'drop') %>%
    mutate(
      percentage = total_sales / sum(total_sales) * 100,
      label = paste0(product_category, "\n", dollar(total_sales), 
                    "\n(", round(percentage, 1), "%)")
    )
  
  p <- ggplot(category_summary, aes(x = "", y = total_sales, fill = product_category)) +
    geom_bar(stat = "identity", width = 1, color = "white", size = 2) +
    coord_polar("y", start = 0) +
    scale_fill_manual(values = c("#2E86AB", "#A23B72", "#F18F01")) +
    labs(
      title = "Sales Distribution by Product Category",
      subtitle = "Q1 2024",
      fill = "Category"
    ) +
    theme_void() +
    theme(
      plot.title = element_text(size = 14, face = "bold", hjust = 0.5),
      plot.subtitle = element_text(size = 10, hjust = 0.5, color = "gray40"),
      legend.position = "right"
    )
  
  return(p)
}

# 4. Monthly Sales Comparison (Grouped Bar Chart)
plot_monthly_comparison <- function(data) {
  monthly_category <- data %>%
    group_by(month, product_category) %>%
    summarise(total_sales = sum(sales_amount), .groups = 'drop')
  
  p <- ggplot(monthly_category, aes(x = month, y = total_sales, fill = product_category)) +
    geom_bar(stat = "identity", position = "dodge", alpha = 0.8) +
    scale_y_continuous(labels = dollar_format()) +
    scale_fill_manual(values = c("#2E86AB", "#A23B72", "#F18F01")) +
    labs(
      title = "Monthly Sales by Product Category",
      subtitle = "Q1 2024 Breakdown",
      x = "Month",
      y = "Total Sales ($)",
      fill = "Category"
    ) +
    theme_business() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  return(p)
}

# 5. Sales Rep Performance (Horizontal Bar Chart)
plot_rep_performance <- function(data) {
  rep_summary <- data %>%
    group_by(sales_rep) %>%
    summarise(
      total_sales = sum(sales_amount),
      num_transactions = n(),
      avg_sale = mean(sales_amount),
      .groups = 'drop'
    ) %>%
    arrange(desc(total_sales))
  
  p <- ggplot(rep_summary, aes(x = reorder(sales_rep, total_sales), y = total_sales)) +
    geom_bar(stat = "identity", fill = "#F18F01", alpha = 0.8) +
    geom_text(aes(label = paste0(dollar(total_sales), "\n(", num_transactions, " sales)")), 
              hjust = -0.1, size = 3) +
    coord_flip() +
    scale_y_continuous(labels = dollar_format(), expand = expansion(mult = c(0, 0.15))) +
    labs(
      title = "Sales Representative Performance",
      subtitle = "Total Sales and Number of Transactions",
      x = "Sales Rep",
      y = "Total Sales ($)"
    ) +
    theme_business()
  
  return(p)
}

# Generate and save all plots
save_all_plots <- function() {
  dir.create("output/figures", recursive = TRUE, showWarnings = FALSE)
  
  cat("Generating visualizations...\n")
  
  # Save plots
  ggsave("output/figures/sales_by_region.png", 
         plot_sales_by_region(sales_data), 
         width = 8, height = 6, dpi = 300)
  cat("✓ Saved: sales_by_region.png\n")
  
  ggsave("output/figures/sales_trend.png", 
         plot_sales_trend(sales_data), 
         width = 10, height = 6, dpi = 300)
  cat("✓ Saved: sales_trend.png\n")
  
  ggsave("output/figures/sales_by_category.png", 
         plot_sales_by_category(sales_data), 
         width = 8, height = 6, dpi = 300)
  cat("✓ Saved: sales_by_category.png\n")
  
  ggsave("output/figures/monthly_comparison.png", 
         plot_monthly_comparison(sales_data), 
         width = 10, height = 6, dpi = 300)
  cat("✓ Saved: monthly_comparison.png\n")
  
  ggsave("output/figures/rep_performance.png", 
         plot_rep_performance(sales_data), 
         width = 8, height = 6, dpi = 300)
  cat("✓ Saved: rep_performance.png\n")
  
  cat("\nAll visualizations saved to output/figures/\n")
}

# Main execution
if (!interactive()) {
  save_all_plots()
} else {
  cat("Available functions:\n")
  cat("  - plot_sales_by_region(sales_data)\n")
  cat("  - plot_sales_trend(sales_data)\n")
  cat("  - plot_sales_by_category(sales_data)\n")
  cat("  - plot_monthly_comparison(sales_data)\n")
  cat("  - plot_rep_performance(sales_data)\n")
  cat("  - save_all_plots() - Generate all plots\n")
}
