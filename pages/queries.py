"""
Mock queries module for tests - exposes get_open_orders_report as q010_open_order_report_data
"""

from models.query_definitions import (
    get_open_orders_report,
    q093_shipment_status,
)

import sys

# Ensure module is accessible as both 'queries' and 'pages.queries'
sys.modules.setdefault("pages.queries", sys.modules[__name__])

# Alias for backwards compatibility with tests
def q010_open_order_report_data(start_date='2025-01-01', end_date='2025-12-31'):
    """Legacy function name for tests"""
    return get_open_orders_report(start_date, end_date)

# Query descriptions for tests
query_descriptions = {
    "Open Order Report": "Shows all open and processing orders with customer details and total amounts.",
    "Shipment Status": "Lists shipments with tracking numbers and current status.",
}

def get_query_data():
    """Get real data from database queries."""
    import pandas as pd

    # Use a default date range for demonstration/testing
    try:
        open_orders = q010_open_order_report_data('2025-01-01', '2025-12-31')
    except Exception:
        open_orders = pd.DataFrame()

    try:
        shipments = q093_shipment_status()
    except Exception:
        shipments = pd.DataFrame()

    return {
        "Open Order Report": open_orders,
        "Shipment Status": shipments,
    }
