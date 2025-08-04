import json
from pathlib import Path
import pandas as pd
import streamlit as st
import numpy as np
import time

st.set_page_config(page_title="GraphiteVision Analytics - Tables", layout="wide")

# Logo in upper right
logo_path = Path("static/TTU_LOGO.jpg")
if logo_path.exists():
    col1, col2 = st.columns([6, 1])
    with col2:
        st.image(str(logo_path), width=120)

st.title("Data Tables")
st.markdown("""
Welcome to GraphiteVision Analytics. Select a table below to preview its schema and data. Use the search box to filter results. Download any table as CSV for further analysis.
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

table_names = sorted(schema.keys())
if not table_names:
    st.warning("schema.json is empty. No tables to display.")
    st.stop()

st.subheader("Select a Table")
table_selected = st.radio("Select a table:", table_names, horizontal=True)

# Show schema details for selected table
columns = schema[table_selected]
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
    # Try to get data from database first
    import sqlite3
    try:
        conn = sqlite3.connect("graphite_analytics.db")
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
st.dataframe(df, use_container_width=True)
st.download_button(
    "Download as CSV",
    df.to_csv(index=False).encode("utf-8"),
    file_name=f"{table_selected}.csv",
    mime="text/csv",
)

