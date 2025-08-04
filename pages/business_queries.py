"""
Business Queries Page
Specialized business intelligence queries for Toyo Tanso USA operations.
"""
import streamlit as st
import pandas as pd
import logging
from datetime import datetime, timedelta
from pathlib import Path
import sys
sys.path.append('src')
from models.query_definitions import get_db_connection, run_query

logging.basicConfig(level=logging.INFO)

# Business query definitions
business_queries = {
    "Customer Order Volume": """
        SELECT 
            c.CustomerName,
            COUNT(o.OrderID) AS TotalOrders,
            SUM(od.TotalCost) AS TotalOrderValue
        FROM 
            Orders o
        JOIN 
            Customers c ON o.CustomerID = c.CustomerID
        JOIN 
            OrderDetails od ON o.OrderID = od.OrderID
        WHERE 
            o.OrderDate BETWEEN ? AND ?
        GROUP BY 
            c.CustomerName
        ORDER BY 
            TotalOrderValue DESC
    """,
    
    "Product Performance": """
        SELECT 
            p.ProductID,
            p.ProductName,
            COUNT(od.OrderID) AS TimesOrdered,
            SUM(od.Quantity) AS TotalQuantity,
            SUM(od.TotalCost) AS TotalRevenue,
            AVG(od.UnitPrice) AS AveragePrice
        FROM 
            OrderDetails od
        JOIN 
            Products p ON od.ProductID = p.ProductID
        JOIN 
            Orders o ON od.OrderID = o.OrderID
        WHERE 
            o.OrderDate BETWEEN ? AND ?
        GROUP BY 
            p.ProductID, p.ProductName
        ORDER BY 
            TotalRevenue DESC
    """,
    
    "Order Status Summary": """
        SELECT 
            o.Status AS OrderStatus,
            COUNT(o.OrderID) AS OrderCount,
            SUM(od.TotalCost) AS TotalValue,
            MIN(o.OrderDate) AS EarliestOrder,
            MAX(o.OrderDate) AS LatestOrder
        FROM 
            Orders o
        JOIN 
            OrderDetails od ON o.OrderID = od.OrderID
        WHERE 
            o.OrderDate BETWEEN ? AND ?
        GROUP BY 
            o.Status
        ORDER BY 
            OrderCount DESC
    """
}

# Query descriptions
query_descriptions = {
    "Customer Order Volume": "Analyze customer order patterns with total order counts and revenue by customer.",
    "Product Performance": "Evaluate product performance by order frequency, quantity, and revenue.",
    "Order Status Summary": "Get a summary of orders by status with counts, total values, and date ranges."
}

def main():
    # Logo in upper right
    logo_path = Path("static/TTU_LOGO.jpg")
    if logo_path.exists():
        col1, col2 = st.columns([6, 1])
        with col2:
            st.image(str(logo_path), width=120)
    
    # Page title and description
    st.title("Business Intelligence Queries")
    st.markdown("""
    Advanced business intelligence queries for operational insight. Select a business query below and specify the date range to analyze.
    """)
    
    # Date range selector
    st.subheader("Select Date Range")
    col1, col2 = st.columns(2)
    
    # Default to last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    with col1:
        start_date = st.date_input("Start Date", value=start_date)
    with col2:
        end_date = st.date_input("End Date", value=end_date)
        
    if start_date > end_date:
        st.error("Error: Start date must be before end date")
        return
    
    # Query selection UI
    st.subheader("Select a Business Query")
    options = list(business_queries.keys())
    choice = st.radio("Select a query:", options, horizontal=True)
    
    if choice:
        st.info(query_descriptions.get(choice, ""))
        
        try:
            # Execute the selected query with date parameters
            query = business_queries[choice]
            with get_db_connection() as conn:
                df = pd.read_sql(query, conn, params=(start_date, end_date))
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                
                # Show summary stats
                st.subheader("Summary")
                st.write(f"Total records: {len(df)}")
                
                # Add visualization based on query type
                st.subheader("Visualization")
                if choice == "Customer Order Volume":
                    st.bar_chart(df.set_index('CustomerName')['TotalOrderValue'])
                elif choice == "Product Performance":
                    st.bar_chart(df.set_index('ProductName')['TotalRevenue'])
                elif choice == "Order Status Summary":
                    st.bar_chart(df.set_index('OrderStatus')['OrderCount'])
                
                # Download option
                st.download_button(
                    "Download Query Results",
                    df.to_csv(index=False).encode("utf-8"),
                    file_name=f"{choice.replace(' ', '_')}_{start_date}_to_{end_date}.csv",
                    mime="text/csv",
                )
            else:
                st.warning("No data available for this query in the selected date range.")
        except Exception as e:
            logging.error(f"Query execution failed: {e}")
            st.error(f"Failed to execute query: {str(e)}")
            st.warning("Make sure the database connection is properly configured.")

if __name__ == "__main__":
    main()