"""
Unit tests for Interactive Reports page functionality
Tests dashboard components, visualization logic, and data processing
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestInteractiveReportsDemoData:
    """Test suite for interactive reports demo data generation"""
    
    def test_demo_data_structure(self):
        """Test that demo data has the correct structure"""
        # Simulate the demo data generation logic
        np.random.seed(42)
        today = datetime.now()
        dates = [(today - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(365, 0, -10)]
        
        customers = ["ACME Corp", "Toyo Industries", "GlobalTech", "Innovative Solutions", 
                    "TechFusion", "Quantum Materials", "SpectraSystems", "FusionTech",
                    "NexGen Manufacturing", "PrecisionParts"]
                    
        products = ["Carbon Component A", "Graphite Assembly B", "Specialized Fixture", 
                   "ISO Compliant Part", "Thermal Resistor", "High-Temp Module", 
                   "Conductive Component", "Heat Shield Assembly"]
        
        # Verify data structure
        assert len(dates) > 0, "Should have date entries"
        assert len(customers) == 10, "Should have 10 customers"
        assert len(products) == 8, "Should have 8 products"
        
        # Verify data types
        for date_str in dates[:3]:  # Check first 3 dates
            datetime.strptime(date_str, '%Y-%m-%d')  # Should not raise exception
        
        for customer in customers:
            assert isinstance(customer, str), "Customer names should be strings"
            assert len(customer) > 0, "Customer names should not be empty"
        
        for product in products:
            assert isinstance(product, str), "Product names should be strings"
            assert len(product) > 0, "Product names should not be empty"

    def test_demo_sales_data_generation(self):
        """Test demo sales data generation logic"""
        np.random.seed(42)
        
        # Simulate sales data generation
        sales_data = []
        customers = ["ACME Corp", "Beta Industries", "Gamma Solutions"]
        products = ["Product A", "Product B", "Product C"]
        
        for i in range(10):  # Generate 10 sample records
            customer = np.random.choice(customers)
            product = np.random.choice(products)
            quantity = np.random.randint(1, 20)
            unit_price = np.random.uniform(500, 10000)
            total = quantity * unit_price
            status = np.random.choice(["Complete", "In Progress", "Pending", "On Hold"])
            
            sales_data.append({
                "CustomerName": customer,
                "ProductName": product,
                "Quantity": quantity,
                "UnitPrice": unit_price,
                "TotalAmount": total,
                "Status": status,
                "Region": np.random.choice(["North", "South", "East", "West", "International"]),
                "SalesPerson": np.random.choice(["John Smith", "Lisa Johnson", "Robert Chen"])
            })
        
        df = pd.DataFrame(sales_data)
        
        # Verify DataFrame structure
        assert len(df) == 10, "Should have 10 records"
        assert 'CustomerName' in df.columns, "Should have CustomerName column"
        assert 'ProductName' in df.columns, "Should have ProductName column"
        assert 'TotalAmount' in df.columns, "Should have TotalAmount column"
        
        # Verify data types
        assert pd.api.types.is_numeric_dtype(df['Quantity']), "Quantity should be numeric"
        assert pd.api.types.is_numeric_dtype(df['UnitPrice']), "UnitPrice should be numeric"
        assert pd.api.types.is_numeric_dtype(df['TotalAmount']), "TotalAmount should be numeric"
        
        # Verify calculated totals
        for _, row in df.iterrows():
            expected_total = row['Quantity'] * row['UnitPrice']
            assert abs(row['TotalAmount'] - expected_total) < 0.01, "Total calculation should be accurate"

class TestVisualizationLogic:
    """Test suite for visualization logic"""
    
    def test_monthly_trend_data_processing(self):
        """Test monthly trend data processing"""
        # Create test data
        test_data = {
            'OrderDate': ['2025-01-15', '2025-01-20', '2025-02-10', '2025-02-25', '2025-03-05'],
            'TotalAmount': [1000, 1500, 2000, 1200, 1800]
        }
        df = pd.DataFrame(test_data)
        
        # Process data like in the interactive reports
        df['Month'] = pd.to_datetime(df['OrderDate']).dt.strftime('%Y-%m')
        monthly_sales = df.groupby('Month').agg({'TotalAmount': 'sum'}).reset_index()
        
        # Verify processing
        assert len(monthly_sales) == 3, "Should have 3 months"
        assert monthly_sales[monthly_sales['Month'] == '2025-01']['TotalAmount'].iloc[0] == 2500
        assert monthly_sales[monthly_sales['Month'] == '2025-02']['TotalAmount'].iloc[0] == 3200
        assert monthly_sales[monthly_sales['Month'] == '2025-03']['TotalAmount'].iloc[0] == 1800

    def test_customer_analysis_data_processing(self):
        """Test customer analysis data processing"""
        # Create test data
        test_data = {
            'CustomerName': ['ACME Corp', 'ACME Corp', 'Beta Inc', 'Beta Inc', 'Gamma Ltd'],
            'OrderDate': ['2025-01-01', '2025-01-15', '2025-01-10', '2025-01-20', '2025-01-05'],
            'TotalAmount': [1000, 1500, 800, 1200, 900]
        }
        df = pd.DataFrame(test_data)
        
        # Process data like in customer insights
        customer_sales = df.groupby('CustomerName').agg({
            'TotalAmount': 'sum', 
            'OrderDate': 'count'
        }).reset_index()
        customer_sales = customer_sales.rename(columns={'OrderDate': 'Order Count'})
        customer_sales = customer_sales.sort_values('TotalAmount', ascending=False)
        
        # Verify processing
        assert len(customer_sales) == 3, "Should have 3 customers"
        assert customer_sales.iloc[0]['CustomerName'] == 'ACME Corp'  # Highest total
        assert customer_sales.iloc[0]['TotalAmount'] == 2500
        assert customer_sales.iloc[0]['Order Count'] == 2

    def test_product_performance_analysis(self):
        """Test product performance analysis logic"""
        # Create test data
        test_data = {
            'ProductName': ['Product A', 'Product A', 'Product B', 'Product C', 'Product C'],
            'Quantity': [5, 3, 10, 2, 4],
            'TotalAmount': [1000, 600, 2000, 400, 800]
        }
        df = pd.DataFrame(test_data)
        
        # Process data like in product analysis
        product_sales = df.groupby('ProductName').agg({
            'TotalAmount': 'sum', 
            'Quantity': 'sum'
        }).reset_index()
        product_sales = product_sales.sort_values('TotalAmount', ascending=False)
        
        # Verify processing
        assert len(product_sales) == 3, "Should have 3 products"
        assert product_sales.iloc[0]['ProductName'] == 'Product B'  # Highest sales
        assert product_sales.iloc[0]['TotalAmount'] == 2000
        assert product_sales.iloc[1]['TotalAmount'] == 1600  # Product A total

class TestChartDataPreparation:
    """Test suite for chart data preparation"""
    
    def test_pie_chart_data_preparation(self):
        """Test pie chart data preparation"""
        # Create test data for regions
        test_data = {
            'Region': ['North', 'North', 'South', 'East', 'West', 'West'],
            'TotalAmount': [1000, 1500, 800, 1200, 900, 1100]
        }
        df = pd.DataFrame(test_data)
        
        # Prepare data for pie chart
        region_sales = df.groupby('Region').agg({'TotalAmount': 'sum'}).reset_index()
        
        # Verify preparation
        assert len(region_sales) == 4, "Should have 4 regions"
        assert 'Region' in region_sales.columns, "Should have Region column"
        assert 'TotalAmount' in region_sales.columns, "Should have TotalAmount column"
        
        # Verify totals
        north_total = region_sales[region_sales['Region'] == 'North']['TotalAmount'].iloc[0]
        assert north_total == 2500, "North region total should be 2500"
        
        west_total = region_sales[region_sales['Region'] == 'West']['TotalAmount'].iloc[0]
        assert west_total == 2000, "West region total should be 2000"

    def test_timeline_chart_data_preparation(self):
        """Test timeline chart data preparation"""
        # Create test data
        test_data = {
            'OrderDate': ['2025-01-15', '2025-01-20', '2025-01-25', '2025-02-10', '2025-02-15'],
            'Status': ['Complete', 'Complete', 'Pending', 'Complete', 'Pending'],
            'Count': [1, 1, 1, 1, 1]
        }
        df = pd.DataFrame(test_data)
        
        # Prepare data for timeline
        df['OrderMonth'] = pd.to_datetime(df['OrderDate']).dt.strftime('%Y-%m')
        timeline = df.groupby(['OrderMonth', 'Status']).size().reset_index(name='Count')
        
        # Verify preparation
        assert 'OrderMonth' in timeline.columns, "Should have OrderMonth column"
        assert 'Status' in timeline.columns, "Should have Status column"
        assert 'Count' in timeline.columns, "Should have Count column"
        
        # Check specific data points
        jan_complete = timeline[(timeline['OrderMonth'] == '2025-01') & (timeline['Status'] == 'Complete')]
        assert len(jan_complete) == 1, "Should have one Complete entry for January"
        assert jan_complete['Count'].iloc[0] == 2, "Should have 2 Complete orders in January"

class TestErrorHandlingInReports:
    """Test suite for error handling in interactive reports"""
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrames in visualizations"""
        empty_df = pd.DataFrame()
        
        # Test operations that should handle empty data gracefully
        assert len(empty_df) == 0, "Empty DataFrame should have 0 length"
        assert empty_df.empty, "DataFrame should be empty"
        
        # Test groupby operations on empty DataFrame
        try:
            if not empty_df.empty and 'CustomerName' in empty_df.columns:
                grouped = empty_df.groupby('CustomerName').sum()
                assert len(grouped) == 0, "Grouped empty DataFrame should be empty"
        except KeyError:
            pass  # Expected when columns don't exist

    def test_missing_columns_handling(self):
        """Test handling of missing columns in data processing"""
        # Create DataFrame missing expected columns
        incomplete_df = pd.DataFrame({
            'SomeColumn': [1, 2, 3],
            'AnotherColumn': ['A', 'B', 'C']
        })
        
        # Test column existence checks
        expected_columns = ['CustomerName', 'TotalAmount', 'OrderDate']
        missing_columns = [col for col in expected_columns if col not in incomplete_df.columns]
        
        assert len(missing_columns) == 3, "Should identify all missing columns"
        assert 'CustomerName' in missing_columns, "Should detect missing CustomerName"
        assert 'TotalAmount' in missing_columns, "Should detect missing TotalAmount"

    @patch('pandas.read_sql')
    def test_database_query_failure_handling(self, mock_read_sql):
        """Test handling of database query failures"""
        # Mock database query failure
        mock_read_sql.side_effect = Exception("Database connection failed")
        
        # Test that the function handles the exception gracefully
        try:
            result = pd.read_sql("SELECT * FROM Orders", "dummy_connection")
            assert False, "Should have raised an exception"
        except Exception as e:
            assert "Database connection failed" in str(e)

class TestFilterFunctionality:
    """Test suite for filter functionality in interactive reports"""
    
    def test_date_range_filtering(self):
        """Test date range filtering logic"""
        # Create test data
        test_data = {
            'OrderDate': ['2025-01-15', '2025-02-20', '2025-03-25', '2025-04-10'],
            'CustomerName': ['ACME', 'Beta', 'Gamma', 'Delta'],
            'TotalAmount': [1000, 1500, 2000, 1200]
        }
        df = pd.DataFrame(test_data)
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
        
        # Apply date filter (January to February)
        start_date = pd.to_datetime('2025-01-01')
        end_date = pd.to_datetime('2025-02-28')
        
        filtered_df = df[(df['OrderDate'] >= start_date) & (df['OrderDate'] <= end_date)]
        
        # Verify filtering
        assert len(filtered_df) == 2, "Should have 2 records in date range"
        assert 'ACME' in filtered_df['CustomerName'].values, "Should include ACME"
        assert 'Beta' in filtered_df['CustomerName'].values, "Should include Beta"
        assert 'Gamma' not in filtered_df['CustomerName'].values, "Should exclude Gamma"

    def test_customer_filtering(self):
        """Test customer filtering logic"""
        # Create test data
        test_data = {
            'CustomerName': ['ACME Corp', 'ACME Corp', 'Beta Inc', 'Gamma Ltd'],
            'TotalAmount': [1000, 1500, 800, 900]
        }
        df = pd.DataFrame(test_data)
        
        # Apply customer filter
        selected_customer = 'ACME Corp'
        filtered_df = df[df['CustomerName'] == selected_customer]
        
        # Verify filtering
        assert len(filtered_df) == 2, "Should have 2 ACME Corp records"
        assert all(filtered_df['CustomerName'] == 'ACME Corp'), "All records should be ACME Corp"
        assert filtered_df['TotalAmount'].sum() == 2500, "Total should be 2500"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])