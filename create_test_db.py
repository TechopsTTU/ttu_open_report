"""
Database setup for GraphiteVision Analytics
Creates SQLite database with sample data for development/testing
"""
import sqlite3
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def create_sample_database():
    """Creates SQLite database with sample business data."""
    db_path = Path("graphite_analytics.db")
    
    # Remove existing database
    if db_path.exists():
        db_path.unlink()
        logging.info("Removed existing database")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create Customers table
    cursor.execute("""
    CREATE TABLE Customers (
        CustomerID INTEGER PRIMARY KEY,
        CompanyName TEXT NOT NULL,
        ContactName TEXT,
        ContactTitle TEXT,
        Address TEXT,
        City TEXT,
        Region TEXT,
        PostalCode TEXT,
        Country TEXT,
        Phone TEXT,
        Fax TEXT,
        Industry TEXT,
        CustomerType TEXT
    )
    """)
    
    # Create Products table
    cursor.execute("""
    CREATE TABLE Products (
        ProductID INTEGER PRIMARY KEY,
        ProductName TEXT NOT NULL,
        CategoryID INTEGER,
        SupplierID INTEGER,
        QuantityPerUnit TEXT,
        UnitPrice DECIMAL(10,2),
        UnitsInStock INTEGER,
        UnitsOnOrder INTEGER,
        ReorderLevel INTEGER,
        Discontinued INTEGER,
        GraphiteGrade TEXT,
        MaterialType TEXT
    )
    """)
    
    # Create Orders table
    cursor.execute("""
    CREATE TABLE Orders (
        OrderID INTEGER PRIMARY KEY,
        CustomerID INTEGER,
        EmployeeID INTEGER,
        OrderDate DATE,
        RequiredDate DATE,
        ShippedDate DATE,
        ShipVia INTEGER,
        Freight DECIMAL(10,2),
        ShipName TEXT,
        ShipAddress TEXT,
        ShipCity TEXT,
        ShipRegion TEXT,
        ShipPostalCode TEXT,
        ShipCountry TEXT,
        Status TEXT,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    )
    """)
    
    # Create OrderDetails table
    cursor.execute("""
    CREATE TABLE OrderDetails (
        OrderDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderID INTEGER,
        ProductID INTEGER,
        UnitPrice DECIMAL(10,2),
        Quantity INTEGER,
        Discount REAL,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    )
    """)
    
    # Create Shipments table
    cursor.execute("""
    CREATE TABLE Shipments (
        ShipmentID INTEGER PRIMARY KEY,
        OrderID INTEGER,
        ShippedDate DATE,
        TrackingNumber TEXT,
        Carrier TEXT,
        Status TEXT,
        DeliveryDate DATE,
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
    )
    """)
    
    # Insert sample customers
    customers_data = [
        (1, 'Aerospace Components Inc', 'John Smith', 'Purchasing Manager', '123 Aviation Blvd', 'Seattle', 'WA', '98101', 'USA', '206-555-0001', '206-555-0002', 'Aerospace', 'Corporate'),
        (2, 'Tesla Manufacturing', 'Sarah Johnson', 'Materials Engineer', '456 Electric Ave', 'Austin', 'TX', '78701', 'USA', '512-555-0003', '512-555-0004', 'Automotive', 'Corporate'),
        (3, 'Samsung Electronics', 'Kim Park', 'Supply Chain Director', '789 Tech Drive', 'San Jose', 'CA', '95101', 'USA', '408-555-0005', '408-555-0006', 'Electronics', 'Enterprise'),
        (4, 'Boeing Defense Systems', 'Michael Chen', 'Senior Buyer', '321 Defense Way', 'Chicago', 'IL', '60601', 'USA', '312-555-0007', '312-555-0008', 'Defense', 'Government'),
        (5, 'General Electric', 'Lisa Williams', 'Materials Specialist', '654 Industrial Pkwy', 'Cincinnati', 'OH', '45201', 'USA', '513-555-0009', '513-555-0010', 'Industrial', 'Corporate')
    ]
    
    cursor.executemany("""
    INSERT INTO Customers (CustomerID, CompanyName, ContactName, ContactTitle, Address, City, Region, PostalCode, Country, Phone, Fax, Industry, CustomerType)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, customers_data)
    
    # Insert sample products
    products_data = [
        (1, 'High Purity Graphite Block', 1, 1, '10kg blocks', 450.00, 50, 20, 10, 0, 'Grade A', 'Synthetic'),
        (2, 'Graphite Electrode 18 inch', 1, 1, 'Single unit', 1200.00, 25, 10, 5, 0, 'UHP', 'Ultra High Power'),
        (3, 'Flexible Graphite Sheet', 2, 2, '1m x 1m sheets', 85.00, 200, 50, 25, 0, 'Grade B', 'Flexible'),
        (4, 'Graphite Crucible Large', 3, 1, 'Single unit', 320.00, 30, 15, 8, 0, 'Grade C', 'Molded'),
        (5, 'Carbon Fiber Reinforced', 4, 3, '5kg rolls', 750.00, 40, 20, 10, 0, 'Premium', 'Composite'),
        (6, 'Graphite Powder Fine', 2, 2, '25kg bags', 65.00, 100, 25, 15, 0, 'Standard', 'Natural'),
        (7, 'Isostatic Graphite Rod', 1, 1, '2m lengths', 280.00, 35, 12, 8, 0, 'ISO Grade', 'Isostatic'),
        (8, 'Graphite Heat Exchanger', 5, 3, 'Complete unit', 2500.00, 8, 3, 2, 0, 'Industrial', 'Machined')
    ]
    
    cursor.executemany("""
    INSERT INTO Products (ProductID, ProductName, CategoryID, SupplierID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued, GraphiteGrade, MaterialType)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, products_data)
    
    # Insert sample orders
    orders_data = [
        (1001, 1, 1, '2025-07-01', '2025-07-15', '2025-07-10', 1, 125.50, 'Aerospace Components Inc', '123 Aviation Blvd', 'Seattle', 'WA', '98101', 'USA', 'Shipped'),
        (1002, 2, 2, '2025-07-02', '2025-07-16', '2025-07-12', 2, 85.25, 'Tesla Manufacturing', '456 Electric Ave', 'Austin', 'TX', '78701', 'USA', 'Shipped'),
        (1003, 3, 1, '2025-07-03', '2025-07-17', None, 1, 200.75, 'Samsung Electronics', '789 Tech Drive', 'San Jose', 'CA', '95101', 'USA', 'Processing'),
        (1004, 4, 3, '2025-07-04', '2025-07-18', None, 3, 95.00, 'Boeing Defense Systems', '321 Defense Way', 'Chicago', 'IL', '60601', 'USA', 'Open'),
        (1005, 5, 2, '2025-07-05', '2025-07-19', '2025-07-14', 1, 150.25, 'General Electric', '654 Industrial Pkwy', 'Cincinnati', 'OH', '45201', 'USA', 'Shipped'),
        (1006, 1, 1, '2025-07-06', '2025-07-20', None, 2, 75.50, 'Aerospace Components Inc', '123 Aviation Blvd', 'Seattle', 'WA', '98101', 'USA', 'Open'),
        (1007, 3, 3, '2025-07-07', '2025-07-21', None, 1, 300.00, 'Samsung Electronics', '789 Tech Drive', 'San Jose', 'CA', '95101', 'USA', 'Processing'),
        (1008, 2, 2, '2025-07-08', '2025-07-22', '2025-07-16', 3, 45.75, 'Tesla Manufacturing', '456 Electric Ave', 'Austin', 'TX', '78701', 'USA', 'Shipped')
    ]
    
    cursor.executemany("""
    INSERT INTO Orders (OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry, Status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, orders_data)
    
    # Insert sample order details
    order_details_data = [
        (1001, 1, 450.00, 2, 0.0),
        (1001, 3, 85.00, 10, 0.05),
        (1002, 2, 1200.00, 1, 0.0),
        (1002, 6, 65.00, 5, 0.0),
        (1003, 4, 320.00, 3, 0.10),
        (1003, 7, 280.00, 2, 0.0),
        (1004, 8, 2500.00, 1, 0.0),
        (1005, 1, 450.00, 1, 0.0),
        (1005, 5, 750.00, 2, 0.05),
        (1006, 3, 85.00, 15, 0.0),
        (1007, 2, 1200.00, 2, 0.10),
        (1008, 6, 65.00, 8, 0.0)
    ]
    
    cursor.executemany("""
    INSERT INTO OrderDetails (OrderID, ProductID, UnitPrice, Quantity, Discount)
    VALUES (?, ?, ?, ?, ?)
    """, order_details_data)
    
    # Insert sample shipments
    shipments_data = [
        (501, 1001, '2025-07-10', 'TN123456789', 'FedEx', 'Delivered', '2025-07-12'),
        (502, 1002, '2025-07-12', 'TN987654321', 'UPS', 'Delivered', '2025-07-14'),
        (503, 1005, '2025-07-14', 'TN456789123', 'FedEx', 'Delivered', '2025-07-16'),
        (504, 1008, '2025-07-16', 'TN789123456', 'DHL', 'In Transit', None),
        (505, 1003, '2025-07-18', 'TN321654987', 'UPS', 'Processing', None)
    ]
    
    cursor.executemany("""
    INSERT INTO Shipments (ShipmentID, OrderID, ShippedDate, TrackingNumber, Carrier, Status, DeliveryDate)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, shipments_data)
    
    conn.commit()
    conn.close()
    
    logging.info(f"Created SQLite database: {db_path}")
    logging.info("Database populated with sample graphite manufacturing data")
    
    return str(db_path)

if __name__ == "__main__":
    create_sample_database()
