import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()

db_path = os.getenv("ACCESS_DB_PATH")
db_driver = os.getenv("ACCESS_DB_DRIVER")

conn_str = f"DRIVER={db_driver};DBQ={db_path}"  # For Access

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM MSysObjects")
    print("Access DB connection successful! Test query result:", cursor.fetchone())
    conn.close()
except Exception as e:
    print("Access DB connection failed:", e)
