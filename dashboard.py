import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go


@st.cache_resource
def get_connection():
    """Connect to SQLite database"""
    return sqlite3.connect('sales_data.db')


@st.cache_data
def load_data(query):
    """Execute SQL query and return pandas DataFrame"""
    conn = get_connection()
    df = pd.read_sql(query, conn)
    return df


def revenue_by_country(region):
    """Chart 1: Revenue by Country"""
    if region == 'All Regions':
        query = """
        SELECT 
            dc.Country,
            dc.Region,
            SUM(f.`Total Revenue`) as Revenue,
            COUNT(*) as Orders
        FROM fact_sales f
        JOIN dim_country dc ON f.country_id = dc.country_id
        GROUP BY dc.Country, dc.Region
        ORDER BY Revenue DESC
        LIMIT 20
        """
    else:
        query = f"""
        SELECT 
            dc.Country,
            dc.Region,
            SUM(f.`Total Revenue`) as Revenue,
            COUNT(*) as Orders
        FROM fact_sales f
        JOIN dim_country dc ON f.country_id = dc.country_id
        WHERE dc.Region = '{region}'
        GROUP BY dc.Country, dc.Region
        ORDER BY Revenue DESC
        """
    df = load_data(query)
    
    fig = px.bar(
        df, 
        x='Country', 
        y='Revenue',
        title='Top 20 Countries by Revenue',
        labels={'Revenue': 'Total Revenue ($)', 'Country': 'Country'},
        color='Region',
        height=500
    )
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>')
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def profit_trend_over_time(region):
    """Chart 2: Monthly Profit Trend"""
    if region == 'All Regions':
        query = """
        SELECT 
            strftime('%Y-%m', `Order Date`) as Month,
            SUM(`Total Profit`) as Monthly_Profit
        FROM fact_sales
        GROUP BY strftime('%Y-%m', `Order Date`)
        ORDER BY Month
        """
    else:
        query = f"""
        SELECT 
            strftime('%Y-%m', f.`Order Date`) as Month,
            SUM(f.`Total Profit`) as Monthly_Profit
        FROM fact_sales f
        JOIN dim_country dc ON f.country_id = dc.country_id
        WHERE dc.Region = '{region}'
        GROUP BY strftime('%Y-%m', f.`Order Date`)
        ORDER BY Month
        """
    df = load_data(query)
    df['Month'] = pd.to_datetime(df['Month'])
    
    fig = px.line(
        df,
        x='Month',
        y='Monthly_Profit',
        title='Monthly Profit Trend',
        labels={'Monthly_Profit': 'Profit ($)', 'Month': 'Month'},
        height=500,
        markers=True
    )
    fig.update_traces(hovertemplate='<b>%{x|%B %Y}</b><br>Profit: $%{y:,.0f}<extra></extra>')
    fig.update_layout(hovermode='x unified')
    return fig


def product_performance(region):
    """Chart 3: Product Performance"""
    if region == 'All Regions':
        query = """
        SELECT 
            dp.`Item Type` as Product,
            COUNT(*) as Orders,
            SUM(f.`Total Revenue`) as Revenue,
            SUM(f.`Total Profit`) as Profit,
            ROUND(AVG(f.`Total Profit`), 2) as Avg_Profit_Per_Order
        FROM fact_sales f
        JOIN dim_product dp ON f.product_id = dp.product_id
        GROUP BY dp.`Item Type`
        ORDER BY Profit DESC
        """
    else:
        query = f"""
        SELECT 
            dp.`Item Type` as Product,
            COUNT(*) as Orders,
            SUM(f.`Total Revenue`) as Revenue,
            SUM(f.`Total Profit`) as Profit,
            ROUND(AVG(f.`Total Profit`), 2) as Avg_Profit_Per_Order
        FROM fact_sales f
        JOIN dim_product dp ON f.product_id = dp.product_id
        JOIN dim_country dc ON f.country_id = dc.country_id
        WHERE dc.Region = '{region}'
        GROUP BY dp.`Item Type`
        ORDER BY Profit DESC
        """
    df = load_data(query)
    
    fig = px.bar(
        df,
        x='Product',
        y='Profit',
        title='Total Profit by Product',
        labels={'Profit': 'Total Profit ($)', 'Product': 'Product Type'},
        color='Profit',
        color_continuous_scale='Viridis',
        height=500
    )
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>')
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def channel_comparison(region):
    """Chart 4: Sales Channel Comparison"""
    if region == 'All Regions':
        query = """
        SELECT 
            dc.`Sales Channel` as Channel,
            COUNT(*) as Orders,
            SUM(f.`Total Revenue`) as Revenue,
            SUM(f.`Total Profit`) as Profit,
            SUM(f.`Units Sold`) as Units,
            ROUND(AVG(f.`Total Profit`), 2) as Avg_Profit
        FROM fact_sales f
        JOIN dim_channel dc ON f.channel_id = dc.channel_id
        GROUP BY dc.`Sales Channel`
        """
    else:
        query = f"""
        SELECT 
            dc.`Sales Channel` as Channel,
            COUNT(*) as Orders,
            SUM(f.`Total Revenue`) as Revenue,
            SUM(f.`Total Profit`) as Profit,
            SUM(f.`Units Sold`) as Units,
            ROUND(AVG(f.`Total Profit`), 2) as Avg_Profit
        FROM fact_sales f
        JOIN dim_channel dc ON f.channel_id = dc.channel_id
        JOIN dim_country dco ON f.country_id = dco.country_id
        WHERE dco.Region = '{region}'
        GROUP BY dc.`Sales Channel`
        """
    df = load_data(query)
    
    fig = go.Figure(data=[
        go.Bar(name='Revenue', x=df['Channel'], y=df['Revenue'], 
               hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'),
        go.Bar(name='Profit', x=df['Channel'], y=df['Profit'],
               hovertemplate='<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>')
    ])
    
    fig.update_layout(
        title='Sales Channel: Revenue vs Profit',
        barmode='group',
        xaxis_title='Sales Channel',
        yaxis_title='Amount ($)',
        height=500
    )
    return fig


def main():
    """Main Streamlit app"""
    st.set_page_config(page_title='Sales Dashboard', layout='wide')
    
    st.title('Sales Data Analytics Dashboard')
    st.markdown('---')
    
    # Get available regions for filter
    regions_query = "SELECT DISTINCT Region FROM dim_country ORDER BY Region"
    regions_df = load_data(regions_query)
    all_regions = regions_df['Region'].tolist()
    
    # Add "All Regions" option
    region_options = ['All Regions'] + all_regions
    selected_region = st.selectbox('Filter by Region:', region_options)
    
    st.markdown('---')
    
    # Summary metrics
    if selected_region == 'All Regions':
        summary_query = """
            SELECT 
                COUNT(*) as Total_Orders,
                SUM(`Total Revenue`) as Total_Revenue,
                SUM(`Total Profit`) as Total_Profit,
                AVG(`Total Profit`) as Avg_Profit
            FROM fact_sales
        """
    else:
        summary_query = f"""
            SELECT 
                COUNT(*) as Total_Orders,
                SUM(f.`Total Revenue`) as Total_Revenue,
                SUM(f.`Total Profit`) as Total_Profit,
                AVG(f.`Total Profit`) as Avg_Profit
            FROM fact_sales f
            JOIN dim_country dc ON f.country_id = dc.country_id
            WHERE dc.Region = '{selected_region}'
        """
    
    summary = load_data(summary_query)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric('Total Orders', f"{summary['Total_Orders'][0]:,}")
    with col2:
        st.metric('Total Revenue', f"${summary['Total_Revenue'][0]:,.0f}")
    with col3:
        st.metric('Total Profit', f"${summary['Total_Profit'][0]:,.0f}")
    with col4:
        st.metric('Avg Profit/Order', f"${summary['Avg_Profit'][0]:,.0f}")
    
    st.markdown('---')
    
    # Charts
    st.header('Key Visualizations')
    
    # Chart 1
    st.subheader('1. Top Countries by Revenue')
    st.plotly_chart(revenue_by_country(selected_region), use_container_width=True)
    
    # Chart 2
    st.subheader('2. Profit Trend Over Time')
    st.plotly_chart(profit_trend_over_time(selected_region), use_container_width=True)
    
    # Chart 3
    st.subheader('3. Product Performance')
    st.plotly_chart(product_performance(selected_region), use_container_width=True)
    
    # Chart 4
    st.subheader('4. Sales Channel Comparison')
    st.plotly_chart(channel_comparison(selected_region), use_container_width=True)


if __name__ == '__main__':
    main()
