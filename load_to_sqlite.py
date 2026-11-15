import pandas as pd
import sqlite3


def load_to_sqlite():
    """Load normalized CSV files into SQLite database"""
    
    # Connect to SQLite (creates database if it doesn't exist)
    conn = sqlite3.connect('sales_data.db')
    cursor = conn.cursor()
    
    # Drop existing tables if they exist (for fresh load)
    cursor.execute('DROP TABLE IF EXISTS fact_sales')
    cursor.execute('DROP TABLE IF EXISTS dim_country')
    cursor.execute('DROP TABLE IF EXISTS dim_product')
    cursor.execute('DROP TABLE IF EXISTS dim_channel')
    conn.commit()
    
    # Load dimension tables
    dim_country = pd.read_csv('dim_country.csv')
    dim_product = pd.read_csv('dim_product.csv')
    dim_channel = pd.read_csv('dim_channel.csv')
    
    # Load fact table
    fact_sales = pd.read_csv('fact_sales.csv')
    
    # Convert date columns to datetime
    fact_sales['Order Date'] = pd.to_datetime(fact_sales['Order Date'])
    fact_sales['Ship Date'] = pd.to_datetime(fact_sales['Ship Date'])
    
    # Write tables to SQLite
    dim_country.to_sql('dim_country', conn, index=False, if_exists='replace')
    dim_product.to_sql('dim_product', conn, index=False, if_exists='replace')
    dim_channel.to_sql('dim_channel', conn, index=False, if_exists='replace')
    fact_sales.to_sql('fact_sales', conn, index=False, if_exists='replace')
    
    # Create indexes for faster queries
    cursor.execute('CREATE INDEX idx_fact_country ON fact_sales(country_id)')
    cursor.execute('CREATE INDEX idx_fact_product ON fact_sales(product_id)')
    cursor.execute('CREATE INDEX idx_fact_channel ON fact_sales(channel_id)')
    conn.commit()
    
    # Verify the load
    print("Tables loaded to sales_data.db:\n")
    
    expected_counts = {
        'dim_country': len(dim_country),
        'dim_product': len(dim_product),
        'dim_channel': len(dim_channel),
        'fact_sales': len(fact_sales),
    }
    problems = []
    for table_name in ['dim_country', 'dim_product', 'dim_channel', 'fact_sales']:
        count = pd.read_sql(f'SELECT COUNT(*) as count FROM {table_name}', conn)
        actual = int(count['count'][0])
        print(f"  {table_name}: {actual:,} rows")
        if actual != expected_counts[table_name]:
            problems.append(f"{table_name} has {actual} rows, CSV has {expected_counts[table_name]}")

    # Every fact row must point to a row in each dimension
    for key, dim_table in [('country_id', 'dim_country'), ('product_id', 'dim_product'), ('channel_id', 'dim_channel')]:
        orphans = pd.read_sql(
            f'SELECT COUNT(*) as count FROM fact_sales WHERE {key} NOT IN (SELECT {key} FROM {dim_table})',
            conn,
        )
        orphan_count = int(orphans['count'][0])
        if orphan_count > 0:
            problems.append(f"{orphan_count} fact rows have a {key} with no row in {dim_table}")

    if problems:
        conn.close()
        raise ValueError("Database load failed checks: " + "; ".join(problems))
    
    # Show schema
    print("\nDatabase schema:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f'PRAGMA table_info({table_name})')
        columns = cursor.fetchall()
        print(f"\n  {table_name}:")
        for col in columns:
            print(f"    - {col[1]} ({col[2]})")
    
    conn.close()
    print("\nDatabase ready for Streamlit dashboard!")


if __name__ == "__main__":
    load_to_sqlite()
