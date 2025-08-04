"""
Table and column mapping between development (SQLite) and production (Pervasive) databases.
This module provides mappings to translate queries from development schema to production schema.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Table name mappings: development -> production
TABLE_MAPPINGS = {
    'sqlite': {
        'Orders': 'Orders',
        'OrderDetails': 'OrderDetails', 
        'Products': 'Products',
        'Customers': 'Customers',
        'Shipments': 'Shipments'
    },
    'pervasive': {
        'Orders': 'OEHDR',
        'OrderDetails': 'OELIN',
        'Products': 'INVITEM',  # We'll need to identify the item master table
        'Customers': 'ARCUST',
        'Shipments': 'OESHIPTO'  # Ship-to table
    }
}

# Column name mappings for key tables
COLUMN_MAPPINGS = {
    'sqlite': {
        'Orders': {
            'OrderID': 'OrderID',
            'CustomerID': 'CustomerID',
            'OrderDate': 'OrderDate',
            'ShipDate': 'ShipDate',
            'Status': 'Status'
        },
        'OrderDetails': {
            'OrderID': 'OrderID',
            'ProductID': 'ProductID',
            'Quantity': 'Quantity',
            'UnitPrice': 'UnitPrice',
            'TotalCost': 'TotalCost'
        },
        'Products': {
            'ProductID': 'ProductID',
            'ProductName': 'ProductName'
        },
        'Customers': {
            'CustomerID': 'CustomerID',
            'CustomerName': 'CustomerName'
        }
    },
    'pervasive': {
        'Orders': {
            'OrderID': 'Ordernumber',
            'CustomerID': 'Customerkey', 
            'OrderDate': 'Orderdate',
            'ShipDate': 'Shipdate',
            'Status': 'Orderstatus'
        },
        'OrderDetails': {
            'OrderID': 'Ordernumber',
            'ProductID': 'Itemkey',
            'Quantity': 'Qtyordered',
            'UnitPrice': 'Unitprice', 
            'TotalCost': '(Qtyordered * Unitprice)'  # Calculated field
        },
        'Products': {
            'ProductID': 'Itemkey',
            'ProductName': 'Itemdescription'
        },
        'Customers': {
            'CustomerID': 'Customerkey',
            'CustomerName': 'Customername'
        }
    }
}

def get_database_type():
    """Get the current database type from environment."""
    db_env = os.getenv("DATABASE_ENV", "sqlite").lower()
    return db_env if db_env in ['sqlite', 'pervasive'] else 'sqlite'

def get_table_name(logical_table_name):
    """Get the physical table name for the current database type."""
    db_type = get_database_type()
    return TABLE_MAPPINGS[db_type].get(logical_table_name, logical_table_name)

def get_column_name(logical_table_name, logical_column_name):
    """Get the physical column name for the current database type."""
    db_type = get_database_type()
    table_mapping = COLUMN_MAPPINGS[db_type].get(logical_table_name, {})
    return table_mapping.get(logical_column_name, logical_column_name)

def translate_query(sql_query):
    """
    Translate a query from development schema to production schema.
    This is a basic implementation - for complex queries, consider using a proper SQL parser.
    """
    db_type = get_database_type()
    if db_type == 'sqlite':
        return sql_query  # No translation needed
    
    # For Pervasive, translate table and column names
    translated_query = sql_query
    
    # Replace table names
    for logical_table, physical_table in TABLE_MAPPINGS['pervasive'].items():
        # Replace table references (with word boundaries to avoid partial matches)
        import re
        pattern = r'\b' + re.escape(logical_table) + r'\b'
        translated_query = re.sub(pattern, physical_table, translated_query, flags=re.IGNORECASE)
    
    # Replace column references (more complex - would need proper SQL parsing for production)
    # For now, we'll handle the most common patterns
    
    return translated_query

def get_sample_production_query():
    """Get a sample query that works with production data."""
    return """
    SELECT TOP 10
        h.Ordernumber as OrderID,
        h.Customername as CustomerName, 
        h.Orderdate as OrderDate,
        l.Itemkey as ProductID,
        l.Itemdescription as ProductName,
        l.Qtyordered as Quantity,
        l.Unitprice as UnitPrice,
        (l.Qtyordered * l.Unitprice) as TotalCost
    FROM OEHDR h 
    INNER JOIN OELIN l ON h.Ordernumber = l.Ordernumber
    WHERE h.Orderstatus <> 'C'
    ORDER BY h.Orderdate DESC
    """

if __name__ == "__main__":
    # Test the mappings
    print(f"Database type: {get_database_type()}")
    print(f"Orders table: {get_table_name('Orders')}")
    print(f"OrderDetails table: {get_table_name('OrderDetails')}")
    print(f"Sample query:")
    print(get_sample_production_query())