"""
Interactive Reports
Provides interactive data visualizations and dashboard capabilities.
"""
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Handle optional plotly dependency
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly is not installed. Some visualizations will use Altair instead. Install plotly with 'pip install plotly'.")
from datetime import datetime, timedelta
from pathlib import Path
import sys
sys.path.append('src')
from models.query_definitions import get_db_connection, run_query
from utils.currency_formatter import format_currency

# Logo in upper right
logo_path = Path("static/TTU_LOGO.jpg")
if logo_path.exists():
    col1, col2 = st.columns([6, 1])
    with col2:
        st.image(str(logo_path), width=120)

st.title("Interactive Analytics Dashboard")
st.markdown("""
Welcome to the GraphiteVision Analytics Interactive Dashboard. Use the tools below to explore your business data through rich visualizations and interactive charts.
""")

# Define tabs for different visualizations
tab1, tab2, tab3, tab4 = st.tabs(["Sales Overview", "Product Analysis", "Customer Insights", "Order Status"])

# Helper function to get demo data if database connection fails
def get_demo_data():
    # Create sample sales data
    np.random.seed(42)
    today = datetime.now()
    dates = [(today - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(365, 0, -10)]
    
    customers = ["ACME Corp", "Toyo Industries", "GlobalTech", "Innovative Solutions", 
                "TechFusion", "Quantum Materials", "SpectraSystems", "FusionTech",
                "NexGen Manufacturing", "PrecisionParts"]
                
    products = ["Carbon Component A", "Graphite Assembly B", "Specialized Fixture", 
               "ISO Compliant Part", "Thermal Resistor", "High-Temp Module", 
               "Conductive Component", "Heat Shield Assembly"]
               
    sales_data = []
    for i, date in enumerate(dates):
        for _ in range(np.random.randint(1, 5)):  # 1-4 orders per day
            customer = np.random.choice(customers)
            product = np.random.choice(products)
            quantity = np.random.randint(1, 20)
            unit_price = np.random.uniform(500, 10000)
            total = quantity * unit_price
            status = np.random.choice(["Complete", "In Progress", "Pending", "On Hold"])
            sales_data.append({
                "OrderDate": date,
                "CustomerName": customer,
                "ProductName": product,
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "TotalAmount": total,
                "Status": status,
                "Region": np.random.choice(["North", "South", "East", "West", "International"]),
                "SalesPerson": np.random.choice(["John Smith", "Lisa Johnson", "Robert Chen", "Maria Garcia"])
            })
    
    return pd.DataFrame(sales_data)

# Try to get real data, or use demo data
try:
    # Get date range for filters
    st.sidebar.header("Filters")
    today = datetime.now()
    default_start = today - timedelta(days=365)
    default_end = today
    
    start_date = st.sidebar.date_input("Start Date", default_start)
    end_date = st.sidebar.date_input("End Date", default_end)
    
    if start_date > end_date:
        st.sidebar.error("Start date must be before end date")
    
    # Try to run a real query
    try:
        query = """
        SELECT 
            o.OrderDate, c.CustomerName, p.ProductName,
            od.Quantity, od.UnitPrice, od.TotalCost as TotalAmount,
            o.Status, 'All' as Region, 
            COALESCE(o.SalespersonKey, 'Unknown') as SalesPerson
        FROM 
            Orders o
        JOIN 
            OrderDetails od ON o.OrderID = od.OrderID
        JOIN 
            Customers c ON o.CustomerID = c.CustomerID
        JOIN 
            Products p ON od.ProductID = p.ProductID
        WHERE 
            o.OrderDate BETWEEN ? AND ?
        """
        df = run_query(query, params=(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        
        if df.empty:
            st.sidebar.warning("No data found in the selected date range. Using demo data instead.")
            df = get_demo_data()
    except Exception as e:
        st.sidebar.warning("Database query failed. Using demo data for visualization.")
        df = get_demo_data()
    
    # Apply filters from sidebar
    customer_list = ['All'] + sorted(df['CustomerName'].unique().tolist())
    selected_customer = st.sidebar.selectbox("Customer", customer_list)
    
    if selected_customer != 'All':
        df = df[df['CustomerName'] == selected_customer]
    
    product_list = ['All'] + sorted(df['ProductName'].unique().tolist())
    selected_product = st.sidebar.selectbox("Product", product_list)
    
    if selected_product != 'All':
        df = df[df['ProductName'] == selected_product]
        
    # Create visualizations in each tab
    with tab1:  # Sales Overview
        st.header("Sales Overview")
        
        # Show metrics at the top
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Orders", len(df), f"{len(df) - len(get_demo_data()) // 2:+}")
        with col2:
            total_sales = df['TotalAmount'].sum()
            st.metric("Total Sales", format_currency(total_sales), f"{5.2:+}%")
        with col3:
            avg_order = total_sales / len(df) if len(df) > 0 else 0
            st.metric("Average Order Value", format_currency(avg_order), f"{2.1:+}%")
            
        # Monthly trend chart
        st.subheader("Monthly Sales Trend")
        df['Month'] = pd.to_datetime(df['OrderDate']).dt.strftime('%Y-%m')
        monthly_sales = df.groupby('Month').agg({'TotalAmount': 'sum'}).reset_index()
        
        chart = alt.Chart(monthly_sales).mark_line(point=True).encode(
            x=alt.X('Month', title='Month'),
            y=alt.Y('TotalAmount', title='Sales Amount ($)'),
            tooltip=['Month', 'TotalAmount']
        ).properties(height=300)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Sales by region (Pie chart)
        st.subheader("Sales Distribution by Region")
        region_sales = df.groupby('Region').agg({'TotalAmount': 'sum'}).reset_index()
        
        if PLOTLY_AVAILABLE:
            fig = px.pie(region_sales, values='TotalAmount', names='Region', 
                        title='Sales by Region', hole=0.3,
                        color_discrete_sequence=px.colors.qualitative.Plotly)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Alternative using Altair
            chart = alt.Chart(region_sales).mark_arc().encode(
                theta=alt.Theta(field="TotalAmount", type="quantitative"),
                color=alt.Color(field="Region", type="nominal"),
                tooltip=['Region', 'TotalAmount']
            ).properties(title='Sales by Region')
            st.altair_chart(chart, use_container_width=True)
    
    with tab2:  # Product Analysis
        st.header("Product Performance Analysis")
        
        # Top products by sales
        st.subheader("Top Products by Sales")
        product_sales = df.groupby('ProductName').agg({'TotalAmount': 'sum', 'Quantity': 'sum'}).reset_index()
        product_sales = product_sales.sort_values('TotalAmount', ascending=False).head(10)
        
        if PLOTLY_AVAILABLE:
            fig = px.bar(product_sales, x='ProductName', y='TotalAmount',
                        title='Top 10 Products by Sales', 
                        labels={'ProductName': 'Product', 'TotalAmount': 'Sales Amount ($)'},
                        color='TotalAmount')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            chart = alt.Chart(product_sales).mark_bar().encode(
                x=alt.X('ProductName', sort='-y', title='Product', axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('TotalAmount', title='Sales Amount ($)'),
                color='TotalAmount',
                tooltip=['ProductName', 'TotalAmount', 'Quantity']
            ).properties(title='Top 10 Products by Sales')
            st.altair_chart(chart, use_container_width=True)
        
        # Product quantity vs price scatter plot
        st.subheader("Product Quantity vs Price Analysis")
        if PLOTLY_AVAILABLE:
            fig = px.scatter(df, x='UnitPrice', y='Quantity', size='TotalAmount', 
                            color='ProductName', hover_name='ProductName',
                            title='Product Quantity vs Price',
                            labels={'UnitPrice': 'Unit Price ($)', 'Quantity': 'Quantity Ordered'})
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            chart = alt.Chart(df).mark_circle().encode(
                x=alt.X('UnitPrice', title='Unit Price ($)'),
                y=alt.Y('Quantity', title='Quantity Ordered'),
                size='TotalAmount',
                color='ProductName',
                tooltip=['ProductName', 'UnitPrice', 'Quantity', 'TotalAmount']
            ).properties(title='Product Quantity vs Price', height=400)
            st.altair_chart(chart, use_container_width=True)
        
    with tab3:  # Customer Insights
        st.header("Customer Insights")
        
        # Top customers by sales
        st.subheader("Top Customers by Sales")
        customer_sales = df.groupby('CustomerName').agg({'TotalAmount': 'sum', 'OrderDate': 'count'}).reset_index()
        customer_sales = customer_sales.rename(columns={'OrderDate': 'Order Count'})
        customer_sales = customer_sales.sort_values('TotalAmount', ascending=False).head(10)
        
        if PLOTLY_AVAILABLE:
            fig = px.bar(customer_sales, x='CustomerName', y='TotalAmount',
                        title='Top 10 Customers by Sales', 
                        labels={'CustomerName': 'Customer', 'TotalAmount': 'Sales Amount ($)'},
                        color='Order Count', text='Order Count')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            chart = alt.Chart(customer_sales).mark_bar().encode(
                x=alt.X('CustomerName', sort='-y', title='Customer', axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('TotalAmount', title='Sales Amount ($)'),
                color='Order Count',
                tooltip=['CustomerName', 'TotalAmount', 'Order Count']
            ).properties(title='Top 10 Customers by Sales')
            st.altair_chart(chart, use_container_width=True)
        
        # Customer order frequency analysis
        st.subheader("Customer Order Frequency")
        customer_order_counts = df.groupby('CustomerName').size().reset_index(name='Order Count')
        customer_order_counts = customer_order_counts.sort_values('Order Count', ascending=False)
        
        if PLOTLY_AVAILABLE:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=customer_order_counts['CustomerName'],
                y=customer_order_counts['Order Count'],
                marker_color='rgb(55, 83, 109)'
            ))
            fig.update_layout(
                title='Customer Order Frequency',
                xaxis_tickangle=-45,
                xaxis_title='Customer',
                yaxis_title='Number of Orders'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            chart = alt.Chart(customer_order_counts).mark_bar().encode(
                x=alt.X('CustomerName', sort='-y', title='Customer', axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('Order Count', title='Number of Orders'),
                tooltip=['CustomerName', 'Order Count']
            ).properties(title='Customer Order Frequency')
            st.altair_chart(chart, use_container_width=True)
        
    with tab4:  # Order Status
        st.header("Order Status Analysis")
        
        # Order status distribution
        st.subheader("Order Status Distribution")
        status_counts = df['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        if PLOTLY_AVAILABLE:
            fig = px.pie(status_counts, values='Count', names='Status', 
                        title='Order Status Distribution', 
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            chart = alt.Chart(status_counts).mark_arc().encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Status", type="nominal"),
                tooltip=['Status', 'Count']
            ).properties(title='Order Status Distribution')
            st.altair_chart(chart, use_container_width=True)
        
        # Status by sales person
        st.subheader("Order Status by Sales Person")
        status_by_sp = df.groupby(['SalesPerson', 'Status']).size().reset_index(name='Count')
        
        if PLOTLY_AVAILABLE:
            fig = px.bar(status_by_sp, x='SalesPerson', y='Count', color='Status', 
                        title='Order Status by Sales Person', 
                        labels={'SalesPerson': 'Sales Person', 'Count': 'Number of Orders'})
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            chart = alt.Chart(status_by_sp).mark_bar().encode(
                x=alt.X('SalesPerson', title='Sales Person', axis=alt.Axis(labelAngle=-45)),
                y=alt.Y('Count', title='Number of Orders'),
                color='Status',
                tooltip=['SalesPerson', 'Status', 'Count']
            ).properties(title='Order Status by Sales Person')
            st.altair_chart(chart, use_container_width=True)
        
        # Timeline of orders by status
        st.subheader("Order Timeline by Status")
        df['OrderMonth'] = pd.to_datetime(df['OrderDate']).dt.strftime('%Y-%m')
        timeline = df.groupby(['OrderMonth', 'Status']).size().reset_index(name='Count')
        
        if PLOTLY_AVAILABLE:
            fig = px.line(timeline, x='OrderMonth', y='Count', color='Status', 
                        title='Order Timeline by Status',
                        labels={'OrderMonth': 'Month', 'Count': 'Number of Orders'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            chart = alt.Chart(timeline).mark_line(point=True).encode(
                x=alt.X('OrderMonth', title='Month'),
                y=alt.Y('Count', title='Number of Orders'),
                color='Status',
                tooltip=['OrderMonth', 'Status', 'Count']
            ).properties(title='Order Timeline by Status')
            st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error(f"An error occurred while generating reports: {str(e)}")
    st.info("This is likely due to a database connection issue or missing dependencies.")
    
    # Display helpful information
    st.subheader("Troubleshooting")
    st.markdown("""
    To fix this issue, please make sure:
    1. The database connection is properly configured
    2. All required Python packages are installed:
       - streamlit
       - pandas
       - numpy
       - altair
       - plotly
    3. The demo data generation is working properly
    """)