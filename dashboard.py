import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


@st.cache_data
def load_data():
    """Load data from CSVs"""
    fact_sales = pd.read_csv('fact_sales.csv')
    dim_country = pd.read_csv('dim_country.csv')
    dim_product = pd.read_csv('dim_product.csv')
    dim_channel = pd.read_csv('dim_channel.csv')
    
    # Convert dates
    fact_sales['Order Date'] = pd.to_datetime(fact_sales['Order Date'])
    fact_sales['Ship Date'] = pd.to_datetime(fact_sales['Ship Date'])
    
    return fact_sales, dim_country, dim_product, dim_channel


def revenue_by_country(fact_sales, dim_country):
    """Chart 1: Revenue by Country"""
    merged = fact_sales.merge(
        dim_country[['country_id', 'Country', 'Region']],
        on='country_id',
        how='left'
    )
    
    data = merged.groupby(['Country', 'Region']).agg({
        'Total Revenue': 'sum'
    }).reset_index().sort_values('Total Revenue', ascending=False).head(20)
    
    fig = px.bar(
        data, 
        x='Country', 
        y='Total Revenue',
        title='Top 20 Countries by Revenue',
        labels={'Total Revenue': 'Revenue ($)', 'Country': 'Country'},
        color='Region',
        height=500
    )
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>')
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def profit_trend_over_time(fact_sales):
    """Chart 2: Monthly Profit Trend"""
    fact_sales['Month'] = pd.to_datetime(fact_sales['Order Date']).dt.to_period('M')
    data = fact_sales.groupby('Month').agg({
        'Total Profit': 'sum'
    }).reset_index()
    data['Month'] = data['Month'].astype(str)
    data['Month'] = pd.to_datetime(data['Month'])
    data = data.sort_values('Month')
    
    fig = px.line(
        data,
        x='Month',
        y='Total Profit',
        title='Monthly Profit Trend',
        labels={'Total Profit': 'Profit ($)', 'Month': 'Month'},
        height=500,
        markers=True
    )
    fig.update_traces(hovertemplate='<b>%{x|%B %Y}</b><br>Profit: $%{y:,.0f}<extra></extra>')
    fig.update_layout(hovermode='x unified')
    return fig


def product_performance(fact_sales, dim_product):
    """Chart 3: Product Performance"""
    merged = fact_sales.merge(
        dim_product[['product_id', 'Item Type']],
        on='product_id',
        how='left'
    )
    
    data = merged.groupby('Item Type').agg({
        'Total Profit': 'sum'
    }).reset_index().sort_values('Total Profit', ascending=False)
    
    fig = px.bar(
        data,
        x='Item Type',
        y='Total Profit',
        title='Total Profit by Product',
        labels={'Total Profit': 'Profit ($)', 'Item Type': 'Product Type'},
        color='Total Profit',
        color_continuous_scale='Viridis',
        height=500
    )
    fig.update_traces(hovertemplate='<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>')
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def channel_comparison(fact_sales, dim_channel):
    """Chart 4: Sales Channel Comparison"""
    merged = fact_sales.merge(
        dim_channel[['channel_id', 'Sales Channel']],
        on='channel_id',
        how='left'
    )
    
    data = merged.groupby('Sales Channel').agg({
        'Total Revenue': 'sum',
        'Total Profit': 'sum'
    }).reset_index()
    
    fig = go.Figure(data=[
        go.Bar(name='Revenue', x=data['Sales Channel'], y=data['Total Revenue'], 
               hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'),
        go.Bar(name='Profit', x=data['Sales Channel'], y=data['Total Profit'],
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
    
    # Load data
    fact_sales, dim_country, dim_product, dim_channel = load_data()
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric('Total Orders', f"{len(fact_sales):,}")
    with col2:
        st.metric('Total Revenue', f"${fact_sales['Total Revenue'].sum():,.0f}")
    with col3:
        st.metric('Total Profit', f"${fact_sales['Total Profit'].sum():,.0f}")
    with col4:
        st.metric('Avg Profit/Order', f"${fact_sales['Total Profit'].mean():,.0f}")
    
    st.markdown('---')
    
    # Charts
    st.header('Key Visualizations')
    
    # Chart 1
    st.subheader('1. Top Countries by Revenue')
    st.plotly_chart(revenue_by_country(fact_sales, dim_country), use_container_width=True)
    
    # Chart 2
    st.subheader('2. Profit Trend Over Time')
    st.plotly_chart(profit_trend_over_time(fact_sales), use_container_width=True)
    
    # Chart 3
    st.subheader('3. Product Performance')
    st.plotly_chart(product_performance(fact_sales, dim_product), use_container_width=True)
    
    # Chart 4
    st.subheader('4. Sales Channel Comparison')
    st.plotly_chart(channel_comparison(fact_sales, dim_channel), use_container_width=True)


if __name__ == '__main__':
    main()
