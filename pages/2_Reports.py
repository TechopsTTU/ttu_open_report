"""
Reports Hub Page
Main hub for accessing all available reports in the GraphiteVision Analytics platform.
"""
import streamlit as st
from pathlib import Path

# Logo in upper right
logo_path = Path("static/TTU_LOGO.jpg")
if logo_path.exists():
    col1, col2 = st.columns([6, 1])
    with col2:
        st.image(str(logo_path), width=120)

st.title("Reports Hub")
st.markdown("""
Welcome to the GraphiteVision Analytics Reports Hub. Select from the available reports below to access detailed business intelligence and operational data.
""")

# Reports navigation
st.subheader("Available Reports")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Open Order Report", use_container_width=True):
        st.switch_page("5_open_order_report.py")
    
    st.markdown("View all open and processing orders with customer details and delivery dates.")

with col2:
    if st.button("📈 Interactive Reports", use_container_width=True):
        st.switch_page("3_reports.py")
    
    st.markdown("Interactive charts and visualizations for business data analysis.")

st.markdown("---")

# Quick access section
st.subheader("Quick Access")
st.markdown("""
- **Open Order Report**: Real-time view of all active orders and their status
- **Interactive Reports**: Visual analytics with charts and graphs
- **More reports coming soon**: Additional business intelligence features in development
""")