"""
TTU Open Report Streamlit App
Main dashboard for navigation and overview.
"""
import streamlit as st
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def main():
    # Set up page config and custom styles
    st.set_page_config(page_title="TTU Open Report", layout="wide")
    st.markdown("""
    <style>
    .quick-link-btn {
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        padding: 0.7em 2em;
        margin: 0.5em;
        font-size: 1.1em;
        font-weight: 500;
        color: #333;
        transition: box-shadow 0.2s;
    }
    .quick-link-btn:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.16);
        border-color: #0072B5;
        color: #0072B5;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display logo if available
    logo_path = Path("TTU_LOGO.jpg")
    if logo_path.exists():
        st.image(str(logo_path), width=180)
        logging.info("Logo displayed.")
    else:
        logging.warning("Logo file TTU_LOGO.jpg not found.")

    # Main title and description
    st.title("TTU Open Report Dashboard")
    st.markdown("""
    Welcome to the TTU Open Report system. Use the sidebar to navigate between tables, queries, reports, and forms. This dashboard provides:
    - Data extraction and preview
    - Business queries and analytics
    - Interactive reports and charts
    - Data entry forms
    """)

    # Quick navigation links
    st.subheader("Quick Links")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<a href="/tables" class="quick-link-btn">Tables</a>', unsafe_allow_html=True)
    with col2:
        st.markdown('<a href="/queries" class="quick-link-btn">Queries</a>', unsafe_allow_html=True)
    with col3:
        st.markdown('<a href="/reports" class="quick-link-btn">Reports</a>', unsafe_allow_html=True)
    with col4:
        st.markdown('<a href="/forms" class="quick-link-btn">Forms</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
