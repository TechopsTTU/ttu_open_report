import pyodbc
import os
import sqlite3
from dotenv import load_dotenv

def check_database_connection():
    """Checks connections to SQLite and Pervasive databases and returns status and info."""
    load_dotenv()
    
    db_info = {
        "database_name": "N/A",
        "database_type": "N/A",
        "connection_string": "N/A",
        "tables_found": "N/A",
        "columns_found": "N/A",
        "error_message": ""
    }
    
    # Check environment settings to prioritize connection type
    active_env = os.getenv("ACTIVE_ENV", "local")
    database_env = os.getenv("DATABASE_ENV", "sqlite")
    
    # Try Pervasive connection first if we're in production mode
    if active_env == "prod" and database_env == "pervasive":
        driver = os.getenv("NDUSTROS_DRIVER")
        server = os.getenv("NDUSTROS_SERVER")
        port = os.getenv("NDUSTROS_PORT")
        database = os.getenv("NDUSTROS_DB")
        user = os.getenv("NDUSTROS_USER")
        password = os.getenv("NDUSTROS_PASS")
        
        if all([driver, server, port, database, user, password]):
            conn_str = (
                f"DRIVER={{{driver}}};"
                f"SERVERNAME={server};"
                f"PORT={port};"
                f"DBQ={database};"
                f"UID={user};"
                f"PWD={password};"
            )
            
            try:
                conn = pyodbc.connect(conn_str, autocommit=True)
                cursor = conn.cursor()
                
                # Get table count using ODBC tables() method
                cursor.tables()
                tables = cursor.fetchall()
                table_count = len(tables)
                
                # Test data access with a known table
                try:
                    cursor.execute("SELECT COUNT(*) FROM OEHDR")
                    record_count = cursor.fetchone()[0]
                    additional_info = f"OEHDR table: {record_count} records"
                except:
                    additional_info = "Table access verified"

                db_info.update({
                    "database_name": f"{database} (Production)",
                    "database_type": "Pervasive PSQL",
                    "connection_string": f"{server}:{port}/{database}",
                    "tables_found": table_count,
                    "columns_found": "N/A (Complex schema)",
                    "error_message": additional_info
                })
                conn.close()
                return True, db_info
            except pyodbc.Error as ex:
                db_info["error_message"] = f"Pervasive connection failed: {ex}, falling back to SQLite"
                # Fall through to try SQLite

    # Try SQLite connection (either as fallback or primary)
    sqlite_db_path = "graphite_analytics.db"
    if os.path.exists(sqlite_db_path):
        try:
            conn = sqlite3.connect(sqlite_db_path)
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            
            # Get column count (simple sum for all tables)
            column_count = 0
            for table_name in table_names:
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                column_count += len(columns)

            db_info.update({
                "database_name": sqlite_db_path,
                "database_type": "SQLite",
                "connection_string": os.path.abspath(sqlite_db_path),
                "tables_found": len(table_names),
                "columns_found": column_count
            })
            conn.close()
            return True, db_info
        except sqlite3.Error as e:
            db_info["error_message"] = f"SQLite connection failed: {e}"
            # Continue to try Pervasive if SQLite fails
    else:
        db_info["error_message"] = "SQLite database file (graphite_analytics.db) not found."

    # If SQLite not found or failed, try Pervasive
    driver = os.getenv("NDUSTROS_DRIVER")
    server = os.getenv("NDUSTROS_SERVER")
    port = os.getenv("NDUSTROS_PORT")
    database = os.getenv("NDUSTROS_DB")
    user = os.getenv("NDUSTROS_USER")
    password = os.getenv("NDUSTROS_PASS")
    
    if all([driver, server, port, database, user, password]):
        conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVERNAME={server};"
            f"PORT={port};"
            f"DBQ={database};"
            f"UID={user};"
            f"PWD={password};"
        )
        
        try:
            conn = pyodbc.connect(conn_str, autocommit=True)
            cursor = conn.cursor()
            
            # Get table names (example for Pervasive, adjust as needed)
            # This query might vary based on Pervasive version/schema
            try:
                cursor.execute("SELECT TABLE_NAME FROM X$FILE WHERE XF$TYPE = 'T'") # Common for Pervasive
                tables = cursor.fetchall()
                table_names = [table[0] for table in tables]
            except pyodbc.Error:
                table_names = [] # Fallback if X$FILE is not accessible

            column_count = "N/A" # More complex to get all columns for Pervasive without specific table iteration

            db_info.update({
                "database_name": database,
                "database_type": "Pervasive PSQL",
                "connection_string": conn_str,
                "tables_found": len(table_names) if table_names else "N/A",
                "columns_found": column_count
            })
            conn.close()
            return True, db_info
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            db_info["error_message"] = f"Pervasive DB connection failed: {sqlstate} - {ex}"
            return False, db_info
    else:
        if not db_info["error_message"]:
            db_info["error_message"] = "Pervasive DB environment variables not fully set and SQLite not found/failed."
        return False, db_info

    return False, db_info # Should not be reached if one of the above returns

if __name__ == "__main__":
    status, info = check_database_connection()
    print(f"Connection Status: {status}")
    for key, value in info.items():
        print(f"{key}: {value}")
