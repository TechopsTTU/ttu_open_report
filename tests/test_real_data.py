#!/usr/bin/env python3
"""Test script to verify real data is loaded correctly"""

import sqlite3
import logging

def test_database():
    """Test the real data in the database"""
    conn = sqlite3.connect('graphite_analytics.db')
    cursor = conn.cursor()
    
    print("Testing Real Data Migration Results")
    print("=" * 50)
    
    # Test Order IDs with alphanumeric values
    cursor.execute('SELECT COUNT(*) FROM Orders WHERE OrderID LIKE "B%"')
    b_orders = cursor.fetchone()[0]
    print(f"Orders with 'B' prefix: {b_orders}")
    
    # Sample orders
    cursor.execute('SELECT OrderID, CustomerID, TotalAmount FROM Orders LIMIT 5')
    orders = cursor.fetchall()
    print(f"\nSample Orders:")
    for order in orders:
        print(f"  Order {order[0]}: Customer {order[1]}, Total ${order[2]:.2f}")
    
    # Test customers
    cursor.execute('SELECT COUNT(*) FROM Customers')
    customer_count = cursor.fetchone()[0]
    print(f"\nTotal Customers: {customer_count}")
    
    # Sample customers
    cursor.execute('SELECT CustomerID, CustomerName FROM Customers LIMIT 5')
    customers = cursor.fetchall()
    print(f"Sample Customers:")
    for customer in customers:
        print(f"  {customer[0]}: {customer[1]}")
    
    # Test products with real part numbers
    cursor.execute('SELECT COUNT(*) FROM Products')
    product_count = cursor.fetchone()[0]
    print(f"\nTotal Products: {product_count}")
    
    # Sample products
    cursor.execute('SELECT ProductID, ProductName FROM Products LIMIT 5')
    products = cursor.fetchall()
    print(f"Sample Products:")
    for product in products:
        print(f"  {product[0]}: {product[1][:50]}...")
    
    # Test shipments
    cursor.execute('SELECT COUNT(*) FROM Shipments')
    shipment_count = cursor.fetchone()[0]
    print(f"\nTotal Shipments: {shipment_count}")
    
    # Test unique order count in order details
    cursor.execute('SELECT COUNT(DISTINCT OrderID) FROM OrderDetails')
    unique_orders = cursor.fetchone()[0]
    print(f"Unique Orders in Details: {unique_orders}")
    
    print("\nReal data verification complete!")
    
    conn.close()

if __name__ == "__main__":
    test_database()
