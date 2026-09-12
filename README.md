# Sales Analytics Dashboard

A professional data analytics portfolio project demonstrating end-to-end data pipeline development, dimensional data modeling, and interactive visualization.

## Live Dashboard

**[View the Dashboard](https://sales-dashboard-6v6zofutvawhbm99jfon82.streamlit.app/)**

## Project Overview

This project showcases a complete data workflow:
- **Data Cleaning**: Validated 50,000 sales records, checking for duplicates, data integrity, and calculation accuracy
- **Data Normalization**: Designed and implemented a star schema with separate dimension and fact tables
- **Data Visualization**: Built an interactive dashboard with 4 key business insights
- **Deployment**: Deployed to Streamlit Cloud for live access

## Data Architecture

### Star Schema Design

```
         dim_country
              |
         dim_product
              |
    fact_sales (center)
              |
         dim_channel
```

**Dimension Tables:**
- `dim_country.csv` - 185 unique country/region combinations
- `dim_product.csv` - 12 product types
- `dim_channel.csv` - 2 sales channels (Online/Offline)

**Fact Table:**
- `fact_sales.csv` - 50,000 sales transactions with foreign keys to dimensions

## Data Quality

All cleaned data passed validation checks:
- ✓ 0 duplicate Order IDs
- ✓ 0 profit calculation errors
- ✓ 0 invalid shipping dates (Ship Date >= Order Date)
- ✓ All 14 columns with correct data types

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

- **Python**: Data processing and scripting
- **pandas**: Data manipulation and validation
- **SQLite**: Database for dimensional model
- **Streamlit**: Interactive web dashboard
- **Plotly**: Interactive visualizations
- **Git & GitHub**: Version control

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

# 3. Load into SQLite (optional - currently using CSVs for Streamlit Cloud)
python load_to_sqlite.py
```

## Key Insights

- **Geographic Diversity**: Sales span 185 countries across 6 regions
- **Product Mix**: 12 product types with varying profitability
- **Channel Strategy**: Both Online and Offline channels contribute significantly
- **Seasonal Patterns**: Monthly profit trends show consistent performance

## Future Enhancements

- Migrate to SQLite backend for improved query performance
- Add interactive filters for country, product, and time period selection
- Implement forecasting models for profit prediction
- Add drill-down capabilities for detailed transaction analysis
- Deploy additional dimension tables for customer and supplier data

## Contact & Portfolio

- **GitHub**: https://github.com/rickmac/sales-dashboard
- **Medium Articles**: https://medium.com/@ricky-mcbride
- **Dashboard**: https://sales-dashboard-6v6zofutvawhbm99jfon82.streamlit.app/

---

*Data portfolio project demonstrating modern data engineering and analytics skills for the Harris County Public Defender's Office Data Specialist position.*
