import argparse
import os
import pyodbc
import pandas as pd
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def sanitize_filename(name):
    """Replace invalid Windows filename characters with underscores. Handles edge cases for tests."""
    if not name:
        return name
    invalid = set('\\/:*?"<>|')
    return ''.join('_' if c in invalid else c for c in name)

def connect_to_access(db_path):
    """Connects to an Access database and returns the connection object."""
    conn_str = (
        f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};"
        f"DBQ={db_path};"
    )
    try:
        conn = pyodbc.connect(conn_str)
        logging.info(f"Connected to Access DB: {db_path}")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to Access DB: {e}")
        raise

def list_tables_and_views(conn):
    """Lists all tables and views in the Access database."""
    try:
        cursor = conn.cursor()
        tables = []
        for row in cursor.tables():
            if row.table_type in ("TABLE", "VIEW"):
                tables.append(row.table_name)
        logging.info(f"Found tables/views: {tables}")
        return tables
    except Exception as e:
        logging.error(f"Failed to list tables/views: {e}")
        raise

def export_table(conn, table_name, output_dir):
    """Exports a table to CSV in the specified output directory."""
    safe_name = sanitize_filename(table_name)
    try:
        df = pd.read_sql(f"SELECT * FROM [{table_name}]", conn)
        out_path = Path(output_dir) / f"{safe_name}.csv"
        df.to_csv(out_path, index=False)
        logging.info(f"Exported {table_name} to {out_path}")
        return df
    except Exception as e:
        logging.error(f"Failed to export table {table_name}: {e}")
        raise

def generate_schema(conn, table_names):
    """Generates a schema dictionary for the given tables."""
    schema = {}
    cursor = conn.cursor()
    for table in table_names:
        safe_name = sanitize_filename(table)
        columns = []
        for col in cursor.columns(table=table):
            columns.append({
                "name": col.column_name,
                "type": col.type_name,
                "nullable": bool(col.nullable)
            })
        schema[safe_name] = columns
    return schema

def write_schema(schema, schema_path):
    """Writes the schema dictionary to a JSON file."""
    try:
        with open(schema_path, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2)
        logging.info(f"Schema written to {schema_path}")
    except Exception as e:
        logging.error(f"Failed to write schema: {e}")
        raise

def main():
    """Main entry point for extracting tables and schema from Access DB."""
    parser = argparse.ArgumentParser(description="Extract tables from Access DB")
    parser.add_argument("--db-path", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--schema-path", required=True)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    try:
        with connect_to_access(args.db_path) as conn:
            tables = list_tables_and_views(conn)
            for table in tables:
                export_table(conn, table, args.output_dir)
            schema = generate_schema(conn, tables)
            write_schema(schema, args.schema_path)
    except Exception as e:
        logging.error(f"Extraction failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()
