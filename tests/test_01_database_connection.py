"""
Test 01: Database Connection Tests
Tests for database connectivity and basic operations
"""
import pytest
import sys
from pathlib import Path
import os
import sqlite3

# Add src to path for imports
sys.path.append('src')
from models.query_definitions import get_sqlite_connection, get_db_connection


class TestDatabaseConnection:
    """Test database connection functionality"""
    
    def test_sqlite_database_exists(self):
        """Test that SQLite database file exists"""
        db_path = Path("graphite_analytics.db")
        assert db_path.exists(), f"SQLite database not found: {db_path}"
    
    def test_sqlite_connection_success(self):
        """Test SQLite connection can be established"""
        conn = get_sqlite_connection()
        assert conn is not None, "SQLite connection should not be None"
        conn.close()
    
    def test_sqlite_connection_has_tables(self):
        """Test SQLite database has required tables"""
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['Orders', 'OrderDetails', 'Customers', 'Products']
        for table in required_tables:
            assert table in tables, f"Required table '{table}' not found in database"
        
        conn.close()
    
    def test_get_db_connection_defaults_to_sqlite(self):
        """Test that get_db_connection defaults to SQLite"""
        original_env = os.environ.get('DATABASE_ENV')
        if 'DATABASE_ENV' in os.environ:
            del os.environ['DATABASE_ENV']
        
        try:
            conn = get_db_connection()
            assert conn is not None, "Default database connection should not be None"
            # Verify it's SQLite by checking connection type
            assert isinstance(conn, sqlite3.Connection), "Default connection should be SQLite"
            conn.close()
        finally:
            if original_env:
                os.environ['DATABASE_ENV'] = original_env
    
    def test_sqlite_connection_can_execute_query(self):
        """Test that SQLite connection can execute a simple query"""
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        # Execute a simple query
        cursor.execute("SELECT COUNT(*) FROM Orders")
        result = cursor.fetchone()
        
        assert result is not None, "Query should return a result"
        assert isinstance(result[0], int), "Count should return an integer"
        assert result[0] >= 0, "Count should be non-negative"
        
        conn.close()


if __name__ == "__main__":
    pytest.main([__file__])
