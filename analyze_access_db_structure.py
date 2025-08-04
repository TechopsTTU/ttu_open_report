#!/usr/bin/env python3
"""
Analyzes the structure of the Access database to identify tables and queries.

This script connects to the 'Opnordrp-vlad-copy.accdb' file and lists all
user-defined tables and queries to help locate the source for the
'Open Order Report'.
"""

import pyodbc
import os

def analyze_access_db_structure():
    """
    Connects to the Access database and lists all user tables and queries.
    """
    # Ensure we are in the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    db_file = os.path.abspath('Opnordrp-vlad-copy.accdb')
    
    if not os.path.exists(db_file):
        print(f"ERROR: Database file not found at '{db_file}'")
        print("Please ensure you are in the 'dev' branch and the file is present.")
        return

    # This is the standard ODBC driver for .accdb files on Windows.
    # It's typically installed with Microsoft Office or the free
    # Microsoft Access Database Engine 2016 Redistributable.
    driver = '{Microsoft Access Driver (*.mdb, *.accdb)}'
    conn_str = f'DRIVER={driver};DBQ={db_file};'

    print(f"Connecting to Access DB: {os.path.basename(db_file)}")

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        print("\n--- TABLES ---")
        tables = []
        for row in cursor.tables(tableType='TABLE'):
            table_name = row.table_name
            # Filter out Access system tables
            if not table_name.startswith('MSys'):
                tables.append(table_name)
        
        for table in sorted(tables):
            print(f"  - {table}")

        print("\n--- QUERIES (Potential Report Sources) ---")
        queries = []
        # In ODBC, Access queries are treated as 'VIEWS'
        for row in cursor.tables(tableType='VIEW'):
            query_name = row.table_name
            # Filter out temporary queries created by Access forms/reports
            if not query_name.startswith('~'):
                 queries.append(query_name)

        for query in sorted(queries):
            print(f"  - {query}")

        print("Analysis complete.")
        print("\nNEXT STEP: Please identify the query from the list above that is most likely related to the 'Open Order Report'.")

    except pyodbc.Error as e:
        print(f"DATABASE CONNECTION ERROR: {e}")
        print("--- TROUBLESHOOTING ---")
        print("1. Ensure you have the 'Microsoft Access Database Engine 2016 Redistributable' installed.")
        print("   You can download it from the official Microsoft website.")
        print("2. Make sure no other application (like MS Access itself) has the database file open.")
        print("3. Verify the file is not corrupted.")

    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    analyze_access_db_structure()
