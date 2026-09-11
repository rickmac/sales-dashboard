import pandas as pd


def load_cleaned_data(filename):
    """Load the cleaned sales data"""
    sales_data = pd.read_csv(filename)
    # Convert date columns back to datetime
    sales_data['Order Date'] = pd.to_datetime(sales_data['Order Date'])
    sales_data['Ship Date'] = pd.to_datetime(sales_data['Ship Date'])
    return sales_data


def create_dim_country(sales_data):
    """Extract unique Country/Region combinations"""
    dim_country = sales_data[['Country', 'Region']].drop_duplicates().reset_index(drop=True)
    dim_country.insert(0, 'country_id', range(1, len(dim_country) + 1))
    return dim_country


def create_dim_product(sales_data):
    """Extract unique Item Types"""
    dim_product = sales_data[['Item Type']].drop_duplicates().reset_index(drop=True)
    dim_product.insert(0, 'product_id', range(1, len(dim_product) + 1))
    return dim_product


def create_dim_channel(sales_data):
    """Extract unique Sales Channels"""
    dim_channel = sales_data[['Sales Channel']].drop_duplicates().reset_index(drop=True)
    dim_channel.insert(0, 'channel_id', range(1, len(dim_channel) + 1))
    return dim_channel


def create_fact_table(sales_data, dim_country, dim_product, dim_channel):
    """Create fact table with foreign keys to dims"""
    fact_sales = sales_data.copy()
    
    # Merge to get foreign keys
    fact_sales = fact_sales.merge(
        dim_country[['country_id', 'Country', 'Region']],
        on=['Country', 'Region'],
        how='left'
    )
    
    fact_sales = fact_sales.merge(
        dim_product[['product_id', 'Item Type']],
        on=['Item Type'],
        how='left'
    )
    
    fact_sales = fact_sales.merge(
        dim_channel[['channel_id', 'Sales Channel']],
        on=['Sales Channel'],
        how='left'
    )
    
    # Keep only necessary columns
    fact_sales = fact_sales[[
        'Order ID',
        'country_id',
        'product_id',
        'channel_id',
        'Order Priority',
        'Order Date',
        'Ship Date',
        'Units Sold',
        'Unit Price',
        'Unit Cost',
        'Total Revenue',
        'Total Cost',
        'Total Profit'
    ]]
    
    return fact_sales


def save_dims(dim_country, dim_product, dim_channel):
    """Save all dim tables to CSV"""
    dim_country.to_csv('dim_country.csv', index=False)
    dim_product.to_csv('dim_product.csv', index=False)
    dim_channel.to_csv('dim_channel.csv', index=False)
    print("dim tables saved:")
    print(f"  - dim_country.csv ({len(dim_country)} rows)")
    print(f"  - dim_product.csv ({len(dim_product)} rows)")
    print(f"  - dim_channel.csv ({len(dim_channel)} rows)")


def save_fact_table(fact_sales):
    """Save fact table to CSV"""
    fact_sales.to_csv('fact_sales.csv', index=False)
    print(f"Fact table saved: fact_sales.csv ({len(fact_sales)} rows)")


# Main
if __name__ == "__main__":
    # Load cleaned data
    sales_data = load_cleaned_data('cleaned_sales_data.csv')
    print(f"Loaded {len(sales_data)} rows of cleaned data\n")
    
    # Create dims
    dim_country = create_dim_country(sales_data)
    dim_product = create_dim_product(sales_data)
    dim_channel = create_dim_channel(sales_data)
    
    print("dims created:")
    print(f"  - Countries: {len(dim_country)}")
    print(f"  - Products: {len(dim_product)}")
    print(f"  - Channels: {len(dim_channel)}\n")
    
    # Create fact table
    fact_sales = create_fact_table(sales_data, dim_country, dim_product, dim_channel)
    
    # Save all tables
    save_dims(dim_country, dim_product, dim_channel)
    save_fact_table(fact_sales)
    
    print("\nNormalization complete!")
