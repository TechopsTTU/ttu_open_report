"""
Mock queries module for tests - exposes get_open_orders_report as q010_open_order_report_data
"""

from models.query_definitions import get_open_orders_report

# Alias for backwards compatibility with tests
def q010_open_order_report_data(start_date='2025-01-01', end_date='2025-12-31'):
    """Legacy function name for tests"""
    return get_open_orders_report(start_date, end_date)

# Query descriptions for tests
query_descriptions = {
    "Open Order Report": "Shows all open and processing orders with customer details and total amounts."
}

def get_query_data():
    """Get real data from database queries."""
    try:
        # Use a default date range for demonstration/testing
        open_orders = get_open_orders_report('2025-01-01', '2025-12-31')
        return {
            "Open Order Report": open_orders
        }
    except Exception as e:
        # Fallback to empty DataFrames if database fails
        import pandas as pd
        return {
            "Open Order Report": pd.DataFrame()
        }
