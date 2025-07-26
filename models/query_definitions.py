import os
import pyodbc
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

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
    try:
        with get_ds_connection() as conn:
            df = pd.read_sql(sql, conn)
        logging.info("Query executed successfully.")
        return df
    except Exception as e:
        logging.error(f"Query execution failed: {e}")
        raise

def q010_open_order_report_data() -> pd.DataFrame:
    """Returns mock data for Open Order Report (for testing/demo)."""
    data = {
        "OrderID": [1001, 1002, 1003],
        "OrderDate": ["2025-07-01", "2025-07-02", "2025-07-03"],
        "Customer": ["Acme", "Beta", "Gamma"],
        "Status": ["Open", "Open", "Closed"],
        "Amount": [250.0, 400.0, 150.0]
    }
    return pd.DataFrame(data)

def q093_shipment_status() -> pd.DataFrame:
    """Returns mock data for Shipment Status (for testing/demo)."""
    data = {
        "ShipmentID": [501, 502, 503],
        "OrderID": [1001, 1002, 1003],
        "ShippedDate": ["2025-07-04", "2025-07-05", None],
        "Status": ["Shipped", "Pending", "Pending"]
    }
    return pd.DataFrame(data)

def test_connection():
    """Tests the database connection and logs the result."""
    try:
        with get_ds_connection() as conn:
            logging.info("Connection successful!")
    except Exception as e:
        logging.error(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
