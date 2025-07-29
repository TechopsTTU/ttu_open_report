import streamlit as st
from datetime import date
from pathlib import Path
from models.query_definitions import get_open_orders_report

# Logo in upper right
logo_path = Path("TTU_LOGO.jpg")
if logo_path.exists():
    col1, col2 = st.columns([6, 1])
    with col2:
        st.image(str(logo_path), width=120)

st.title("Open Order Report")

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
    # Only use date range for get_open_orders_report; other filters not implemented
    df = get_open_orders_report(
        start_date=start_date.isoformat() if isinstance(start_date, date) else '2025-01-01',
        end_date=end_date.isoformat() if isinstance(end_date, date) else '2025-12-31'
    )
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="open_order_report.csv",
            mime="text/csv",
        )
    else:
        st.warning("No open orders found for the selected criteria.")
