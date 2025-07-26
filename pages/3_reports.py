"""
Reports Page
Displays interactive charts and business data visualizations. Handles chart selection and rendering.
"""
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def main():
    # Logo in upper right
    logo_path = Path("TTU_LOGO.jpg")
    if logo_path.exists():
        col1, col2 = st.columns([6, 1])
        with col2:
            st.image(str(logo_path), width=120)
    
    # Page title and description
    st.title("Interactive Reports")
    st.markdown("""
    Visualize your business data with interactive charts and comprehensive reports. These sample visualizations will display real-time data once your database is connected.
    """)

    # Generate mock data for chart with error handling
    try:
        order_dates = pd.date_range("2025-07-01", periods=10)
        order_counts = np.random.randint(5, 20, size=10)
        logging.info("Mock report data generated successfully.")
    except Exception as e:
        logging.error(f"Failed to generate mock report data: {e}")
        st.error("Error generating report data.")
        return

    # Chart selection UI
    st.subheader("Total Orders by Date")
    options = ["Bar Chart", "Line Chart"]
    chart_type = st.radio("Select chart type:", options, horizontal=True)

    # Chart rendering with error handling
    container = st.container()
    with container:
        try:
            fig, ax = plt.subplots(figsize=(6, 2.5))
            if chart_type == "Bar Chart":
                ax.bar(order_dates, order_counts, color="#0072B5")
            else:
                ax.plot(order_dates, order_counts, marker="o", color="#0072B5")
            ax.set_ylabel("Number of Orders")
            ax.set_xlabel("Order Date")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        except Exception as e:
            logging.error(f"Chart rendering failed: {e}")
            st.error("Chart rendering failed.")

    st.write(f"Total orders: {order_counts.sum()}")
    st.write(f"Average orders per day: {order_counts.mean():.2f}")

    # Placeholder for future report logic
    st.info("Report logic will be enabled once query functions are implemented.")

if __name__ == "__main__":
    main()
