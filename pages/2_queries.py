"""
Queries Page
Displays business queries and sample/mock data. Handles query selection and download.
"""
import streamlit as st
import pandas as pd
import numpy as np
import logging
from models.query_definitions import (
    q010_open_order_report_data,
    q093_shipment_status,
    # import other query funcs as you implement them
)

logging.basicConfig(level=logging.INFO)

# Mock query descriptions
query_descriptions = {
    "Open Order Report": "Shows all open orders with customer, date, and status.",
    "Shipment Status": "Displays shipment status for recent orders.",
}

# Generate mock data with error handling
try:
    open_order_data = pd.DataFrame({
        "OrderID": np.arange(1001, 1011),
        "OrderDate": pd.date_range("2025-07-01", periods=10),
        "Customer": np.random.choice(["Acme", "Beta", "Gamma", "Delta"], 10),
        "Status": np.random.choice(["Open", "Closed"], 10),
        "Amount": np.random.uniform(100, 500, 10).round(2)
    })
    shipment_status_data = pd.DataFrame({
        "ShipmentID": np.arange(501, 511),
        "OrderID": np.arange(1001, 1011),
        "ShippedDate": pd.date_range("2025-07-04", periods=10),
        "Status": np.random.choice(["Shipped", "Pending"], 10)
    })
    logging.info("Mock data generated successfully.")
except Exception as e:
    logging.error(f"Failed to generate mock data: {e}")
    open_order_data = pd.DataFrame()
    shipment_status_data = pd.DataFrame()

queries = {
    "Open Order Report": open_order_data,
    "Shipment Status": shipment_status_data,
}

def main():
    # Page title and description
    st.title("Queries")
    st.markdown("""
    Run key business queries and view results instantly. Select a query below to see sample data. When live, these will pull directly from your backend.
    """)

    # Generate mock data with error handling
    try:
        open_order_data = pd.DataFrame({
            "OrderID": np.arange(1001, 1011),
            "OrderDate": pd.date_range("2025-07-01", periods=10),
            "Customer": np.random.choice(["Acme", "Beta", "Gamma", "Delta"], 10),
            "Status": np.random.choice(["Open", "Closed"], 10),
            "Amount": np.random.uniform(100, 500, 10).round(2)
        })
        shipment_status_data = pd.DataFrame({
            "ShipmentID": np.arange(501, 511),
            "OrderID": np.arange(1001, 1011),
            "ShippedDate": pd.date_range("2025-07-04", periods=10),
            "Status": np.random.choice(["Shipped", "Pending"], 10)
        })
        logging.info("Mock data generated successfully.")
    except Exception as e:
        logging.error(f"Failed to generate mock data: {e}")
        st.error("Error generating mock data.")
        return

    queries = {
        "Open Order Report": open_order_data,
        "Shipment Status": shipment_status_data,
    }

    # Query selection UI
    st.subheader("Select a Query")
    options = list(queries.keys())
    choice = st.radio("Select a query:", options, horizontal=True)
    if choice:
        st.info(query_descriptions.get(choice, ""))
        df = queries[choice]
        st.dataframe(df, use_container_width=True)
        try:
            st.download_button(
                "Download Query Results",
                df.to_csv(index=False).encode("utf-8"),
                file_name=f"{choice.replace(' ', '_')}.csv",
                mime="text/csv",
            )
        except Exception as e:
            logging.error(f"Download failed: {e}")
            st.error("Download failed.")

if __name__ == "__main__":
    main()

st.subheader("Select a Query")
options = list(queries.keys())
choice = st.radio("Select a query:", options, horizontal=True)
if choice:
    st.info(query_descriptions.get(choice, ""))
    df = queries[choice]
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "Download Query Results",
        df.to_csv(index=False).encode("utf-8"),
        file_name=f"{choice.replace(' ', '_')}.csv",
        mime="text/csv",
    )
