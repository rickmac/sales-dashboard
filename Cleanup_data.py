import pandas as pd

def load_data(filename):	
	df = pd.read_csv(filename)
	return df

def convert_dates(sales_data):
    """Convert Order Date and Ship Date to datetime format"""
    sales_data['Order Date'] = pd.to_datetime(sales_data['Order Date'])
    sales_data['Ship Date'] = pd.to_datetime(sales_data['Ship Date'])
    return sales_data

def check_duplicates(sales_data):
    """Check for duplicate Order IDs"""
    duplicates = sales_data[sales_data.duplicated(subset=['Order ID'], keep=False)]
    print(f"Total duplicate Order IDs found: {len(duplicates)}")
    if len(duplicates) > 0:
        print(duplicates)
    return sales_data

def validate_profit(sales_data):
    """Check if Total Profit ≈ Total Revenue - Total Cost (within tolerance)"""
    expected_profit = sales_data['Total Revenue'] - sales_data['Total Cost']
    profit_mismatch = sales_data[abs(sales_data['Total Profit'] - expected_profit) > 0.01]

    print(f"Profit calculation errors found: {len(profit_mismatch)}")
    if len(profit_mismatch) > 0:
        print(profit_mismatch)

    return sales_data

def validate_shipping_dates(sales_data):
    """Check that Ship Date is after or equal to Order Date"""
    invalid_dates = sales_data[sales_data['Ship Date'] < sales_data['Order Date']]

    print(f"Invalid shipping dates found (Ship < Order): {len(invalid_dates)}")
    if len(invalid_dates) > 0:
        print(invalid_dates[['Order Date', 'Ship Date', 'Order ID']])

    return sales_data

def save_cleaned_data(sales_data, filename):
    """Save cleaned data to CSV"""
    sales_data.to_csv(filename, index=False)
    print(f"Cleaned data saved to {filename}")
    return sales_data    

# Main
if __name__ == "__main__":
    sales_data = load_data('FiftyThousand_recs.csv')
    sales_data = convert_dates(sales_data)
    #print(sales_data.info())  
    sales_data = check_duplicates(sales_data)
    sales_data = validate_profit(sales_data)  
    sales_data = validate_shipping_dates(sales_data)
    sales_data = save_cleaned_data(sales_data, 'cleaned_sales_data.csv')
    print(sales_data.info())

