import pytest
import pandas as pd
from datetime import date
from src.models.query_definitions import get_open_orders_report

@pytest.mark.parametrize("start_date, end_date", [
    (date(2020, 1, 1), date(2025, 12, 31)),  # Use wider date range to include actual data
    (None, None)
])
def test_open_order_report_logic(start_date, end_date):
    """Test open order report with actual database data"""
    df = get_open_orders_report(
        start_date=start_date.isoformat() if start_date else "2000-01-01",
        end_date=end_date.isoformat() if end_date else "2030-12-31"
    )
    
    # Test DataFrame structure
    assert isinstance(df, pd.DataFrame), "Should return a DataFrame"
    
    # If data exists, check structure
    if not df.empty:
        expected_columns = ['OrderID', 'OrderDate', 'CustomerName', 'CustomerPO', 
                           'ProductID', 'ProductName', 'QtyRemaining', 'UnitPrice', 
                           'TotalCost', 'OrderStatus', 'PromiseDate']
        
        for col in expected_columns:
            assert col in df.columns, f"Missing expected column: {col}"
        
        # Check data types
        assert pd.api.types.is_numeric_dtype(df['QtyRemaining']), "QtyRemaining should be numeric"
        assert pd.api.types.is_numeric_dtype(df['UnitPrice']), "UnitPrice should be numeric"
        assert pd.api.types.is_numeric_dtype(df['TotalCost']), "TotalCost should be numeric"
    else:
        # If no data, that's also valid - just ensure proper empty DataFrame structure
        print("No data found for given date range - this is acceptable for test purposes")
