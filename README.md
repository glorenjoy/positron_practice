# Business Analytics Project with Positron

A comprehensive starter project for business analytics using **Positron IDE** with R and Python. This project demonstrates modern data analytics workflows, from data cleaning to interactive dashboards, focusing on business KPIs and data-driven decision making.

## 📊 Project Overview

This analytics project provides a complete framework for analyzing business sales data, featuring:

- **Data Quality & Accuracy**: Robust data cleaning and validation processes
- **Multi-Language Analysis**: Leveraging both R and Python for comprehensive insights
- **Professional Visualizations**: High-quality charts using ggplot2 and matplotlib
- **Interactive Dashboards**: Quarto-based business intelligence reports
- **Business-Focused Insights**: KPI tracking and actionable recommendations

## 🗂️ Project Structure

```
positron_practice/
├── data/
│   ├── raw/                    # Original, immutable data
│   │   └── sales_data.csv      # Sample sales dataset
│   └── processed/              # Cleaned, validated data
│
├── scripts/
│   ├── r/                      # R analysis scripts
│   │   ├── data_cleaning.R     # Data validation and cleaning
│   │   └── visualizations.R    # ggplot2 visualizations
│   └── python/                 # Python analysis scripts
│       ├── data_analysis.py    # pandas statistical analysis
│       └── visualizations.py   # matplotlib/seaborn charts
│
├── notebooks/                  # Jupyter/R notebooks for exploration
│
├── reports/                    # Quarto reports and dashboards
│   └── business_dashboard.qmd  # Interactive KPI dashboard
│
├── output/                     # Generated outputs
│   ├── figures/               # Visualization exports
│   └── tables/                # Analysis results (CSV/Excel)
│
├── requirements.txt           # Python dependencies
├── r_packages.txt            # R package list
└── README.md                 # This file
```

## 🚀 Getting Started

### Prerequisites

1. **Positron IDE** - Download from [positron.posit.co](https://positron.posit.co/)
2. **R** (≥ 4.0.0) - [r-project.org](https://www.r-project.org/)
3. **Python** (≥ 3.8) - [python.org](https://www.python.org/)
4. **Quarto** - [quarto.org](https://quarto.org/)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/glorenjoy/positron_practice.git
cd positron_practice
```

#### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Install R Packages

Open R or RStudio and run:

```r
# Install required packages
packages <- c("dplyr", "tidyr", "lubridate", "readr", "ggplot2", 
              "scales", "knitr", "rmarkdown", "DT")

install.packages(packages)
```

### Quick Start Guide

#### Step 1: Data Cleaning (R)

```bash
# Run from project root
Rscript scripts/r/data_cleaning.R
```

This script:
- ✅ Validates data quality
- ✅ Removes duplicates and invalid records
- ✅ Creates derived fields (date components, unit prices)
- ✅ Outputs cleaned data to `data/processed/`

#### Step 2: Generate Visualizations

**R Visualizations (ggplot2):**
```bash
Rscript scripts/r/visualizations.R
```

**Python Visualizations (matplotlib/seaborn):**
```bash
python scripts/python/data_analysis.py
python scripts/python/visualizations.py
```

#### Step 3: Run Statistical Analysis

```bash
python scripts/python/data_analysis.py
```

This generates:
- KPI calculations
- Regional performance analysis
- Product category insights
- Sales rep performance metrics
- Time series analysis

#### Step 4: Create Dashboard

```bash
quarto render reports/business_dashboard.qmd
```

Opens an interactive HTML dashboard with:
- Executive summary with key KPIs
- Regional performance breakdown
- Product category analysis
- Sales trends and forecasts
- Team performance metrics
- Data-driven recommendations

## 📈 Business Analytics Use Cases

### 1. **Performance Monitoring**
Track key business metrics in real-time:
- Total revenue and growth rates
- Regional market share
- Product category performance
- Sales team productivity

### 2. **Strategic Planning**
Use insights for data-driven decisions:
- Identify high-performing regions for expansion
- Optimize product mix based on profitability
- Allocate resources to top-performing categories
- Set realistic sales targets

### 3. **Operational Optimization**
Improve day-to-day operations:
- Identify sales patterns and seasonality
- Optimize inventory based on demand
- Benchmark sales rep performance
- Detect anomalies and outliers

### 4. **Customer Intelligence**
Understand customer behavior:
- Track customer acquisition and retention
- Analyze purchase patterns
- Calculate customer lifetime value
- Segment customers for targeted marketing

## 🎯 Key Features

### Data Accuracy & Quality

- **Validation Rules**: Automatic detection of negative values, missing data, and duplicates
- **Data Profiling**: Comprehensive statistics on data quality and completeness
- **Outlier Detection**: IQR-based methods to identify unusual transactions
- **Audit Trail**: Clear documentation of data transformations

### Effective Visualizations

**R (ggplot2) Visualizations:**
- Regional sales comparison (bar charts)
- Daily sales trends with smoothing (line charts)
- Category distribution (pie/donut charts)
- Monthly performance comparison (grouped bars)
- Sales rep rankings (horizontal bars)

**Python (matplotlib/seaborn) Visualizations:**
- Revenue heatmaps (region × category)
- Distribution analysis (histograms, box plots)
- Advanced time series with moving averages
- Comprehensive regional dashboards
- Category performance matrices

### Interactive Dashboards

The Quarto dashboard features:
- **Tabbed Navigation**: Easy access to different analyses
- **Interactive Tables**: Sortable, searchable data tables
- **Responsive Design**: Clean UI that works on all devices
- **Embedded Insights**: Contextual recommendations and callouts
- **Export Options**: Download charts and data for presentations

## 📝 Sample Data

The project includes a sample dataset (`data/raw/sales_data.csv`) with:
- 50 transactions across Q1 2024
- 4 regions (North, South, East, West)
- 3 product categories (Electronics, Furniture, Office Supplies)
- 5 sales representatives
- Fields: date, region, product_category, sales_amount, units_sold, customer_id, sales_rep

**Replace this with your own data** while maintaining the same column structure.

## 🛠️ Customization

### Adding Your Own Data

1. Place your CSV file in `data/raw/`
2. Update file paths in scripts if necessary
3. Modify `data_cleaning.R` validation rules as needed
4. Re-run the analysis pipeline

### Customizing Visualizations

- **Colors**: Update color palettes in script headers
- **Themes**: Modify `theme_business()` function in R scripts
- **Chart Types**: Swap visualization functions as needed
- **KPIs**: Add custom metrics to analysis scripts

### Extending the Dashboard

Edit `reports/business_dashboard.qmd`:
- Add new sections with `##` headers
- Insert R/Python code chunks with ` ```{r}` or ` ```{python}`
- Customize layout with Quarto's grid system
- Add interactive widgets with `htmlwidgets`

## 🤝 Contributing

This is a practice repository, but suggestions and improvements are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with enhancements
- Share your own analytics use cases

## 📚 Resources

### Positron IDE
- [Documentation](https://positron.posit.co/docs)
- [Getting Started Guide](https://positron.posit.co/start)

### R Resources
- [ggplot2 Documentation](https://ggplot2.tidyverse.org/)
- [dplyr Tutorial](https://dplyr.tidyverse.org/)
- [R for Data Science](https://r4ds.had.co.nz/)

### Python Resources
- [pandas Documentation](https://pandas.pydata.org/)
- [matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)

### Quarto
- [Quarto Documentation](https://quarto.org/docs/guide/)
- [Dashboard Examples](https://quarto.org/docs/dashboards/)

## 📄 License

This project is provided as-is for educational and practice purposes.

## 👤 Author

**Gloria Enjoy**
- GitHub: [@glorenjoy](https://github.com/glorenjoy)

---

**Built with ❤️ using Positron, R, Python, and Quarto**

*Last Updated: 2024*
