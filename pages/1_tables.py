import json
from pathlib import Path
import pandas as pd
import streamlit as st
import numpy as np
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import time

st.set_page_config(page_title="GraphiteVision Analytics - Tables", layout="wide")

# Logo in upper right
logo_path = Path("TTU_LOGO.jpg")
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
csv_path = Path("cache") / "raw" / f"{table_selected}.csv"
if csv_path.exists():
    df = pd.read_csv(csv_path)
else:
    # Generate mock data if CSV is missing
    np.random.seed(42)
    col_names = [col["name"] for col in columns]
    df = pd.DataFrame({
        name: np.random.choice([f"Sample {name} {i}" for i in range(1, 21)], 20)
        for name in col_names
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

@classmethod
def setUpClass(cls):
    service = Service("C:/edgedriver_win64/msedgedriver.exe")
    cls.driver = webdriver.Edge(service=service)
    cls.driver.get("http://localhost:8501")
    time.sleep(3)
