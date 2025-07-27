import os
import pyodbc
import pandas as pd
import logging
import sqlite3
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_sqlite_connection():
    """Connect to the SQLite test database if it exists."""
    db_path = Path("graphite_analytics.db")
    if not db_path.exists():
        logging.warning(f"SQLite database not found: {db_path}")
        return None

    try:
        conn = sqlite3.connect(str(db_path))
        logging.info("SQLite database connection established.")
        return conn
    except Exception as e:
        logging.error(f"SQLite database connection failed: {e}")
        return None

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

def run_pass_through(sql: str, params: list | tuple | None = None) -> pd.DataFrame:
    """Executes a SQL query and returns the result as a DataFrame.

    Parameters
    ----------
    sql : str
        SQL statement to execute.
    params : list | tuple | None
        Optional query parameters passed to ``pandas.read_sql``. If ``None``,
        the query executes without parameters.
    """
    # Check if we're in development mode (use SQLite)
    use_sqlite = os.getenv("USE_SQLITE", "true").lower() == "true"
    
    try:
        if use_sqlite:
            conn = get_sqlite_connection()
            if conn is None:
                logging.warning("SQLite connection unavailable. Returning empty DataFrame.")
                return pd.DataFrame()
            with conn:
                if params:
                    df = pd.read_sql(sql, conn, params=params)
                else:
                    df = pd.read_sql(sql, conn)
        else:
            with get_ds_connection() as conn:
                if params:
                    df = pd.read_sql(sql, conn, params=params)
                else:
                    df = pd.read_sql(sql, conn)
        logging.info("Query executed successfully.")
        return df
    except Exception as e:
        logging.error(f"Query execution failed: {e}")
        return pd.DataFrame()

def q010_open_order_report_data(
    start_date: str | None = None,
    end_date: str | None = None,
    customer_id: int | None = None,
    statuses: list | None = None,
) -> pd.DataFrame:
    """Return Open Order Report data filtered by optional parameters.

    Parameters
    ----------
    start_date : str | None
        Minimum ``OrderDate`` to include (ISO format ``YYYY-MM-DD``).
    end_date : str | None
        Maximum ``OrderDate`` to include.
    customer_id : int | None
        Limit results to a specific customer ID.
    statuses : list | None
        Order status values to filter. Defaults to ``['Open', 'Processing']``.
    """

    if statuses is None:
        statuses = ["Open", "Processing"]

    sql = """
        SELECT
            o.OrderID,
            o.OrderDate,
            c.CustomerName as CustomerName,
            o.Status,
            o.TotalAmount AS TotalAmount
        FROM Orders o
        JOIN Customers c ON o.CustomerID = c.CustomerID
        WHERE 1=1
    """

    params: list = []

    if statuses:
        placeholders = ",".join(["?"] * len(statuses))
        sql += f" AND o.Status IN ({placeholders})"
        params.extend(statuses)

    if start_date:
        sql += " AND o.OrderDate >= ?"
        params.append(start_date)

    if end_date:
        sql += " AND o.OrderDate <= ?"
        params.append(end_date)

    if customer_id:
        sql += " AND o.CustomerID = ?"
        params.append(customer_id)

    sql += "\n    ORDER BY o.OrderDate DESC"

    return run_pass_through(sql, params if params else None)

def q093_shipment_status() -> pd.DataFrame:
    """Returns Shipment Status data from database."""
    sql = """
    SELECT 
        s.ShipmentID,
        s.OrderID,
        s.ShippedDate,
        s.Status,
        s.TrackingNumber
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
