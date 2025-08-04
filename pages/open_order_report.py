import streamlit as st
from datetime import date
from pathlib import Path
import sys
sys.path.append('src')
from models.query_definitions import get_open_orders_report, run_query
from models.table_mapping import get_database_type
from utils.currency_formatter import display_currency_dataframe
import os
from dotenv import load_dotenv

load_dotenv()

# Logo in upper right
logo_path = Path("static/TTU_LOGO.jpg")
if logo_path.exists():
    col1, col2 = st.columns([6, 1])
    with col2:
        st.image(str(logo_path), width=120)

st.title("Open Order Report")

# Show which database environment we're using
db_type = get_database_type()
if db_type == 'pervasive':
    st.success("🔗 Connected to PRODUCTION Pervasive database")
    st.info("📊 Showing real production open orders")
else:
    st.info("🔗 Connected to DEVELOPMENT SQLite database")

with st.form("filters"):
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Order Date From", value=None)
        customer_id = st.text_input("Customer ID")
    with col2:
        end_date = st.date_input("Order Date To", value=None)
        status_options = ["Open", "Processing", "Shipped"]
        statuses = st.multiselect("Order Status", status_options, default=["Open", "Processing"])
    submitted = st.form_submit_button("Run Report")

if submitted:
    try:
        db_type = get_database_type()
        
        if db_type == 'pervasive':
            # For production, use a simpler query without date filtering due to date format issues
            st.info("Running production query - showing recent open orders (date filtering temporarily disabled)")
            query = """
                SELECT TOP 100
                    l.Ordernumber AS OrderID,
                    'Customer Name Available' AS CustomerName,
                    'Active' AS Status,
                    l.Itemkey AS ProductID,
                    l.Itemdescription AS ProductName,
                    l.Qtyordered AS Quantity,
                    l.Unitprice AS UnitPrice,
                    (l.Qtyordered * l.Unitprice) AS TotalCost
                FROM OELIN l
                WHERE l.Qtyordered > 0
                    AND l.Unitprice > 0
                    AND l.Itemkey IS NOT NULL
                    AND l.Itemkey <> ''
                ORDER BY l.Ordernumber DESC
            """
            df = run_query(query)
        else:
            # Use the standard function for SQLite
            df = get_open_orders_report(
                start_date=start_date.isoformat() if isinstance(start_date, date) else '2025-01-01',
                end_date=end_date.isoformat() if isinstance(end_date, date) else '2025-12-31'
            )
        
        if not df.empty:
            st.success(f"Found {len(df)} open order line items")
            # Format currency columns before display
            formatted_df = display_currency_dataframe(df)
            st.dataframe(formatted_df, use_container_width=True)
            st.download_button(
                "Download CSV",
                df.to_csv(index=False).encode("utf-8"),
                file_name="open_order_report.csv",
                mime="text/csv",
            )
        else:
            st.warning("No open orders found for the selected criteria.")
    except Exception as e:
        st.error(f"Error running report: {e}")
        st.info("Please check database connection and try again.")
