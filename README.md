# Sales Analytics Dashboard

I built the whole pipeline from raw data to a live Streamlit dashboard.

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

Each pipeline step checks its output and stops with an error if a check fails, so bad data never reaches the database.

**Cleaning (`Cleanup_data.py`)**
- No duplicate Order IDs
- Total Profit equals Total Revenue minus Total Cost, within $0.01
- Ship Date is on or after Order Date

**Normalization (`normalize_data.py`)**
- The fact table has the same number of rows as the cleaned data
- Every fact row matches a row in each dimension table
- Dimension keys are unique
- Total revenue in the fact table matches the cleaned data

**Loading (`load_to_sqlite.py`)**
- Each table's row count matches its CSV file
- Every fact row matches a row in each dimension table

All 50,000 source records pass these checks.

## Dashboard Features

### Date Range Filter
A date picker in the sidebar sets the start and end date. The summary cards and all four charts update to show only orders in that range. The default range is 2010-01-01 to 2020-09-10, which covers the full dataset.

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

The 50,000-record source file (`FiftyThousand_recs.csv`) is not in this repository. The repository includes `cleaned_sales_data.csv`, which already passed the cleaning checks, so the pipeline can start from there:

```bash
# 1. Normalize into dimensional tables (reads cleaned_sales_data.csv)
python normalize_data.py

# 2. Load into SQLite (creates sales_data.db)
python load_to_sqlite.py
```

To rerun the cleaning step, place the 50,000-record source file at `FiftyThousand_recs.csv` in the project folder, then run `python Cleanup_data.py` before the steps above. That file is not in the repository.

## Key Insights

- Geographic Diversity: Sales span 185 countries across 6 regions
- Product Mix: 12 product types with varying profitability
- Channel Strategy: Both Online and Offline channels contribute strongly
- Seasonal Patterns: Monthly profit trends show consistent performance

## Contact & Portfolio

- GitHub: https://github.com/rickmac/sales-dashboard
- Dashboard: https://sales-dashboard-6v6zofutvawhbm99jfon82.streamlit.app/
