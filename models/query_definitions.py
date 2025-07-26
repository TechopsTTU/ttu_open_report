import os
import pyodbc
import pandas as pd
import logging
import sqlite3
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_sqlite_connection():
    """Connects to the SQLite test database."""
    db_path = Path("graphite_analytics.db")
    if not db_path.exists():
        raise FileNotFoundError(f"SQLite database not found: {db_path}. Run create_test_db.py first.")
    
    try:
        conn = sqlite3.connect(str(db_path))
        logging.info("SQLite database connection established.")
        return conn
    except Exception as e:
        logging.error(f"SQLite database connection failed: {e}")
        raise

def build_connection_string():
    """Builds the ODBC connection string from environment variables."""
    drv = os.getenv("NDUSTROS_DRIVER", "Pervasive ODBC Client Interface")
    srv = os.getenv("NDUSTROS_SERVER", "PLATSRVR")
    port = os.getenv("NDUSTROS_PORT", "1583")
    dbq = os.getenv("NDUSTROS_DB", "NdustrOS")
    user = os.getenv("NDUSTROS_USER")
    pwd = os.getenv("NDUSTROS_PASS")
    if not user or not pwd:
        raise ValueError("NDUSTROS_USER and NDUSTROS_PASS must be set")
    return (
        f"Driver={{{drv}}};"
        f"ServerName={srv};Port={port};DBQ={dbq};"
        f"uid={user};pwd={pwd}"
    )

def get_ds_connection():
    """Attempts to connect to the NdustrOS database using ODBC."""
    conn_str = build_connection_string()
    try:
        conn = pyodbc.connect(conn_str)
        logging.info("Database connection established.")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

def run_pass_through(sql: str) -> pd.DataFrame:
    """Executes a SQL query and returns the result as a DataFrame."""
    # Check if we're in development mode (use SQLite)
    use_sqlite = os.getenv("USE_SQLITE", "true").lower() == "true"
    
    try:
        if use_sqlite:
            with get_sqlite_connection() as conn:
                df = pd.read_sql(sql, conn)
        else:
            with get_ds_connection() as conn:
                df = pd.read_sql(sql, conn)
        logging.info("Query executed successfully.")
        return df
    except Exception as e:
        logging.error(f"Query execution failed: {e}")
        raise

def q010_open_order_report_data() -> pd.DataFrame:
    """Returns Open Order Report data from database."""
    sql = """
    SELECT 
        o.OrderID,
        o.OrderDate,
        c.CompanyName as Customer,
        o.Status,
        SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) as Amount
    FROM Orders o
    JOIN Customers c ON o.CustomerID = c.CustomerID
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    WHERE o.Status IN ('Open', 'Processing')
    GROUP BY o.OrderID, o.OrderDate, c.CompanyName, o.Status
    ORDER BY o.OrderDate DESC
    """
    return run_pass_through(sql)

def q093_shipment_status() -> pd.DataFrame:
    """Returns Shipment Status data from database."""
    sql = """
    SELECT 
        s.ShipmentID,
        s.OrderID,
        s.ShippedDate,
        s.Status,
        s.TrackingNumber,
        s.Carrier,
        s.DeliveryDate
    FROM Shipments s
    JOIN Orders o ON s.OrderID = o.OrderID
    ORDER BY s.ShippedDate DESC
    """
    return run_pass_through(sql)

def test_connection():
    """Tests the database connection and logs the result."""
    try:
        with get_ds_connection() as conn:
            logging.info("Connection successful!")
    except Exception as e:
        logging.error(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
