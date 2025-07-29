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
        raise FileNotFoundError(f"SQLite database not found: {db_path}. Run create_real_data_db.py first.")
    
    try:
        conn = sqlite3.connect(str(db_path))
        logging.info("SQLite database connection established.")
        return conn
    except Exception as e:
        logging.error(f"SQLite database connection failed: {e}")
        raise

def build_pervasive_connection_string():
    """Builds the Pervasive DB ODBC connection string from environment variables."""
    drv = os.getenv("NDUSTROS_DRIVER", "Pervasive ODBC Client Interface")
    srv = os.getenv("NDUSTROS_SERVER", "PLATSRVR")
    port = os.getenv("NDUSTROS_PORT", "1583")
    dbq = os.getenv("NDUSTROS_DB", "NdustrOS")
    user = os.getenv("NDUSTROS_USER")
    pwd = os.getenv("NDUSTROS_PASS")
    
    if not all([drv, srv, port, dbq, user, pwd]):
        raise ValueError("One or more Pervasive DB environment variables are not set.")
        
    return f"Driver={{{drv}}};ServerName={srv};Port={port};DBQ={dbq};uid={user};pwd={pwd}"

def get_pervasive_connection():
    """Attempts to connect to the Pervasive database using ODBC."""
    try:
        conn_str = build_pervasive_connection_string()
        conn = pyodbc.connect(conn_str)
        logging.info("Pervasive DB connection established.")
        return conn
    except Exception as e:
        logging.error(f"Pervasive DB connection failed: {e}")
        raise

def get_db_connection():
    """
    Establishes a database connection based on the DATABASE_ENV environment variable.
    Defaults to SQLite if the variable is not set.
    """
    db_env = os.getenv("DATABASE_ENV", "sqlite").lower()
    
    if db_env == "pervasive":
        logging.info("Connecting to Pervasive DB...")
        return get_pervasive_connection()
    elif db_env == "sqlite":
        logging.info("Connecting to SQLite DB...")
        return get_sqlite_connection()
    else:
        raise ValueError(f"Invalid DATABASE_ENV: '{db_env}'. Must be 'sqlite' or 'pervasive'.")

def run_query(sql: str, params=None) -> pd.DataFrame:
    """
    Executes a SQL query against the configured database and returns a DataFrame.
    """
    try:
        with get_db_connection() as conn:
            df = pd.read_sql(sql, conn, params=params)
        logging.info("Query executed successfully.")
        return df
    except Exception as e:
        logging.error(f"Query execution failed: {e}")
        raise

# --- Specific Query Functions ---

def get_open_orders_report(start_date, end_date) -> pd.DataFrame:
    """
    Returns Open Order Report data from the configured database.
    The SQL is written to be compatible with both SQLite and Pervasive SQL.
    """
    sql = """
    SELECT
        o.OrderID,
        o.OrderDate,
        c.CustomerName,
        o.CustomerPO,
        p.ProductID,
        p.ProductName,
        od.Quantity AS QtyRemaining,
        od.UnitPrice,
        od.TotalCost,
        o.Status AS OrderStatus,
        o.DeliveryDate AS PromiseDate
    FROM
        Orders o
    JOIN
        OrderDetails od ON o.OrderID = od.OrderID
    JOIN
        Customers c ON o.CustomerID = c.CustomerID
    JOIN
        Products p ON od.ProductID = p.ProductID
    WHERE
        p.ProductID IS NOT NULL
        AND o.Status IN ('BN', 'BP', 'Bp', 'NP')
        AND o.OrderDate BETWEEN ? AND ?
    ORDER BY o.OrderDate, o.OrderID;
    """
    return run_query(sql, params=(start_date, end_date))

def test_connection():
    """Tests the database connection based on the DATABASE_ENV and logs the result."""
    try:
        conn = get_db_connection()
        logging.info("Connection successful!")
        conn.close()
    except Exception as e:
        logging.error(f"Connection failed: {e}")

if __name__ == "__main__":
    # Example of how to test:
    # Set DATABASE_ENV in your shell before running
    # export DATABASE_ENV=pervasive
    # python models/query_definitions.py
    test_connection()
