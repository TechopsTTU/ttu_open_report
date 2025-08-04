"""
Test 04: Data Extraction Tests
Tests for extract.py functionality
"""
import pytest
import sys
import pandas as pd
import os
from pathlib import Path

# Add required paths for imports
sys.path.append('.')
import extract


class TestDataExtraction:
    """Test data extraction functionality"""
    
    def test_extract_module_imports(self):
        """Test that the extract module can be imported"""
        assert hasattr(extract, "extract_data"), "extract.py should have extract_data function"
    
    def test_extract_data_function_exists(self):
        """Test that extract_data function exists and is callable"""
        assert callable(getattr(extract, "extract_data", None)), "extract_data should be callable"
    
    def test_extract_data_returns_dict(self):
        """Test that extract_data returns a dictionary"""
        try:
            result = extract.extract_data(use_sample_data=True)
            assert isinstance(result, dict), "extract_data should return a dictionary"
            assert len(result) > 0, "extract_data dictionary should not be empty"
        except Exception as e:
            pytest.fail(f"extract_data failed with error: {e}")
    
    def test_extract_data_contains_required_tables(self):
        """Test that extract_data returns the required tables"""
        result = extract.extract_data(use_sample_data=True)
        required_tables = ['Orders', 'Customers', 'Products', 'OrderDetails']
        for table in required_tables:
            assert table in result, f"extract_data should contain the {table} table"
            assert isinstance(result[table], pd.DataFrame), f"{table} should be a DataFrame"
    
    def test_extract_data_structure(self):
        """Test that extracted data has the expected structure"""
        result = extract.extract_data(use_sample_data=True)
        
        # Check Orders table
        if 'Orders' in result:
            orders_df = result['Orders']
            expected_orders_columns = {'OrderID', 'OrderDate', 'CustomerID', 'Status'}
            assert all(col in orders_df.columns for col in expected_orders_columns), \
                f"Orders table missing expected columns. Has: {orders_df.columns.tolist()}"
        
        # Check Customers table
        if 'Customers' in result:
            customers_df = result['Customers']
            expected_customers_columns = {'CustomerID', 'CustomerName'}
            assert all(col in customers_df.columns for col in expected_customers_columns), \
                f"Customers table missing expected columns. Has: {customers_df.columns.tolist()}"
        
        # Check Products table
        if 'Products' in result:
            products_df = result['Products']
            expected_products_columns = {'ProductID', 'ProductName'}
            assert all(col in products_df.columns for col in expected_products_columns), \
                f"Products table missing expected columns. Has: {products_df.columns.tolist()}"
        
        # Check OrderDetails table
        if 'OrderDetails' in result:
            order_details_df = result['OrderDetails']
            expected_order_details_columns = {'OrderID', 'ProductID', 'Quantity'}
            assert all(col in order_details_df.columns for col in expected_order_details_columns), \
                f"OrderDetails table missing expected columns. Has: {order_details_df.columns.tolist()}"
    
    def test_save_to_sqlite_function_exists(self):
        """Test that save_to_sqlite function exists and is callable"""
        assert callable(getattr(extract, "save_to_sqlite", None)), "save_to_sqlite should be callable"


if __name__ == "__main__":
    pytest.main([__file__])
