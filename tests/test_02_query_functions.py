"""
Test 02: Query Definitions Tests
Tests query functions and database operations
"""
import pytest
import sys
import pandas as pd
import os

# Set environment to use SQLite for tests
os.environ["DATABASE_ENV"] = "sqlite"

# Add src to path for imports
sys.path.append('src')
from models.query_definitions import run_query, get_open_orders_report


class TestQueryFunctions:
    """Test query functionality"""
    
    def test_run_query_returns_dataframe(self):
        """Test run_query returns a DataFrame"""
        sql = "SELECT 1 AS test"
        result = run_query(sql)
        assert isinstance(result, pd.DataFrame), "run_query should return a pandas DataFrame"
        assert not result.empty, "DataFrame from simple query should not be empty"
    
    def test_run_query_with_params(self):
        """Test run_query with parameters"""
        sql = "SELECT ? AS param_value"
        test_value = 42
        result = run_query(sql, params=(test_value,))
        assert isinstance(result, pd.DataFrame), "run_query with params should return a pandas DataFrame"
        assert not result.empty, "DataFrame from parameterized query should not be empty"
        assert result.iloc[0]['param_value'] == test_value, f"Expected {test_value}, got {result.iloc[0]['param_value']}"
    
    def test_open_orders_report_returns_dataframe(self):
        """Test get_open_orders_report returns a DataFrame"""
        start_date = '2020-01-01'
        end_date = '2025-12-31'
        result = get_open_orders_report(start_date, end_date)
        assert isinstance(result, pd.DataFrame), "get_open_orders_report should return a pandas DataFrame"
        
        # Test returned columns - even if empty, the function should return a DataFrame with expected structure
        expected_columns = {
            'OrderID', 'OrderDate', 'CustomerName', 'CustomerPO', 'ProductID', 
            'ProductName', 'QtyRemaining', 'UnitPrice', 'TotalCost', 'OrderStatus', 'PromiseDate'
        }
        
        # Check if all expected columns exist
        missing_columns = expected_columns - set(result.columns)
        assert not missing_columns, f"Missing expected columns: {missing_columns}"
    
    def test_run_query_handles_invalid_sql(self):
        """Test run_query gracefully handles invalid SQL"""
        sql = "INVALID SQL STATEMENT"
        result = run_query(sql)
        assert isinstance(result, pd.DataFrame), "run_query should return an empty DataFrame for invalid SQL"
        assert result.empty, "DataFrame from invalid SQL should be empty"
    
    def test_run_query_with_joins(self):
        """Test run_query can handle joins between tables"""
        sql = """
        SELECT o.OrderID, c.CustomerName 
        FROM Orders o
        JOIN Customers c ON o.CustomerID = c.CustomerID
        LIMIT 5
        """
        result = run_query(sql)
        assert isinstance(result, pd.DataFrame), "run_query with joins should return a pandas DataFrame"
        
        # Even if no data, the columns should be correct
        expected_columns = {'OrderID', 'CustomerName'}
        missing_columns = expected_columns - set(result.columns)
        assert not missing_columns, f"Missing expected columns in join result: {missing_columns}"


if __name__ == "__main__":
    pytest.main([__file__])
