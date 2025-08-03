#!/usr/bin/env python3
"""
Health check script for GraphiteVision Analytics application.
Verifies that all critical components are working before deployment.
"""

import sys
import logging
from pathlib import Path

def check_database():
    """Check database connectivity and data"""
    try:
        from src.models.query_definitions import get_sqlite_connection
        
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        # Check that required tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['Customers', 'Products', 'Orders', 'OrderDetails', 'Shipments']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            return False, f"Missing required tables: {missing_tables}"
        
        # Check that we have some data
        cursor.execute("SELECT COUNT(*) FROM Orders")
        order_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Customers")
        customer_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Products")
        product_count = cursor.fetchone()[0]
        
        if order_count == 0 or customer_count == 0 or product_count == 0:
            return False, f"Insufficient data: Orders={order_count}, Customers={customer_count}, Products={product_count}"
        
        conn.close()
        return True, f"Database OK: {order_count} orders, {customer_count} customers, {product_count} products"
        
    except Exception as e:
        return False, f"Database error: {e}"

def check_required_files():
    """Check that required application files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'src/models/query_definitions.py',
        'src/models/table_schema.py',
        'graphite_analytics.db'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        return False, f"Missing required files: {missing_files}"
    
    return True, f"All {len(required_files)} required files present"

def check_imports():
    """Check that critical imports work"""
    try:
        import pandas
        import streamlit 
        import sqlite3
        import pyodbc
        from src.models.query_definitions import get_sqlite_connection, get_open_orders_report
        from src.models.table_schema import map_column_type
        
        return True, "All critical imports successful"
        
    except ImportError as e:
        return False, f"Import error: {e}"

def main():
    """Run all health checks"""
    print("GraphiteVision Analytics - Health Check")
    print("=" * 50)
    
    checks = [
        ("Required Files", check_required_files),
        ("Python Imports", check_imports), 
        ("Database", check_database),
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            success, message = check_func()
            status = "[PASS]" if success else "[FAIL]"
            print(f"{check_name:20} {status} - {message}")
            
            if not success:
                all_passed = False
                
        except Exception as e:
            print(f"{check_name:20} [ERROR] - {e}")
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("SUCCESS: All health checks passed! Application ready for deployment.")
        return 0
    else:
        print("FAILURE: Some health checks failed. Please fix issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())