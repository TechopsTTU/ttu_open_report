import os
import pyodbc
import pandas as pd
import logging
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_pervasive_connection():
    """Attempts to connect to the Pervasive database using ODBC."""
    conn = None
    conn = None
    try:
        driver = os.getenv('NDUSTROS_DRIVER', 'Pervasive ODBC Client Interface')
        server = os.getenv('NDUSTROS_SERVER', 'PLATSRVR')
        port = os.getenv('NDUSTROS_PORT', '1583')
        dbq = os.getenv('NDUSTROS_DB', 'NdustrOS')
        user = os.getenv('NDUSTROS_USER')
        pwd = os.getenv('NDUSTROS_PASS')

        conn_str = (
            "DRIVER={" + driver + "};"
            "ServerName=" + server + ";"
            "Port=" + port + ";"
            "DBQ=" + dbq + ";"
            "uid=" + user + ";"
            "pwd=" + pwd
        )
        conn = pyodbc.connect(conn_str, autocommit=True)
        logging.info("Pervasive DB connection established.")
        return conn
    except Exception as e:
        logging.error(f"Pervasive DB connection failed: {e}")
        raise

def get_open_orders_report_pervasive(start_date, end_date):
    """
    Returns Open Order Report data from the Pervasive database.
    Manually fetches data to handle problematic date/time columns.
    """
    conn = None
    try:
        conn = get_pervasive_connection()
        cursor = conn.cursor()

        tables_to_inspect = {
            'OEHDR': ['Ordernumber', 'Customerkey', 'Orderdate', 'Requestdate', 'Shipdate', 'Canceldate'],
            'OELIN': ['Ordernumber', 'Itemkey', 'Qtyremaining'],
            'ARCUST': ['Customerkey', 'Customername'],
            'INMAST_DBM': ['Itemkey', 'Itemdescription1']
        }

        dataframes = {}

        for table_name, columns_list in tables_to_inspect.items():
            select_parts = []
            for col_name in columns_list:
                # Get column type from cursor.columns() to decide on casting
                col_type = None
                for col_info in cursor.columns(table=table_name):
                    if col_info.column_name == col_name:
                        col_type = col_info.type_name
                        break
                
                if col_type in ['DATE', 'TIME', 'TIMESTAMP']:
                    select_parts.append(f'CAST("{col_name}" AS VARCHAR(255)) AS {col_name}')
                else:
                    select_parts.append(f'"{col_name}"')
            
            sql = f"SELECT {', '.join(select_parts)} FROM {table_name}"
            
            print(f"\n--- Executing SQL Query for {table_name} ---\n{sql}")
            cursor.execute(sql)
            
            cols = [column[0] for column in cursor.description]
            rows = [list(row) for row in cursor.fetchall()]
            
            dataframes[table_name] = pd.DataFrame(rows, columns=cols)
            
            print(f"\n--- {table_name} Data (first 10 rows) ---")
            print(dataframes[table_name].head(10))

        # Now, perform the joins in Pandas
        df = dataframes['OEHDR']
        df = pd.merge(df, dataframes['OELIN'], on='Ordernumber', how='inner')
        df = pd.merge(df, dataframes['ARCUST'], on='Customerkey', how='inner')
        df = pd.merge(df, dataframes['INMAST_DBM'], on='Itemkey', how='inner')

        print("\n--- Joined DataFrame (first 10 rows) ---")
        print(df.head(10))
        print(f"\n--- Number of rows in Joined DataFrame: {len(df)} ---")

        # Apply filters and rename columns
        df = df[df['Qtyremaining'] > 0] # Filter for open orders
        df = df[(df['Orderdate'] >= start_date) & (df['Orderdate'] <= end_date)] # Date filter

        df = df.rename(columns={
            'Ordernumber': 'OrderID',
            'Orderdate': 'OrderDate',
            'Customername': 'CustomerName',
            'Customerponumber': 'CustomerPO',
            'Itemkey': 'ProductID',
            'Itemdescription1': 'ProductName',
            'Qtyremaining': 'QtyRemaining',
            'Unitprice': 'UnitPrice',
            'Orderstatus': 'OrderStatus',
            'Requestdate': 'PromiseDate'
        })

        return df

    except Exception as e:
        logging.error(f"Query execution failed in Pervasive DB: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()