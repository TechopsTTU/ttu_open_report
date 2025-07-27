"""
Analyze the Access database to extract all tables and queries
"""
import pyodbc
import pandas as pd
import os

def analyze_access_database():
    # Get full path to the database
    db_path = os.path.abspath('Opnordrp-vlad-copy.accdb')
    print(f'Database path: {db_path}')
    
    # Connect to Access database
    conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};'
    
    try:
        conn = pyodbc.connect(conn_str)
        print("✅ Successfully connected to Access database")
        
        # Get all tables
        print('\n=== TABLES IN DATABASE ===')
        try:
            # Method 1: Use MSysObjects
            tables_query = """
            SELECT Name 
            FROM MSysObjects 
            WHERE Type=1 AND Flags=0 AND Name NOT LIKE 'MSys*' AND Name NOT LIKE '~*'
            ORDER BY Name
            """
            tables = pd.read_sql(tables_query, conn)
            for table in tables['Name']:
                print(f'📋 {table}')
                
        except Exception as e:
            print(f"Method 1 failed: {e}")
            # Method 2: Use system tables
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Name FROM MSysObjects WHERE Type=1 AND Flags=0")
                tables = cursor.fetchall()
                print("Tables found (Method 2):")
                for table in tables:
                    if not table[0].startswith('MSys') and not table[0].startswith('~'):
                        print(f'📋 {table[0]}')
            except Exception as e2:
                print(f"Method 2 failed: {e2}")
        
        # Get all queries  
        print('\n=== QUERIES IN DATABASE ===')
        try:
            queries_query = """
            SELECT Name 
            FROM MSysObjects 
            WHERE Type=5 AND Name NOT LIKE 'MSys*' AND Name NOT LIKE '~*'
            ORDER BY Name
            """
            queries = pd.read_sql(queries_query, conn)
            for query in queries['Name']:
                print(f'🔍 {query}')
                
        except Exception as e:
            print(f"Error getting queries: {e}")
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Name FROM MSysObjects WHERE Type=5")
                queries = cursor.fetchall()
                print("Queries found (alternative method):")
                for query in queries:
                    if not query[0].startswith('MSys') and not query[0].startswith('~'):
                        print(f'🔍 {query[0]}')
            except Exception as e2:
                print(f"Alternative query method failed: {e2}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        print("Make sure you have the Microsoft Access Database Engine installed")

if __name__ == "__main__":
    analyze_access_database()
