import streamlit as st
import polars as pl
import sqlite3
import plotly.express as px
import plotly.graph_objects as go


@st.cache_resource
def get_connection():
    """Connect to SQLite database"""
    return sqlite3.connect('sales_data.db')


@st.cache_data
def load_data_from_db(query):
    """Execute SQL query and return polars DataFrame"""
    conn = get_connection()
    df = pl.read_database(query, connection=conn, infer_schema_length=50000)
    return df


def revenue_by_country():
    """Chart 1: Revenue by Country"""
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
    df = load_data_from_db(query)
    df_pandas = df.to_pandas()
    
    fig = px.bar(
        df_pandas, 
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


def profit_trend_over_time():
    """Chart 2: Monthly Profit Trend"""
    query = """
    SELECT 
        strftime('%Y-%m', `Order Date`) as Month,
        SUM(`Total Profit`) as Monthly_Profit
    FROM fact_sales
    GROUP BY strftime('%Y-%m', `Order Date`)
    ORDER BY Month
    """
    df = load_data_from_db(query)
    df_pandas = df.to_pandas()
    df_pandas['Month'] = pl.Series(df_pandas['Month']).str.to_date().to_pandas()
    
    fig = px.line(
        df_pandas,
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


def product_performance():
    """Chart 3: Product Performance"""
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
    df = load_data_from_db(query)
    df_pandas = df.to_pandas()
    
    fig = px.bar(
        df_pandas,
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


def channel_comparison():
    """Chart 4: Sales Channel Comparison"""
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
    df = load_data_from_db(query)
    df_pandas = df.to_pandas()
    
    fig = go.Figure(data=[
        go.Bar(name='Revenue', x=df_pandas['Channel'], y=df_pandas['Revenue'], 
               hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'),
        go.Bar(name='Profit', x=df_pandas['Channel'], y=df_pandas['Profit'],
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
    
    # Summary metrics
    conn = get_connection()
    summary_query = """
        SELECT 
            COUNT(*) as Total_Orders,
            SUM(`Total Revenue`) as Total_Revenue,
            SUM(`Total Profit`) as Total_Profit,
            AVG(`Total Profit`) as Avg_Profit
        FROM fact_sales
    """
    summary = pl.read_database(summary_query, connection=conn).to_pandas()
    
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
    st.plotly_chart(revenue_by_country(), use_container_width=True)
    
    # Chart 2
    st.subheader('2. Profit Trend Over Time')
    st.plotly_chart(profit_trend_over_time(), use_container_width=True)
    
    # Chart 3
    st.subheader('3. Product Performance')
    st.plotly_chart(product_performance(), use_container_width=True)
    
    # Chart 4
    st.subheader('4. Sales Channel Comparison')
    st.plotly_chart(channel_comparison(), use_container_width=True)


if __name__ == '__main__':
    main()
