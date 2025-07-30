import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()

server = os.getenv("SQL_SERVER_HOST")
user = os.getenv("SQL_SERVER_USER")
password = os.getenv("SQL_SERVER_PASSWORD")
database = os.getenv("SQL_SERVER_DATABASE")

conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={user};"
    f"PWD={password}"
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    print("Connection successful! Test query result:", cursor.fetchone())
    conn.close()
except Exception as e:
    print("Connection failed:", e)
