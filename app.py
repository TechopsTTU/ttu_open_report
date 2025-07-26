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
    st.set_page_config(page_title="Toyo Tanso USA Open Report", layout="wide")
    # Animated gradient background and fade-in effects
    st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #f5f7fa 0%, #c3cfe2 100%);
        animation: gradientMove 8s ease-in-out infinite alternate;
    }
    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }
    .fade-in {
        opacity: 0;
        animation: fadeIn 1.5s forwards;
    }
    @keyframes fadeIn {
        to { opacity: 1; }
    }
    .quick-link-btn {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.10);
        border: 1px solid #b0b0b0;
        padding: 0.8em 2.2em;
        margin: 0.7em;
        font-size: 1.15em;
        font-weight: 600;
        color: #222;
        transition: box-shadow 0.3s, transform 0.3s;
        position: relative;
        overflow: hidden;
    }
    .quick-link-btn:after {
        content: "";
        position: absolute;
        left: 0; top: 0;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, #e0eafc 0%, #cfdef3 100%);
        opacity: 0.1;
        transition: opacity 0.3s;
        z-index: 0;
    }
    .quick-link-btn:hover {
        box-shadow: 0 6px 24px rgba(34,34,34,0.18);
        border-color: #222;
        color: #222;
        transform: translateY(-2px) scale(1.04);
    }
    .quick-link-btn:hover:after {
        opacity: 0.25;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display logo with fade-in animation if available
    logo_path = Path("TTU_LOGO.jpg")
    if logo_path.exists():
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        st.image(str(logo_path), width=180)
        st.markdown('</div>', unsafe_allow_html=True)
        logging.info("Logo displayed.")
    else:
        logging.warning("Logo file TTU_LOGO.jpg not found.")

    # Main title and description with fade-in
    st.markdown('<h1 class="fade-in" style="margin-top:0;">Toyo Tanso USA Open Report Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<div class="fade-in" style="font-size:1.15em; margin-bottom:1em;">'
                'Welcome to the Toyo Tanso USA Open Report system.<br>'
                'We are a leading producer of graphite products for industrial applications.<br>'
                'Use the sidebar to navigate between tables, queries, reports, and forms.<br>'
                'This dashboard provides:<br>'
                '- Data extraction and preview<br>'
                '- Business queries and analytics<br>'
                '- Interactive reports and charts<br>'
                '- Data entry forms'
                '</div>', unsafe_allow_html=True)

    # Quick navigation links with animated buttons
    st.subheader("Quick Links")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<a href="/tables" class="quick-link-btn fade-in">Tables</a>', unsafe_allow_html=True)
    with col2:
        st.markdown('<a href="/queries" class="quick-link-btn fade-in">Queries</a>', unsafe_allow_html=True)
    with col3:
        st.markdown('<a href="/reports" class="quick-link-btn fade-in">Reports</a>', unsafe_allow_html=True)
    with col4:
        st.markdown('<a href="/forms" class="quick-link-btn fade-in">Forms</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
