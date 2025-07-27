"""
Create SQLite database with real data from Access database
Replaces fake data with actual business data from Opnordrp-vlad-copy.accdb
"""
import sqlite3
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def create_real_data_database():
    """Create SQLite database with real data from extracted Access database"""
    
    # Database file path
    db_path = "graphite_analytics.db"
    
    # Remove existing database
    if Path(db_path).exists():
        Path(db_path).unlink()
        logging.info("Removed existing database")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create Customers table (extracted from OO_ReportData)
        logging.info("Creating Customers table...")
        cursor.execute("""
        CREATE TABLE Customers (
            CustomerID TEXT PRIMARY KEY,
            CustomerName TEXT NOT NULL,
            ContactPerson TEXT,
            Email TEXT,
            Phone TEXT,
            SalespersonKey TEXT,
            SalespersonName TEXT
        )
        """)
        
        # Create Products table (extracted from OO_ReportData)
        logging.info("Creating Products table...")
        cursor.execute("""
        CREATE TABLE Products (
            ProductID TEXT PRIMARY KEY,
            ProductName TEXT NOT NULL,
            Description TEXT,
            Category TEXT,
            UnitPrice REAL
        )
        """)
        
        # Create Orders table (extracted from OO_ReportData)
        logging.info("Creating Orders table...")
        cursor.execute("""
        CREATE TABLE Orders (
            OrderID TEXT PRIMARY KEY,
            CustomerID TEXT,
            OrderDate TEXT,
            DeliveryDate TEXT,
            CustomerReqDate TEXT,
            Status TEXT,
            TotalAmount REAL,
            CustomerPO TEXT,
            SalespersonKey TEXT,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
        )
        """)
        
        # Create OrderDetails table (extracted from OO_ReportData)
        logging.info("Creating OrderDetails table...")
        cursor.execute("""
        CREATE TABLE OrderDetails (
            OrderDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
            OrderID TEXT,
            ProductID TEXT,
            Quantity REAL,
            UnitPrice REAL,
            TotalCost REAL,
            QtyOnHand REAL,
            SystemLineSeq INTEGER,
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        )
        """)
        
        # Create Shipments table (will use zzztblShipmentStatus data)
        logging.info("Creating Shipments table...")
        cursor.execute("""
        CREATE TABLE Shipments (
            ShipmentID INTEGER PRIMARY KEY AUTOINCREMENT,
            OrderID TEXT,
            ShippedDate TEXT,
            DeliveryDate TEXT,
            TrackingNumber TEXT,
            Status TEXT,
            Carrier TEXT,
            ShipLate TEXT,
            ShipLateAmount REAL,
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
        )
        """)
        
        # Load and process real data from OO_ReportData.csv
        logging.info("Loading real data from OO_ReportData.csv...")
        
        if not Path("extracted_data/OO_ReportData.csv").exists():
            logging.error("OO_ReportData.csv not found. Please run the extraction first.")
            return
        
        # Read the main open orders data
        df_orders = pd.read_csv("extracted_data/OO_ReportData.csv")
        logging.info(f"Loaded {len(df_orders)} order records")
        
        # Extract unique customers
        customers_data = df_orders.groupby('Custkey').agg({
            'Custname': 'first',
            'Salesp_Key': 'first', 
            'Salesp_Name': 'first'
        }).reset_index()
        
        logging.info(f"Inserting {len(customers_data)} customers...")
        for _, customer in customers_data.iterrows():
            cursor.execute("""
            INSERT OR REPLACE INTO Customers 
            (CustomerID, CustomerName, SalespersonKey, SalespersonName, ContactPerson, Email, Phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                customer['Custkey'].strip(),
                customer['Custname'].strip(),
                customer['Salesp_Key'].strip() if pd.notna(customer['Salesp_Key']) else None,
                customer['Salesp_Name'].strip() if pd.notna(customer['Salesp_Name']) else None,
                "Production Manager",  # Default contact
                f"{customer['Custkey'].strip().lower()}@company.com",  # Generated email
                "555-0100"  # Default phone
            ))
        
        # Extract unique products
        products_data = df_orders.groupby('Itemkey').agg({
            'Desc': 'first',
            'Unitprice': 'first'
        }).reset_index()
        
        logging.info(f"Inserting {len(products_data)} products...")
        for _, product in products_data.iterrows():
            cursor.execute("""
            INSERT OR REPLACE INTO Products 
            (ProductID, ProductName, Description, Category, UnitPrice)
            VALUES (?, ?, ?, ?, ?)
            """, (
                product['Itemkey'].strip(),
                product['Itemkey'].strip(),  # Use ItemKey as product name
                product['Desc'].strip() if pd.notna(product['Desc']) else "Custom Part",
                "Manufacturing Components",  # Default category
                float(product['Unitprice']) if pd.notna(product['Unitprice']) else 0.0
            ))
        
        # Extract unique orders
        orders_data = df_orders.groupby('Ordno').agg({
            'Custkey': 'first',
            'O_Date': 'first',
            'D_Date': 'first', 
            'CustReqDate': 'first',
            'Statusflg': 'first',
            'TotalCost': 'sum',
            'Custpono': 'first',
            'Salesp_Key': 'first'
        }).reset_index()
        
        logging.info(f"Inserting {len(orders_data)} orders...")
        for _, order in orders_data.iterrows():
            cursor.execute("""
            INSERT OR REPLACE INTO Orders 
            (OrderID, CustomerID, OrderDate, DeliveryDate, CustomerReqDate, Status, TotalAmount, CustomerPO, SalespersonKey)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(order['Ordno']).strip(),
                order['Custkey'].strip(),
                order['O_Date'],
                order['D_Date'],
                order['CustReqDate'],
                "Open" if order['Statusflg'] == 'BN' else "Processing",  # Convert status
                float(order['TotalCost']) if pd.notna(order['TotalCost']) else 0.0,
                order['Custpono'].strip() if pd.notna(order['Custpono']) else "",
                order['Salesp_Key'].strip() if pd.notna(order['Salesp_Key']) else None
            ))
        
        # Insert order details
        logging.info(f"Inserting {len(df_orders)} order details...")
        for _, detail in df_orders.iterrows():
            cursor.execute("""
            INSERT INTO OrderDetails 
            (OrderID, ProductID, Quantity, UnitPrice, TotalCost, QtyOnHand, SystemLineSeq)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(detail['Ordno']).strip(),
                detail['Itemkey'].strip(),
                float(detail['Qtyremn']) if pd.notna(detail['Qtyremn']) else 1.0,
                float(detail['Unitprice']) if pd.notna(detail['Unitprice']) else 0.0,
                float(detail['TotalCost']) if pd.notna(detail['TotalCost']) else 0.0,
                float(detail['Qtyonhand']) if pd.notna(detail['Qtyonhand']) else 0.0,
                int(detail['Syslinsq']) if pd.notna(detail['Syslinsq']) else 1
            ))
        
        # Load shipment data if available
        shipment_file = Path("extracted_data/zzztblShipmentStatus.csv")
        if shipment_file.exists():
            logging.info("Loading shipment data from zzztblShipmentStatus.csv...")
            df_shipments = pd.read_csv(shipment_file)
            
            # Take a sample of shipments to avoid too much data
            df_shipments_sample = df_shipments.head(1000)  # Use first 1000 shipments
            
            logging.info(f"Inserting {len(df_shipments_sample)} shipment records...")
            for _, shipment in df_shipments_sample.iterrows():
                try:
                    cursor.execute("""
                    INSERT INTO Shipments 
                    (OrderID, ShippedDate, DeliveryDate, Status, ShipLate, ShipLateAmount)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        str(shipment['Ordno']).strip() if pd.notna(shipment['Ordno']) else None,
                        shipment['Shipdate'] if pd.notna(shipment['Shipdate']) else None,
                        shipment['S_Date'] if pd.notna(shipment['S_Date']) else None,
                        "Shipped" if pd.notna(shipment['Shipdate']) else "Pending",
                        str(shipment['ShipLate']).strip() if pd.notna(shipment['ShipLate']) else "",
                        float(shipment['ShipLateAmount']) if pd.notna(shipment['ShipLateAmount']) else 0.0
                    ))
                except Exception as e:
                    logging.warning(f"Skipped shipment record: {e}")
                    continue
        
        # Commit all changes
        conn.commit()
        
        # Verify data
        logging.info("Verifying inserted data...")
        cursor.execute("SELECT COUNT(*) FROM Customers")
        customers_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Products") 
        products_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Orders")
        orders_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM OrderDetails")
        order_details_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Shipments")
        shipments_count = cursor.fetchone()[0]
        
        logging.info(f"✅ Database created successfully!")
        logging.info(f"   📋 Customers: {customers_count}")
        logging.info(f"   📦 Products: {products_count}")
        logging.info(f"   📄 Orders: {orders_count}")
        logging.info(f"   📝 Order Details: {order_details_count}")
        logging.info(f"   🚚 Shipments: {shipments_count}")
        
    except Exception as e:
        logging.error(f"Error creating database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    create_real_data_database()
