#!/usr/bin/env python3
"""
Page for generating an Open Order Report.

This page allows users to select a date range and generate a report of open orders,
replicating the functionality from the original Access database.
"""

import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(page_title="Open Order Report", layout="wide")

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    db_path = Path("graphite_analytics.db")
    if not db_path.exists():
        st.error(f"Database not found at {db_path}. Please run the data migration script.")
        return None
    try:
        conn = sqlite3.connect(str(db_path))
        return conn
    except sqlite3.Error as e:
        st.error(f"Database connection error: {e}")
        return None

def fetch_open_orders(conn, start_date, end_date):
    """
    Fetches open order data from the database within the specified date range.
    """
    query = """
    SELECT
        o.OrderID,
        o.OrderDate,
        c.CustomerName,
        o.CustomerPO,
        p.ProductID,
        p.ProductName,
        od.Quantity,
        od.UnitPrice,
        od.TotalCost,
        o.Status,
        o.DeliveryDate,
        s.SalespersonName
    FROM Orders o
    JOIN Customers c ON o.CustomerID = c.CustomerID
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    JOIN Products p ON od.ProductID = p.ProductID
    LEFT JOIN Salespersons s ON o.SalespersonKey = s.SalespersonID
    WHERE o.OrderDate BETWEEN ? AND ?
    AND o.Status = 'O'
    ORDER BY o.OrderDate, o.OrderID;
    """
    try:
        df = pd.read_sql_query(query, conn, params=(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        return df
    except Exception as e:
        st.error(f"Failed to fetch open orders: {e}")
        return pd.DataFrame()

def main():
    """Main function to render the Open Order Report page."""
    st.title("📄 Open Order Report Generator")
    st.markdown("Select a date range below to generate a report of all open orders.")

    conn = get_db_connection()
    if not conn:
        st.stop()

    # --- UI for Date Selection ---
    st.sidebar.header("Report Filters")
    
    # Default dates: start of the year to today
    today = datetime.now()
    start_of_year = today.replace(month=1, day=1)

    start_date = st.sidebar.date_input(
        "Start Date",
        value=start_of_year,
        help="Select the start date for the report."
    )
    
    end_date = st.sidebar.date_input(
        "End Date",
        value=today,
        help="Select the end date for the report."
    )

    if start_date > end_date:
        st.sidebar.error("Error: Start date cannot be after end date.")
        st.stop()

    # --- Generate Report Button ---
    if st.sidebar.button("🚀 Generate Report", type="primary"):
        with st.spinner("🔍 Fetching open orders..."):
            report_df = fetch_open_orders(conn, start_date, end_date)

        st.success(f"**Report Generated for {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}**")
        
        if not report_df.empty:
            st.info(f"Found **{len(report_df)}** open order line items.")
            
            # --- Display Report Data ---
            st.dataframe(
                report_df,
                use_container_width=True,
                column_config={
                    "OrderID": st.column_config.TextColumn("Order ID"),
                    "OrderDate": st.column_config.DateColumn("Order Date", format="YYYY-MM-DD"),
                    "CustomerName": st.column_config.TextColumn("Customer"),
                    "CustomerPO": st.column_config.TextColumn("Customer PO"),
                    "ProductID": st.column_config.TextColumn("Product ID"),
                    "ProductName": st.column_config.TextColumn("Product Name"),
                    "Quantity": st.column_config.NumberColumn("Quantity", format="%.2f"),
                    "UnitPrice": st.column_config.NumberColumn("Unit Price", format="$%.2f"),
                    "TotalCost": st.column_config.NumberColumn("Total Cost", format="$%.2f"),
                    "Status": st.column_config.TextColumn("Status"),
                    "DeliveryDate": st.column_config.DateColumn("Est. Delivery", format="YYYY-MM-DD"),
                    "SalespersonName": st.column_config.TextColumn("Salesperson"),
                }
            )

            # --- Download Button ---
            csv = report_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Report as CSV",
                data=csv,
                file_name=f"open_order_report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        else:
            st.warning("No open orders found for the selected date range.")

    conn.close()

if __name__ == "__main__":
    main()
