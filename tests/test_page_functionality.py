"""
Unit tests for GraphiteVision Analytics page components
Tests Streamlit page functionality, data processing, and UI components
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pages import queries
from src.models import table_schema
from extract import sanitize_filename
from src.models.query_definitions import get_open_orders_report, get_sqlite_connection

class TestQueriesPageFunctionality:
    """Test suite for queries page functionality"""
    
    @patch('src.pages.queries.get_open_orders_report')
    def test_get_query_data_success(self, mock_get_open_orders):
        """Test successful query data retrieval"""
        # Mock the database functions
        mock_orders = pd.DataFrame({
            'OrderID': [1, 2],
            'CustomerName': ['Test Corp', 'Demo Inc'],
            'OrderDate': ['2025-07-26', '2025-07-27'],
            'Status': ['Open', 'Processing'],
            'TotalAmount': [500.00, 750.00]
        })
        mock_get_open_orders.return_value = mock_orders
        
        result = queries.get_query_data()
        
        assert isinstance(result, dict)
        assert 'Open Order Report' in result
        
        assert isinstance(result['Open Order Report'], pd.DataFrame)
        
        assert len(result['Open Order Report']) == 2

    @patch('src.pages.queries.get_open_orders_report', side_effect=Exception("Database error"))
    def test_get_query_data_handles_exceptions(self, mock_get_open_orders):
        """Test that get_query_data handles database exceptions gracefully"""
        result = queries.get_query_data()
        
        assert isinstance(result, dict)
        assert 'Open Order Report' in result
        
        # Should return demo data on error
        assert not result['Open Order Report'].empty

class TestTableSchemaModule:
    """Additional tests for table schema functionality"""
    
    def test_map_column_type_edge_cases(self):
        """Test map_column_type with edge cases"""
        # Test None input
        assert table_schema.map_column_type(None) == 'object'
        
        # Test empty string
        assert table_schema.map_column_type('') == 'object'
        
        # Test case insensitive
        assert table_schema.map_column_type('INTEGER') == 'int64'
        assert table_schema.map_column_type('integer') == 'int64'
        assert table_schema.map_column_type('Integer') == 'int64'
        
        # Test partial matches
        assert table_schema.map_column_type('varchar(50)') == 'object'
        assert table_schema.map_column_type('datetime2') == 'datetime64[ns]'

    def test_schema_processing_with_real_data(self):
        """Test schema processing with realistic database schema data"""
        # Simulate real schema data
        schema_data = [
            ('CustomerID', 'int'),
            ('CustomerName', 'varchar'),
            ('CreatedDate', 'datetime'),
            ('IsActive', 'bit'),
            ('Balance', 'decimal'),
            ('Notes', 'text')
        ]
        
        processed_schema = []
        for col_name, col_type in schema_data:
            mapped_type = table_schema.map_column_type(col_type)
            processed_schema.append((col_name, mapped_type))
        
        expected_types = [
            ('CustomerID', 'int64'),
            ('CustomerName', 'object'),
            ('CreatedDate', 'datetime64[ns]'),
            ('IsActive', 'object'),  # bit maps to object
            ('Balance', 'object'),   # decimal maps to object
            ('Notes', 'object')
        ]
        
        assert processed_schema == expected_types

class TestExtractModule:
    """Additional tests for extract module functionality"""
    
    def test_sanitize_filename_comprehensive(self):
        """Comprehensive test for filename sanitization"""
        # Test various invalid characters
        test_cases = [
            ('file<name>.txt', 'file_name.txt'),
            ('file>name.txt', 'file_name.txt'),
            ('file:name.txt', 'file_name.txt'),
            ('file"name.txt', 'file_name.txt'),
            ('file|name.txt', 'file_name.txt'),
            ('file?name.txt', 'file_name.txt'),
            ('file*name.txt', 'file_name.txt'),
            ('file\\name.txt', 'file_name.txt'),
            ('file/name.txt', 'file_name.txt'),
        ]
        
        for input_name, expected in test_cases:
            result = sanitize_filename(input_name)
            assert result == expected, f"Expected {expected}, got {result} for input {input_name}"

    def test_sanitize_filename_edge_cases(self):
        """Test filename sanitization edge cases"""
        # Test empty string
        assert sanitize_filename('') == ''
        
        # Test string with only invalid characters
        assert sanitize_filename('<>:"|?*\\/.') == '__________'
        
        # Test very long filename
        long_name = 'a' * 300 + '.txt'
        result = sanitize_filename(long_name)
        assert len(result) <= 255, f"Filename length {len(result)} exceeds 255"
        
        # Test Unicode characters
        unicode_name = 'файл.txt'
        result = sanitize_filename(unicode_name)
        assert isinstance(result, str)

class TestDataProcessingUtilities:
    """Test suite for data processing utilities"""
    
    def test_dataframe_creation_with_various_types(self):
        """Test DataFrame creation with various data types"""
        # Test mixed data types
        test_data = {
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'score': [85.5, 92.0, 78.5],
            'active': [True, False, True],
            'created': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03'])
        }
        
        df = pd.DataFrame(test_data)
        
        assert len(df) == 3
        assert df['id'].dtype == 'int64'
        assert df['name'].dtype == 'object'
        assert df['score'].dtype == 'float64'
        assert df['active'].dtype == 'bool'
        assert pd.api.types.is_datetime64_any_dtype(df['created'])

    def test_dataframe_operations_safety(self):
        """Test safe DataFrame operations"""
        # Test with empty DataFrame
        empty_df = pd.DataFrame()
        
        # These operations should not raise exceptions
        assert len(empty_df) == 0
        assert empty_df.empty
        assert list(empty_df.columns) == []
        
        # Test CSV export of empty DataFrame
        csv_content = empty_df.to_csv(index=False)
        assert isinstance(csv_content, str)

    def test_data_type_conversion_safety(self):
        """Test safe data type conversions"""
        # Test various data conversion scenarios
        test_data = pd.DataFrame({
            'mixed_numbers': ['1', '2.5', '3', 'invalid'],
            'dates': ['2025-01-01', '2025-13-01', 'invalid', '2025-07-26'],
            'booleans': ['true', 'false', '1', '0']
        })
        
        # Test numeric conversion with error handling
        numeric_col = pd.to_numeric(test_data['mixed_numbers'], errors='coerce')
        assert not numeric_col.isna().all()  # Some values should convert successfully
        assert numeric_col.isna().any()     # Some values should fail (become NaN)
        
        # Test datetime conversion with error handling
        date_col = pd.to_datetime(test_data['dates'], errors='coerce')
        assert not date_col.isna().all()    # Some dates should convert
        assert date_col.isna().any()        # Some should fail

class TestApplicationIntegration:
    """Integration tests for application components"""
    
    @patch('src.pages.queries.get_open_orders_report', return_value=pd.DataFrame({'A': [1]}))
    def test_query_descriptions_completeness(self, mock_get_open_orders):
        """Test that query descriptions exist for all queries"""
        query_data = queries.get_query_data()
        
        # Check that we have descriptions for all queries
        for query_name in query_data.keys():
            assert query_name in queries.query_descriptions, f"Missing description for query: {query_name}"
            assert isinstance(queries.query_descriptions[query_name], str), f"Description for {query_name} is not a string"
            assert len(queries.query_descriptions[query_name]) > 0, f"Empty description for {query_name}"

    def test_file_path_handling(self):
        """Test file path handling across different modules"""
        from pathlib import Path
        
        # Test that logo path is handled correctly
        logo_path = Path("resources/static/TTU_LOGO.jpg")
        
        # Path should be a Path object
        assert isinstance(logo_path, Path)
        
        # Test path operations
        assert logo_path.name == "TTU_LOGO.jpg"
        assert logo_path.suffix == ".jpg"
        
        # Test database path
        db_path = Path("graphite_analytics.db")
        assert isinstance(db_path, Path)
        assert db_path.name == "graphite_analytics.db"

class TestErrorRecovery:
    """Test suite for error recovery and resilience"""
    
    @patch('src.models.query_definitions.get_db_connection', return_value=None)
    def test_graceful_degradation_no_database(self, mock_get_conn):
        """Test that application handles missing database gracefully"""
        result = queries.get_query_data()
        
        # Should return demo data, not crash
        assert isinstance(result, dict)
        for key, df in result.items():
            assert isinstance(df, pd.DataFrame)
            assert not df.empty

    @patch('src.pages.queries.get_open_orders_report')
    def test_partial_failure_recovery(self, mock_get_open_orders):
        """Test recovery when some queries fail but others succeed"""
        # Mock one query to succeed, one to fail
        mock_get_open_orders.side_effect = [pd.DataFrame({'test': [1, 2, 3]}), Exception("Query failed")]
        
        result = queries.get_query_data()
        
        # Should handle partial failure by returning demo data
        assert isinstance(result, dict)
        assert not result['Open Order Report'].empty


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
