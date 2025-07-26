import streamlit as st
import pandas as pd
from models.query_definitions import (
    q010_open_order_report_data,
    q093_shipment_status,
    # import other query funcs as you implement them
)

st.title("Queries")

queries = {
    "Open Order Report": q010_open_order_report_data,
    "Shipment Status": q093_shipment_status,
}

choice = st.selectbox("Choose a query", list(queries.keys()))
if choice:
    func = queries[choice]
    try:
        df = func()
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Query failed: {e}")
