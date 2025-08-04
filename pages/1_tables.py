import json
from pathlib import Path
import pandas as pd
import streamlit as st
import numpy as np
import time
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path for imports
sys.path.append('src')
from models.query_definitions import run_query
from models.table_mapping import get_database_type
from utils.currency_formatter import display_currency_dataframe

st.set_page_config(page_title="GraphiteVision Analytics - Tables", layout="wide")

# Logo in upper right
logo_path = Path("static/TTU_LOGO.jpg")
if logo_path.exists():
    col1, col2 = st.columns([6, 1])
    with col2:
        st.image(str(logo_path), width=120)

st.title("Data Tables")

# Show which database environment we're using
db_type = get_database_type()
if db_type == 'pervasive':
    st.success("🔗 Connected to PRODUCTION Pervasive database")
    st.info("📊 Showing production tables: OEHDR (Orders), OELIN (Order Lines), ARCUST (Customers)")
else:
    st.info("🔗 Connected to DEVELOPMENT SQLite database")

st.markdown("""
Welcome to GraphiteVision Analytics. Select a table below to preview its data. Use the search box to filter results. Download any table as CSV for further analysis.
""")

# 1. load schema.json
schema_path = Path("schema.json")
if not schema_path.exists():
    st.error("schema.json not found. Run extract.py first.")
    st.stop()

try:
    schema = json.loads(schema_path.read_text())
except json.JSONDecodeError:
    st.error("schema.json is not valid JSON. Please rerun extract.py.")
    st.stop()

# Get table names based on database type
db_type = get_database_type()
if db_type == 'pervasive':
    # Production tables
    table_names = ["OEHDR (Orders)", "OELIN (Order Lines)", "ARCUST (Customers)"]
else:
    # Development tables from schema
    table_names = sorted(schema.keys())
    if not table_names:
        st.warning("schema.json is empty. No tables to display.")
        st.stop()

st.subheader("Select a Table")
table_selected = st.radio("Select a table:", table_names, horizontal=True)

# Show schema details for selected table (controlled by environment variable)
if db_type != 'pervasive':
    columns = schema[table_selected]
show_schema = os.getenv("SHOW_SCHEMA_TABLES", "false").lower() == "true"

if show_schema:
    st.subheader("Schema")
    # When displaying schema, handle missing 'nullable' key gracefully
    schema_table = []
    for col in columns:
        if isinstance(col, dict):
            schema_table.append({
                "Column": col.get("name", "N/A"),
                "Type": col.get("type", "N/A"),
                "Nullable": col.get("nullable", "N/A")
            })
        else:
            # Optionally log or display a warning for malformed schema entry
            pass
    st.table(schema_table)

# Data preview and search/filter
csv_path = Path("resources") / "cache" / "raw" / f"{table_selected}.csv"
if csv_path.exists():
    df = pd.read_csv(csv_path)
else:
    # Get data from database based on environment
    try:
        if db_type == 'pervasive':
            # Production Pervasive queries
            if table_selected == "OEHDR (Orders)":
                query = "SELECT TOP 100 Ordernumber, Customername, Orderdate, Orderstatus FROM OEHDR"
            elif table_selected == "OELIN (Order Lines)":
                query = "SELECT TOP 100 Ordernumber, Itemkey, Itemdescription, Qtyordered, Unitprice FROM OELIN WHERE Itemkey IS NOT NULL"
            elif table_selected == "ARCUST (Customers)":
                query = "SELECT TOP 100 Customerkey, Customername, Customercity, Customerstate FROM ARCUST"
            else:
                query = "SELECT TOP 10 'No data' as Message"
            
            df = run_query(query)
        else:
            # SQLite database
            import sqlite3
            conn = sqlite3.connect("graphite_analytics.db")
            try:
                # Check if the table exists in our database
                if table_selected in ["Customers", "Products", "Orders", "OrderDetails", "Shipments"]:
                    df = pd.read_sql(f"SELECT * FROM {table_selected} LIMIT 100", conn)
                else:
                    # Generate realistic mock data based on table name
                    np.random.seed(42)
                    col_names = [col["name"] for col in columns]
                    
                    if "customer" in table_selected.lower():
                        # Customer-like data
                        df = pd.DataFrame({
                            "CustomerID": [f"CUST{i:03d}" for i in range(1, 21)],
                            "CustomerName": [f"Industrial Corp {i}" for i in range(1, 21)],
                            "ContactPerson": [f"Manager {i}" for i in range(1, 21)],
                            "Email": [f"manager{i}@company.com" for i in range(1, 21)],
                            "Phone": [f"555-{1000+i:04d}" for i in range(1, 21)]
                        })
                    elif "product" in table_selected.lower():
                        # Product-like data
                        df = pd.DataFrame({
                            "ProductID": [f"PART{i:03d}" for i in range(1, 21)],
                            "ProductName": [f"Graphite Component {chr(65+i%26)}" for i in range(1, 21)],
                            "Description": [f"High-quality industrial component for manufacturing" for i in range(1, 21)],
                            "Category": np.random.choice(["Graphite", "Carbon", "Heat Shield", "Conductive"], 20),
                            "UnitPrice": np.random.uniform(500, 5000, 20).round(2)
                        })
                    elif "order" in table_selected.lower():
                        # Order-like data
                        df = pd.DataFrame({
                            "OrderID": [f"ORD{31000+i}" for i in range(1, 21)],
                            "CustomerID": [f"CUST{i%10:03d}" for i in range(1, 21)],
                            "OrderDate": pd.date_range("2023-01-01", periods=20, freq="D").strftime('%Y-%m-%d'),
                            "Status": np.random.choice(["Open", "Processing", "Shipped", "Delivered"], 20),
                            "TotalAmount": np.random.uniform(1000, 50000, 20).round(2)
                        })
                    else:
                        # Generic data
                        df = pd.DataFrame({
                            name: np.random.choice([f"Sample {name} {i}" for i in range(1, 21)], 20)
                            for name in col_names[:5]  # Limit to 5 columns for display
                        })
            finally:
                conn.close()
    except Exception as e:
        # Fallback to original mock data
        np.random.seed(42)
        col_names = [col["name"] for col in columns]
        df = pd.DataFrame({
            name: np.random.choice([f"Sample {name} {i}" for i in range(1, 21)], 20)
            for name in col_names[:5]  # Limit to 5 columns for display
        })

search = st.text_input("Search table (case-insensitive)")
if search:
    df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
st.markdown("### Preview")
# Format currency columns before display
formatted_df = display_currency_dataframe(df)
st.dataframe(formatted_df, use_container_width=True)
st.download_button(
    "Download as CSV",
    df.to_csv(index=False).encode("utf-8"),
    file_name=f"{table_selected}.csv",
    mime="text/csv",
)

