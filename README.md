# Sales Analytics Dashboard

I built a the whole pipeline from raw data to a live Streamlit dashboard.

## Live Dashboard

[View the Dashboard](https://sales-dashboard-6v6zofutvawhbm99jfon82.streamlit.app/)

## Background

I wrote two Medium articles in early 2022 on using SQLite and pandas to handle files larger than Excel's capacity and splitting up large csv files. This project takes that public file to transform from raw data to a live dashboard. I reduced the original dataset to 50,000 records to keep it manageable for Streamlit.

https://medium.com/@ricky-mcbride/python-using-sqlite-when-excels-limits-are-surpassed-73f98a6cf5bf?sk=c901ac877433eb5d2394726c4d47fca3

https://medium.com/@ricky-mcbride/python-splitting-up-a-large-csv-file-by-record-count-or-column-value-ab4c4daf1278?sk=18996d50723f374d77b495ee2bd9b7a4



## Project Overview

Here's what I built:
- Data Cleaning: Validated 50,000 sales records for duplicates, data integrity, and calculation accuracy
- Data Normalization: Designed a star schema with dimension and fact tables
- Data Visualization: Built an interactive dashboard with 4 charts
- Deployment: Got it live on Streamlit Cloud

## Data Architecture

### Star Schema Design

A star schema with one central fact table connected to three dimension tables:

Dimension Tables:
- `dim_country.csv` - 185 unique country/region combinations
- `dim_product.csv` - 12 product types
- `dim_channel.csv` - 2 sales channels (Online/Offline)

Fact Table:
- `fact_sales.csv` - 50,000 sales transactions with foreign keys to dimensions

## Data Validation

Ran validation checks on all 50,000 records. Found zero duplicates, zero profit errors, zero date issues, and all columns had the right data types.

## Dashboard Features

### 1. Revenue by Country
Top 20 countries ranked by total revenue, color-coded by region. Identifies geographic performance leaders.

### 2. Profit Trend Over Time
Monthly profit trajectory showing business performance patterns and seasonality.

### 3. Product Performance
Total profit by product type, highlighting which products drive profitability.

### 4. Sales Channel Comparison
Revenue vs. Profit comparison between Online and Offline channels, with detailed metrics.

## Tech Stack

- Python for data processing and scripting
- pandas for data manipulation and validation
- SQLite for the dimensional model and live queries
- Streamlit for the interactive web dashboard
- Plotly for interactive visualizations
- Git and GitHub for version control

## Project Files

| File | Purpose |
|------|---------|
| `Cleanup_data.py` | Data validation and cleaning script |
| `normalize_data.py` | Dimensional table extraction |
| `load_to_sqlite.py` | Load CSVs into SQLite database |
| `dashboard.py` | Streamlit dashboard application |
| `cleaned_sales_data.csv` | Validated source data (50,000 rows) |
| `dim_*.csv` | Dimension tables |
| `fact_sales.csv` | Fact table with foreign keys |

## Getting Started

### Local Setup

```bash
# Clone the repository
git clone https://github.com/rickmac/sales-dashboard.git
cd sales-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard.py
```

The dashboard will open at `http://localhost:8501`

### Data Pipeline

```bash
# 1. Clean and validate data
python Cleanup_data.py

# 2. Normalize into dimensional tables
python normalize_data.py

# 3. Load into SQLite
python load_to_sqlite.py
```

## Key Insights

- Geographic Diversity: Sales span 185 countries across 6 regions
- Product Mix: 12 product types with varying profitability
- Channel Strategy: Both Online and Offline channels contribute strongly
- Seasonal Patterns: Monthly profit trends show consistent performance

## Contact & Portfolio

- GitHub: https://github.com/rickmac/sales-dashboard
- Dashboard: https://sales-dashboard-6v6zofutvawhbm99jfon82.streamlit.app/
