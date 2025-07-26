import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.title("Tables")

# 1. load schema.json
schema_path = Path("schema.json")
if not schema_path.exists():
    st.error("schema.json not found. Run extract.py first.")
    st.stop()

with schema_path.open() as f:
    schema = json.load(f)

table_names = sorted(schema.keys())
if not table_names:
    st.warning("No tables found in schema.json")
    st.stop()

selected = st.selectbox("Choose a table", table_names)

# 2. show the DataFrame from cache/raw
csv_path = Path("cache") / "raw" / f"{selected}.csv"
if csv_path.exists():
    df = pd.read_csv(csv_path)
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "Download as CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name=f"{selected}.csv",
        mime="text/csv",
    )
else:
    st.error(f"No exported file at {csv_path}")
