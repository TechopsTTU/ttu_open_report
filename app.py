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
    st.set_page_config(page_title="GraphiteVision Analytics", layout="wide")
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
    .modern-nav-container {
        display: flex;
        justify-content: flex-end;
        gap: 15px;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    .modern-nav-container a {
        text-decoration: none;
    }
    .modern-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 25px;
        color: white;
        padding: 12px 28px;
        font-size: 16px;
        font-weight: 600;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .modern-btn:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .modern-btn:active {
        transform: translateY(-1px) scale(1.02);
    }
    .modern-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.2), transparent);
        transform: translateX(-100%);
        transition: transform 0.6s;
        border-radius: 25px;
    }
    .modern-btn:hover::before {
        transform: translateX(100%);
    }
    .app-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 20px 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .app-subtitle {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 300;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display logo with fade-in animation if available
    logo_path = Path("resources/static/TTU_LOGO.jpg")
    if logo_path.exists():
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        st.image(str(logo_path), width=180)
        st.markdown('</div>', unsafe_allow_html=True)
        logging.info("Logo displayed.")
    else:
        logging.warning("Logo file TTU_LOGO.jpg not found.")

    # Main title and description with fade-in
    st.markdown('<h1 class="app-title fade-in">GraphiteVision Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle fade-in">Advanced Data Analytics for Toyo Tanso USA</div>', unsafe_allow_html=True)
    st.markdown('<div class="fade-in" style="font-size:1.15em; margin-bottom:2em; text-align:center; color:#555;">'
                'Comprehensive business intelligence platform for graphite manufacturing operations.<br>'
                'Access real-time data, generate insights, and drive operational excellence.'
                '</div>', unsafe_allow_html=True)

    # Modern navigation buttons on the right
    st.markdown('''
    <div class="modern-nav-container fade-in">
        <a href="/tables" target="_self">
            <button class="modern-btn">
                📊 Data Tables
            </button>
        </a>
        <a href="/queries" target="_self">
            <button class="modern-btn">
                🔍 Analytics
            </button>
        </a>
        <a href="/reports" target="_self">
            <button class="modern-btn">
                📈 Reports
            </button>
        </a>
        <a href="/forms" target="_self">
            <button class="modern-btn">
                📝 Data Entry
            </button>
        </a>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
