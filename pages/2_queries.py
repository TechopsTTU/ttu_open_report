"""
Queries Page
Displays business queries and real database data. Handles query selection and download.
"""
import streamlit as st
import pandas as pd
import logging
from pathlib import Path
from models.query_definitions import get_open_orders_report

logging.basicConfig(level=logging.INFO)

# Query descriptions
query_descriptions = {
    "Open Order Report": "Shows all open and processing orders with customer details and total amounts."
}

def get_query_data():
    """Get real data from database queries."""
    try:
        # Use a default date range for demonstration/testing
        open_orders = get_open_orders_report('2025-01-01', '2025-12-31')
        logging.info("Real database queries executed successfully.")
        return {
            "Open Order Report": open_orders
        }
    except Exception as e:
        logging.error(f"Failed to execute database queries: {e}")
        # Fallback to empty DataFrames if database fails
        return {
            "Open Order Report": pd.DataFrame()
        }

def main():
    # Logo in upper right
    logo_path = Path("TTU_LOGO.jpg")
    if logo_path.exists():
        col1, col2 = st.columns([6, 1])
        with col2:
            st.image(str(logo_path), width=120)
    
    # Page title and description
    st.title("Business Analytics - GraphiteVision Analytics")
    st.markdown("""
    Execute advanced business queries and analyze results instantly. Select a query below to see real data from your SQLite database. When you switch to production, these will pull real-time operational data from your Pervasive database.
    """)

    # Get real data from database
    queries = get_query_data()

    # Query selection UI
    st.subheader("Select a Query")
    options = list(queries.keys())
    choice = st.radio("Select a query:", options, horizontal=True)
    
    if choice and not queries[choice].empty:
        st.info(query_descriptions.get(choice, ""))
        df = queries[choice]
        st.dataframe(df, use_container_width=True)
        
        # Show summary stats
        st.subheader("Summary")
        st.write(f"Total records: {len(df)}")
        
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
    elif choice and queries[choice].empty:
        st.warning("No data available for this query. Check database connection.")

if __name__ == "__main__":
    main()
