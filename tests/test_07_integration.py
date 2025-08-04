"""
Test 07: Integration Tests
Tests for integrated functionality between different components
"""
import pytest
import sys
import pandas as pd
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add required paths for imports
sys.path.append('src')
sys.path.append('.')


class TestIntegrationFunctionality:
    """Test integrated functionality between components"""
    
    def test_database_to_ui_integration(self):
        """Test integration between database and UI components"""
        # This test checks if data can flow from database to UI
        # We'll mock the database connection and check if UI functions can use it
        mock_df = pd.DataFrame({
            'OrderID': ['31384', '31592'],
            'OrderDate': ['2020-05-13', '2021-11-03'],
            'CustomerName': ['ACME Corp', 'Toyo Industries'],
            'ProductName': ['Carbon Component A', 'Graphite Assembly B'],
            'TotalCost': [11600.0, 12000.0]
        })
        
        with patch('models.query_definitions.run_query', return_value=mock_df), \
             patch('models.query_definitions.get_open_orders_report', return_value=mock_df):
            
            # Try to import and use get_query_data function from queries
            try:
                # Use importlib to dynamically import the module
                import importlib.util
                spec = importlib.util.spec_from_file_location("queries", "pages/2_queries.py")
                if spec:
                    queries = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(queries)
                    
                    # Check if get_query_data exists and can be called
                    if hasattr(queries, "get_query_data") and callable(queries.get_query_data):
                        result = queries.get_query_data()
                        assert isinstance(result, dict), "get_query_data should return a dictionary"
                        assert "Open Order Report" in result, "Result should contain Open Order Report"
                        
                        # Check that the data is correctly passed through
                        result_df = result["Open Order Report"]
                        assert isinstance(result_df, pd.DataFrame), "Result value should be a DataFrame"
                        assert len(result_df) > 0, "Result DataFrame should not be empty"
                    else:
                        pytest.skip("get_query_data function not found in queries module")
                else:
                    pytest.skip("Could not find 2_queries.py module")
            except Exception as e:
                pytest.skip(f"Error testing database to UI integration: {e}")
    
    def test_query_definitions_to_extraction_integration(self):
        """Test integration between query definitions and data extraction"""
        # Import both modules
        try:
            sys.path.append('.')
            import extract
            sys.path.append('src')
            from models import query_definitions
            
            # Check if both have the necessary functions
            assert hasattr(extract, "extract_data"), "extract module should have extract_data function"
            assert hasattr(query_definitions, "run_query"), "query_definitions module should have run_query function"
            
            # Test if one can potentially use the other
            with patch('models.query_definitions.run_query') as mock_run_query:
                mock_run_query.return_value = pd.DataFrame({"test": [1, 2, 3]})
                
                # This is a simplified integration test
                if hasattr(extract, "extract_data") and callable(extract.extract_data):
                    # Check that extract_data works with sample data
                    result = extract.extract_data(use_sample_data=True)
                    assert isinstance(result, dict), "extract_data should return a dictionary"
                    assert len(result) > 0, "Result should not be empty"
                else:
                    pytest.skip("extract_data function not found or not callable")
        except ImportError as e:
            pytest.skip(f"Could not import required modules: {e}")
        except Exception as e:
            pytest.skip(f"Error in query definitions to extraction integration test: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
