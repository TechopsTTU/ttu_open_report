import os
import pyodbc
import pandas as pd
import logging
from src.models.pervasive_db import get_pervasive_connection

logging.basicConfig(level=logging.INFO)

def inspect_oehdr_and_oelin_raw():
    """
    Manually fetches and inspects raw data from OEHDR and OELIN tables.
    """
    conn = None
    try:
        conn = get_pervasive_connection()
        cursor = conn.cursor()
        
        # Fetch OEHDR data
        sql_oehdr = "SELECT Ordernumber, Poststatus FROM OEHDR;"
        cursor.execute(sql_oehdr)
        oehdr_rows = cursor.fetchall()
        oehdr_cols = [column[0] for column in cursor.description]
        df_oehdr = pd.DataFrame.from_records(oehdr_rows, columns=oehdr_cols)
        
        print("\n--- OEHDR Raw Data Sample (first 10 rows) ---")
        print(df_oehdr.head(10))
        print("\nDistinct values and counts for OEHDR.Poststatus (raw and trimmed):")
        print(df_oehdr['Poststatus'].astype(str).str.strip().value_counts(dropna=False).sort_index())

        # Fetch OELIN data
        sql_oelin = "SELECT Ordernumber, Qtyremaining FROM OELIN;"
        cursor.execute(sql_oelin)
        oelin_rows = cursor.fetchall()
        oelin_cols = [column[0] for column in cursor.description]
        df_oelin = pd.DataFrame.from_records(oelin_rows, columns=oelin_cols)

        print("\n--- OELIN Raw Data Sample (first 10 rows) ---")
        print(df_oelin.head(10))
        print("\nDistinct values and counts for OELIN.Qtyremaining (raw and trimmed):")
        print(df_oelin['Qtyremaining'].astype(str).str.strip().value_counts(dropna=False).sort_index())

    except Exception as e:
        logging.error(f"Failed to inspect OEHDR and OELIN raw data: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    inspect_oehdr_and_oelin_raw()
