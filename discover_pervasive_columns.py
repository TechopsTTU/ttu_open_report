import os
import pyodbc
import logging

logging.basicConfig(level=logging.INFO)

def get_pervasive_connection():
    """Attempts to connect to the Pervasive database using ODBC."""
    try:
        drv = os.getenv("NDUSTROS_DRIVER", "Pervasive ODBC Client Interface")
        srv = os.getenv("NDUSTROS_SERVER", "PLATSRVR")
        port = os.getenv("NDUSTROS_PORT", "1583")
        dbq = os.getenv("NDUSTROS_DB", "NdustrOS")
        user = os.getenv("NDUSTROS_USER")
        pwd = os.getenv("NDUSTROS_PASS")
        
        if not all([drv, srv, port, dbq, user, pwd]):
            raise ValueError("One or more Pervasive DB environment variables are not set.")
            
        conn_str = f"Driver={{{drv}}};ServerName={srv};Port={port};DBQ={dbq};uid={user};pwd={pwd}"
        conn = pyodbc.connect(conn_str, autocommit=True)
        logging.info("Pervasive DB connection established.")
        return conn
    except Exception as e:
        logging.error(f"Pervasive DB connection failed: {e}")
        raise

def list_columns(table_name):
    """Lists all columns in a given table."""
    conn = None
    try:
        conn = get_pervasive_connection()
        cursor = conn.cursor()
        columns = []
        for row in cursor.columns(table=table_name):
            columns.append({'name': row.column_name, 'type': row.type_name})
        print(f"Columns in {table_name}: {columns}")
        return columns
    except Exception as e:
        logging.error(f"Failed to list columns for table {table_name}: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    list_columns("OEHDR")
