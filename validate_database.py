import sqlite3
import os

db_path = "graphite_analytics.db"
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")
print(f"Database size: {os.path.getsize(db_path) if os.path.exists(db_path) else 'N/A'}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tables:", [table[0] for table in tables])
    
    # For each table, get schema and count
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        
        # Get schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print("Columns:", [(col[1], col[2]) for col in columns])
        
        # Count rows
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"Row count: {count}")
        
        # Sample data (up to 3 rows)
        if count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
            rows = cursor.fetchall()
            print("Sample data:")
            for row in rows:
                print(row)
                
    conn.close()
except Exception as e:
    print(f"Error: {str(e)}")
