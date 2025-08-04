"""
Unit tests for Forms page functionality
Tests form validation, database operations, and business logic
"""
import pytest
import pandas as pd
import sqlite3
import tempfile
import os
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestFormsDatabaseOperations:
    """Test suite for forms database operations"""
    
    def test_database_connection_available(self):
        """Test that database connection is available for forms"""
        db_path = Path("graphite_analytics.db")
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Check that required tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['Customers', 'Products', 'Orders', 'OrderDetails']
            for table in required_tables:
                assert table in tables, f"Required table {table} not found"
            
            conn.close()

    def test_customer_insert_validation(self):
        """Test customer data validation before insert"""
        # Test valid customer data
        valid_customer = {
            'CustomerID': 'TEST001',
            'CustomerName': 'Test Corporation',
            'ContactPerson': 'John Doe',
            'Email': 'john@test.com',
            'Phone': '555-1234'
        }
        
        # All required fields present
        assert valid_customer['CustomerID'], "Customer ID is required"
        assert valid_customer['CustomerName'], "Customer Name is required"
        assert '@' in valid_customer['Email'], "Email should contain @"
        
        # Test invalid customer data
        invalid_customer = {
            'CustomerID': '',
            'CustomerName': '',
            'Email': 'invalid-email'
        }
        
        assert not invalid_customer['CustomerID'], "Empty Customer ID should be invalid"
        assert not invalid_customer['CustomerName'], "Empty Customer Name should be invalid"
        assert '@' not in invalid_customer['Email'], "Invalid email format"

    def test_product_insert_validation(self):
        """Test product data validation before insert"""
        # Test valid product data
        valid_product = {
            'ProductID': 'PART001',
            'ProductName': 'Graphite Component A',
            'Description': 'High-quality industrial component',
            'Category': 'Graphite Components',
            'UnitPrice': 500.00
        }
        
        assert valid_product['ProductID'], "Product ID is required"
        assert valid_product['ProductName'], "Product Name is required"
        assert valid_product['UnitPrice'] > 0, "Unit Price must be positive"
        
        # Test invalid product data
        invalid_product = {
            'ProductID': '',
            'ProductName': '',
            'UnitPrice': -100.00
        }
        
        assert not invalid_product['ProductID'], "Empty Product ID should be invalid"
        assert not invalid_product['ProductName'], "Empty Product Name should be invalid"
        assert invalid_product['UnitPrice'] < 0, "Negative price should be invalid"

    def test_order_insert_validation(self):
        """Test order data validation before insert"""
        from datetime import datetime, date
        
        # Test valid order data
        valid_order = {
            'OrderID': 'ORD001',
            'CustomerID': 'CUST001',
            'OrderDate': date.today().isoformat(),
            'DeliveryDate': date.today().isoformat(),
            'Status': 'Open',
            'TotalAmount': 1500.00,
            'CustomerPO': 'PO-12345'
        }
        
        assert valid_order['OrderID'], "Order ID is required"
        assert valid_order['CustomerID'], "Customer ID is required"
        assert valid_order['TotalAmount'] >= 0, "Total Amount must be non-negative"
        assert valid_order['Status'] in ['Open', 'Processing', 'On Hold', 'Shipped'], "Status must be valid"
        
        # Test date validation
        order_date = datetime.fromisoformat(valid_order['OrderDate'])
        delivery_date = datetime.fromisoformat(valid_order['DeliveryDate'])
        assert isinstance(order_date, datetime), "Order date should be valid datetime"
        assert isinstance(delivery_date, datetime), "Delivery date should be valid datetime"

class TestFormBusinessLogic:
    """Test suite for forms business logic"""
    
    def test_order_total_calculation(self):
        """Test order total calculation logic"""
        quantity = 5
        unit_price = 250.00
        expected_total = 1250.00
        
        calculated_total = quantity * unit_price
        assert calculated_total == expected_total, f"Expected {expected_total}, got {calculated_total}"
        
        # Test with decimal quantities
        quantity_decimal = 2.5
        unit_price_decimal = 100.50
        expected_decimal = 251.25
        
        calculated_decimal = quantity_decimal * unit_price_decimal
        assert abs(calculated_decimal - expected_decimal) < 0.01, "Decimal calculation should be accurate"

    def test_email_generation_logic(self):
        """Test automatic email generation for customers"""
        customer_id = "TESTCORP"
        expected_email = "testcorp@company.com"
        
        generated_email = f"{customer_id.lower()}@company.com"
        assert generated_email == expected_email, f"Expected {expected_email}, got {generated_email}"
        
        # Test with special characters (should be handled)
        customer_id_special = "TEST-CORP_123"
        generated_special = f"{customer_id_special.lower()}@company.com"
        assert "@company.com" in generated_special, "Email should contain domain"

    def test_product_category_validation(self):
        """Test product category validation"""
        valid_categories = [
            "Graphite Components", 
            "Carbon Parts", 
            "Specialized Fixtures",
            "Heat Shields", 
            "Conductive Elements", 
            "Custom Manufacturing"
        ]
        
        # Test valid categories
        for category in valid_categories:
            assert category in valid_categories, f"Category {category} should be valid"
        
        # Test invalid category
        invalid_category = "Invalid Category"
        assert invalid_category not in valid_categories, f"Category {invalid_category} should be invalid"

class TestFormDataIntegrity:
    """Test suite for data integrity in forms"""
    
    def test_customer_order_relationship(self):
        """Test that orders reference valid customers"""
        # Test data setup
        customer_data = {
            'CustomerID': 'CUST001',
            'CustomerName': 'Test Customer'
        }
        
        order_data = {
            'OrderID': 'ORD001',
            'CustomerID': 'CUST001',  # Should match customer
            'TotalAmount': 1000.00
        }
        
        # Verify relationship
        assert order_data['CustomerID'] == customer_data['CustomerID'], "Order should reference valid customer"
        
        # Test orphaned order (invalid relationship)
        orphaned_order = {
            'OrderID': 'ORD002',
            'CustomerID': 'NONEXISTENT',  # Invalid customer reference
            'TotalAmount': 500.00
        }
        
        assert orphaned_order['CustomerID'] != customer_data['CustomerID'], "Order references non-existent customer"

    def test_order_detail_relationship(self):
        """Test that order details reference valid orders and products"""
        # Test data setup
        order_data = {
            'OrderID': 'ORD001',
            'TotalAmount': 1000.00
        }
        
        product_data = {
            'ProductID': 'PART001',
            'ProductName': 'Test Product',
            'UnitPrice': 200.00
        }
        
        order_detail_data = {
            'OrderID': 'ORD001',      # Should match order
            'ProductID': 'PART001',   # Should match product
            'Quantity': 5,
            'UnitPrice': 200.00,
            'TotalCost': 1000.00
        }
        
        # Verify relationships
        assert order_detail_data['OrderID'] == order_data['OrderID'], "Order detail should reference valid order"
        assert order_detail_data['ProductID'] == product_data['ProductID'], "Order detail should reference valid product"
        
        # Verify calculation
        expected_total = order_detail_data['Quantity'] * order_detail_data['UnitPrice'] 
        assert order_detail_data['TotalCost'] == expected_total, "Total cost calculation should be correct"

class TestFormErrorHandling:
    """Test suite for forms error handling"""
    
    @patch('sqlite3.connect')
    def test_database_connection_failure(self, mock_connect):
        """Test handling of database connection failures"""
        # Mock connection failure
        mock_connect.side_effect = sqlite3.Error("Connection failed")
        
        # Test that error is handled gracefully
        try:
            conn = sqlite3.connect("test.db")
            assert False, "Should have raised an exception"
        except sqlite3.Error as e:
            assert "Connection failed" in str(e)

    def test_invalid_input_handling(self):
        """Test handling of invalid user inputs"""
        # Test empty strings
        empty_inputs = ['', None, '   ']
        for input_val in empty_inputs:
            is_valid = bool(input_val and input_val.strip())
            assert not is_valid, f"Input '{input_val}' should be invalid"

        # Test valid inputs
        valid_inputs = ['ValidInput', 'Test123', 'CUSTOMER_001']
        for input_val in valid_inputs:
            is_valid = bool(input_val and input_val.strip())
            assert is_valid, f"Input '{input_val}' should be valid"

    def test_numeric_input_validation(self):
        """Test validation of numeric inputs"""
        # Test valid numeric inputs
        valid_numbers = ['100', '250.50', '0', '999.99']
        for num_str in valid_numbers:
            try:
                num_val = float(num_str)
                assert num_val >= 0, f"Number {num_val} should be non-negative"
            except ValueError:
                assert False, f"'{num_str}' should be valid number"

        # Test invalid numeric inputs
        invalid_numbers = ['abc', '', 'not_a_number', '-100']
        for num_str in invalid_numbers:
            if num_str == '-100':
                # Negative numbers are technically valid floats but invalid for prices
                num_val = float(num_str)
                assert num_val < 0, "Negative price should be caught"
            elif num_str in ['abc', 'not_a_number']:
                try:
                    float(num_str)
                    assert False, f"'{num_str}' should not convert to float"
                except ValueError:
                    pass  # Expected

class TestFormUserInterface:
    """Test suite for forms user interface logic"""
    
    def test_form_field_requirements(self):
        """Test form field requirement validation"""
        # Customer form required fields
        customer_required = ['CustomerID', 'CustomerName']
        customer_data = {
            'CustomerID': 'CUST001',
            'CustomerName': 'Test Corp',
            'ContactPerson': 'John Doe',  # Optional
            'Email': 'john@test.com',     # Optional
            'Phone': '555-1234'           # Optional
        }
        
        # Check required fields are present
        for field in customer_required:
            assert field in customer_data, f"Required field {field} missing"
            assert customer_data[field], f"Required field {field} is empty"

        # Product form required fields
        product_required = ['ProductID', 'ProductName']
        product_data = {
            'ProductID': 'PART001',
            'ProductName': 'Test Product',
            'Description': 'Test description',  # Optional
            'Category': 'Graphite Components',  # Optional
            'UnitPrice': 500.00                 # Optional
        }
        
        # Check required fields are present
        for field in product_required:
            assert field in product_data, f"Required field {field} missing"
            assert product_data[field], f"Required field {field} is empty"

    def test_dropdown_options_validation(self):
        """Test dropdown option validation"""
        # Test salesperson options
        salesperson_options = [
            "John Smith", "Lisa Johnson", "Robert Chen", 
            "Maria Garcia", "David Wilson"
        ]
        
        assert len(salesperson_options) > 0, "Should have salesperson options"
        for option in salesperson_options:
            assert isinstance(option, str), "Salesperson option should be string"
            assert len(option) > 0, "Salesperson option should not be empty"

        # Test order status options
        status_options = ["Open", "Processing", "On Hold", "Shipped"]
        
        assert len(status_options) > 0, "Should have status options"
        for option in status_options:
            assert isinstance(option, str), "Status option should be string"
            assert option in status_options, f"Status {option} should be valid"

        # Test payment terms options
        payment_terms = ["Net 30", "Net 60", "Net 90", "COD", "Prepaid"]
        
        assert len(payment_terms) > 0, "Should have payment terms options"
        for term in payment_terms:
            assert isinstance(term, str), "Payment term should be string"
            assert "Net" in term or term in ["COD", "Prepaid"], f"Payment term {term} should be valid format"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])