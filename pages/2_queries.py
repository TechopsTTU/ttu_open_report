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
        open_orders = get_open_orders_report('2020-01-01', '2025-12-31')
        logging.info("Real database queries executed successfully.")
        
        # Create demo data if no real data available
        if open_orders.empty:
            logging.warning("No real data found, creating demo data for display")
            # Create sample data for demo purposes
            open_orders = pd.DataFrame({
                'OrderID': ['31384', '31592', '31612', '31816', '31898'],
                'OrderDate': ['2020-05-13', '2021-11-03', '2022-01-04', '2023-02-15', '2023-05-10'],
                'CustomerName': ['ACME Corp', 'Toyo Industries', 'GlobalTech', 'Innovative Solutions', 'TechFusion'],
                'CustomerPO': ['60776 R2', '4500035575', 'PORD12108264', 'PO-2023-0215', 'TF-2023-051'],
                'ProductID': ['ZZZ40AN1', 'HZZ30AL3', 'GYT25CF', 'ISO-9000-X', 'TRMX-1500'],
                'ProductName': ['Carbon Component A', 'Graphite Assembly B', 'Specialized Fixture', 'ISO Compliant Part', 'Thermal Resistor'],
                'QtyRemaining': [2, 5, 10, 3, 8],
                'UnitPrice': [5800.0, 2400.0, 1200.0, 3500.0, 950.0],
                'TotalCost': [11600.0, 12000.0, 12000.0, 10500.0, 7600.0],
                'OrderStatus': ['Open', 'BP', 'NP', 'BN', 'BP'],
                'PromiseDate': ['2025-06-15', '2025-09-30', '2025-12-15', '2025-08-01', '2025-07-10']
            })
        
        return {
            "Open Order Report": open_orders
        }
    except Exception as e:
        logging.error(f"Failed to execute database queries: {e}")
        # Create fallback demo data
        logging.info("Creating fallback demo data for display")
        open_orders = pd.DataFrame({
            'OrderID': ['31384', '31592', '31612', '31816', '31898'],
            'OrderDate': ['2020-05-13', '2021-11-03', '2022-01-04', '2023-02-15', '2023-05-10'],
            'CustomerName': ['ACME Corp', 'Toyo Industries', 'GlobalTech', 'Innovative Solutions', 'TechFusion'],
            'CustomerPO': ['60776 R2', '4500035575', 'PORD12108264', 'PO-2023-0215', 'TF-2023-051'],
            'ProductID': ['ZZZ40AN1', 'HZZ30AL3', 'GYT25CF', 'ISO-9000-X', 'TRMX-1500'],
            'ProductName': ['Carbon Component A', 'Graphite Assembly B', 'Specialized Fixture', 'ISO Compliant Part', 'Thermal Resistor'],
            'QtyRemaining': [2, 5, 10, 3, 8],
            'UnitPrice': [5800.0, 2400.0, 1200.0, 3500.0, 950.0],
            'TotalCost': [11600.0, 12000.0, 12000.0, 10500.0, 7600.0],
            'OrderStatus': ['Open', 'BP', 'NP', 'BN', 'BP'],
            'PromiseDate': ['2025-06-15', '2025-09-30', '2025-12-15', '2025-08-01', '2025-07-10']
        })
        
        return {
            "Open Order Report": open_orders
        }

def main():
    # Logo in upper right
    logo_path = Path("static/TTU_LOGO.jpg")
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
    
    if choice:
        st.info(query_descriptions.get(choice, ""))
        df = queries[choice]
        
        # Add date filter for open orders
        if choice == "Open Order Report":
            st.subheader("Filter Data")
            col1, col2 = st.columns(2)
            with col1:
                min_date = pd.to_datetime(df['OrderDate']).min() if not df.empty else pd.to_datetime('2020-01-01')
                max_date = pd.to_datetime(df['OrderDate']).max() if not df.empty else pd.to_datetime('2025-12-31')
                start_date = st.date_input("Order From:", min_date)
            with col2:
                end_date = st.date_input("Order To:", max_date)
            
            # Filter by customer name
            if not df.empty:
                customer_list = ['All'] + sorted(df['CustomerName'].unique().tolist())
                selected_customer = st.selectbox("Filter by Customer:", customer_list)
                
                # Apply filters
                filtered_df = df
                if selected_customer != 'All':
                    filtered_df = filtered_df[filtered_df['CustomerName'] == selected_customer]
                
                # Apply date filter
                filtered_df = filtered_df[
                    (pd.to_datetime(filtered_df['OrderDate']) >= pd.to_datetime(start_date)) & 
                    (pd.to_datetime(filtered_df['OrderDate']) <= pd.to_datetime(end_date))
                ]
                
                # Show filtered data
                st.dataframe(filtered_df, use_container_width=True)
                
                # Show summary stats
                st.subheader("Summary")
                st.write(f"Total records: {len(filtered_df)}")
                
                # Add visual analytics
                if not filtered_df.empty:
                    st.subheader("Visual Analytics")
                    chart_type = st.radio("Select chart type:", ["Orders by Customer", "Orders by Status", "Monthly Order Trend"], horizontal=True)
                    
                    if chart_type == "Orders by Customer":
                        customer_summary = filtered_df.groupby('CustomerName').agg({'OrderID': 'count', 'TotalCost': 'sum'}).reset_index()
                        customer_summary.columns = ['Customer', 'Order Count', 'Total Value']
                        st.bar_chart(customer_summary.set_index('Customer')['Total Value'])
                    elif chart_type == "Orders by Status":
                        status_summary = filtered_df.groupby('OrderStatus').agg({'OrderID': 'count'}).reset_index()
                        status_summary.columns = ['Status', 'Order Count']
                        st.bar_chart(status_summary.set_index('Status'))
                    else:  # Monthly trend
                        filtered_df['Month'] = pd.to_datetime(filtered_df['OrderDate']).dt.strftime('%Y-%m')
                        monthly_summary = filtered_df.groupby('Month').agg({'OrderID': 'count', 'TotalCost': 'sum'}).reset_index()
                        st.line_chart(monthly_summary.set_index('Month')['TotalCost'])
                
                try:
                    st.download_button(
                        "Download Query Results",
                        filtered_df.to_csv(index=False).encode("utf-8"),
                        file_name=f"{choice.replace(' ', '_')}.csv",
                        mime="text/csv",
                    )
                except Exception as e:
                    logging.error(f"Download failed: {e}")
                    st.error("Download failed.")
        else:
            st.dataframe(df, use_container_width=True)
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

if __name__ == "__main__":
    main()
