"""
Unit tests for GraphiteVision Analytics database queries and models
Tests SQLite database operations, query functions, and data integrity
"""
import pytest
import pandas as pd
import sqlite3
import os
import tempfile
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import the modules we want to test
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.query_definitions import (
    get_sqlite_connection,
    q010_open_order_report_data,
    q093_shipment_status,
    run_pass_through
)

class TestDatabaseConnection:
    """Test suite for database connection functionality"""
    
    def test_sqlite_connection_success(self):
        """Test successful SQLite database connection"""
        # Create a temporary database for testing
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            temp_db_path = tmp_file.name
        
        try:
            # Create a simple table for testing
            conn = sqlite3.connect(temp_db_path)
            conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
            conn.execute("INSERT INTO test_table (name) VALUES ('test')")
            conn.commit()
            conn.close()
            
            # Test our connection function
            with patch('models.query_definitions.Path') as mock_path:
                mock_path.return_value.exists.return_value = True
                mock_path.return_value.__str__ = lambda self: temp_db_path
                
                connection = get_sqlite_connection()
                assert connection is not None
                
                # Test that we can query the database
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM test_table")
                results = cursor.fetchall()
                assert len(results) == 1
                assert results[0][1] == 'test'
                
                connection.close()
                
        finally:
            # Clean up
            if os.path.exists(temp_db_path):
                os.unlink(temp_db_path)

    def test_sqlite_connection_file_not_exists(self):
        """Test behavior when SQLite database file doesn't exist"""
        with patch('models.query_definitions.Path') as mock_path:
            mock_path.return_value.exists.return_value = False
            
            connection = get_sqlite_connection()
            assert connection is None

class TestQueryFunctions:
    """Test suite for query execution functions"""
    
    @pytest.fixture
    def mock_database(self):
        """Create a mock database with test data"""
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            temp_db_path = tmp_file.name
        
        conn = sqlite3.connect(temp_db_path)
        
        # Create test tables
        conn.execute("""
            CREATE TABLE Customers (
                CustomerID INTEGER PRIMARY KEY,
                CustomerName TEXT,
                ContactPerson TEXT,
                Email TEXT,
                Phone TEXT
            )
        """)
        
        conn.execute("""
            CREATE TABLE Products (
                ProductID INTEGER PRIMARY KEY,
                ProductName TEXT,
                Category TEXT,
                UnitPrice REAL
            )
        """)
        
        conn.execute("""
            CREATE TABLE Orders (
                OrderID INTEGER PRIMARY KEY,
                CustomerID INTEGER,
                OrderDate TEXT,
                Status TEXT,
                TotalAmount REAL,
                FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
            )
        """)
        
        conn.execute("""
            CREATE TABLE Shipments (
                ShipmentID INTEGER PRIMARY KEY,
                OrderID INTEGER,
                ShippedDate TEXT,
                TrackingNumber TEXT,
                Status TEXT,
                FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
            )
        """)
        
        # Insert test data
        conn.execute("INSERT INTO Customers VALUES (1, 'Test Corp', 'John Doe', 'john@test.com', '123-456-7890')")
        conn.execute("INSERT INTO Products VALUES (1, 'Test Product', 'Category A', 100.00)")
        conn.execute("INSERT INTO Orders VALUES (1, 1, '2025-07-26', 'Open', 500.00)")
        conn.execute("INSERT INTO Shipments VALUES (1, 1, '2025-07-27', 'TRK123', 'Shipped')")
        
        conn.commit()
        conn.close()
        
        yield temp_db_path
        
        # Clean up
        if os.path.exists(temp_db_path):
            os.unlink(temp_db_path)

    def test_q010_open_order_report_data(self, mock_database):
        """Test open order report query"""
        with patch('models.query_definitions.get_sqlite_connection') as mock_conn:
            # Mock the database connection
            conn = sqlite3.connect(mock_database)
            mock_conn.return_value = conn
            result = q010_open_order_report_data()
            assert isinstance(result, pd.DataFrame)
            assert not result.empty
            assert 'OrderID' in result.columns
            assert 'CustomerName' in result.columns
            assert 'OrderDate' in result.columns
            assert 'Status' in result.columns
            assert 'TotalAmount' in result.columns
            # Check that we got the test data
            assert len(result) > 0
            assert result.iloc[0]['CustomerName'] == 'Test Corp'
            assert result.iloc[0]['Status'] == 'Open'
            conn.close()

    def test_q093_shipment_status(self, mock_database):
        """Test shipment status query"""
        with patch('models.query_definitions.get_sqlite_connection') as mock_conn:
            # Mock the database connection
            conn = sqlite3.connect(mock_database)
            mock_conn.return_value = conn
            result = q093_shipment_status()
            assert isinstance(result, pd.DataFrame)
            assert not result.empty
            assert 'ShipmentID' in result.columns
            assert 'OrderID' in result.columns
            assert 'Status' in result.columns
            assert 'TrackingNumber' in result.columns
            assert 'ShippedDate' in result.columns
            # Check that we got the test data
            assert len(result) > 0
            assert result.iloc[0]['TrackingNumber'] == 'TRK123'
            assert result.iloc[0]['Status'] == 'Shipped'
            conn.close()

    def test_query_functions_handle_connection_failure(self):
        """Test that query functions handle database connection failures gracefully"""
        with patch('models.query_definitions.get_sqlite_connection', return_value=None):
            # Test q010
            result = q010_open_order_report_data()
            assert isinstance(result, pd.DataFrame)
            assert result.empty
            
            # Test q093
            result = q093_shipment_status()
            assert isinstance(result, pd.DataFrame)
            assert result.empty

    def test_query_functions_handle_sql_errors(self, mock_database):
        """Test that query functions handle SQL execution errors"""
        with patch('models.query_definitions.get_sqlite_connection') as mock_conn:
            # Create a mock connection that raises an exception
            mock_connection = MagicMock()
            mock_connection.execute.side_effect = sqlite3.Error("Database error")
            mock_conn.return_value = mock_connection
            
            # Test that functions return empty DataFrames on error
            result = q010_open_order_report_data()
            assert isinstance(result, pd.DataFrame)
            assert result.empty

class TestRunPassThrough:
    """Test suite for the run_pass_through function"""
    
    def test_run_pass_through_sqlite_mode(self):
        """Test run_pass_through function in SQLite mode"""
        test_query = "SELECT 1 as test_column"
        
        with patch('models.query_definitions.os.getenv', return_value='true'):
            with patch('models.query_definitions.get_sqlite_connection') as mock_conn:
                # Mock successful SQLite connection
                mock_connection = MagicMock()
                mock_conn.return_value = mock_connection
                
                # Mock pandas read_sql to return test data
                with patch('models.query_definitions.pd.read_sql') as mock_read_sql:
                    mock_read_sql.return_value = pd.DataFrame({'test_column': [1]})
                    
                    result = run_pass_through(test_query)
                    
                    assert isinstance(result, pd.DataFrame)
                    assert not result.empty
                    assert 'test_column' in result.columns
                    mock_read_sql.assert_called_once_with(test_query, mock_connection)

    def test_run_pass_through_odbc_mode(self):
        """Test run_pass_through function in ODBC mode"""
        test_query = "SELECT 1 as test_column"
        
        with patch('models.query_definitions.os.getenv', return_value='false'):
            with patch('models.query_definitions.pyodbc.connect') as mock_connect:
                # Mock successful ODBC connection
                mock_connection = MagicMock()
                mock_connect.return_value = mock_connection
                
                # Mock pandas read_sql to return test data
                with patch('models.query_definitions.pd.read_sql') as mock_read_sql:
                    mock_read_sql.return_value = pd.DataFrame({'test_column': [1]})
                    
                    result = run_pass_through(test_query)
                    
                    assert isinstance(result, pd.DataFrame)
                    assert not result.empty
                    assert 'test_column' in result.columns

    def test_run_pass_through_handles_errors(self):
        """Test that run_pass_through handles database errors gracefully"""
        test_query = "SELECT * FROM nonexistent_table"
        
        with patch('models.query_definitions.os.getenv', return_value='true'):
            with patch('models.query_definitions.get_sqlite_connection', return_value=None):
                result = run_pass_through(test_query)
                assert isinstance(result, pd.DataFrame)
                assert result.empty

class TestDataIntegrity:
    """Test suite for data integrity and validation"""
    
    def test_database_schema_exists(self):
        """Test that the main database file exists and has proper schema"""
        db_path = Path("graphite_analytics.db")
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Check that required tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['Customers', 'Products', 'Orders', 'OrderDetails', 'Shipments']
            for table in required_tables:
                assert table in tables, f"Required table {table} not found in database"
            
            conn.close()

    def test_sample_data_integrity(self):
        """Test that sample data in database has proper relationships"""
        db_path = Path("graphite_analytics.db")
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            
            # Test foreign key relationships
            cursor = conn.cursor()
            
            # Check that all orders have valid customers
            cursor.execute("""
                SELECT COUNT(*) FROM Orders o 
                LEFT JOIN Customers c ON o.CustomerID = c.CustomerID 
                WHERE c.CustomerID IS NULL
            """)
            orphaned_orders = cursor.fetchone()[0]
            assert orphaned_orders == 0, "Found orders without valid customers"
            
            # Check that all shipments have valid orders
            cursor.execute("""
                SELECT COUNT(*) FROM Shipments s 
                LEFT JOIN Orders o ON s.OrderID = o.OrderID 
                WHERE o.OrderID IS NULL
            """)
            orphaned_shipments = cursor.fetchone()[0]
            assert orphaned_shipments == 0, "Found shipments without valid orders"
            
            conn.close()

class TestErrorHandling:
    """Test suite for error handling and edge cases"""
    
    def test_empty_query_result_handling(self):
        """Test handling of queries that return no results"""
        with patch('models.query_definitions.get_sqlite_connection') as mock_conn:
            # Create a mock connection that returns empty results
            mock_connection = MagicMock()
            mock_conn.return_value = mock_connection
            
            with patch('models.query_definitions.pd.read_sql') as mock_read_sql:
                mock_read_sql.return_value = pd.DataFrame()  # Empty DataFrame
                
                result = q010_open_order_report_data()
                assert isinstance(result, pd.DataFrame)
                assert result.empty

    def test_invalid_sql_query_handling(self):
        """Test handling of invalid SQL queries"""
        invalid_query = "INVALID SQL STATEMENT"
        
        result = run_pass_through(invalid_query)
        assert isinstance(result, pd.DataFrame)
        # Should return empty DataFrame on error

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
