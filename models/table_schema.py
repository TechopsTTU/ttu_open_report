def map_column_type(type_str):
    t = type_str.upper()
    if t.startswith("VARCHAR") or t.startswith("CHAR") or t.startswith("TEXT"):
        return str
    if t in ("LONG", "INTEGER", "INT", "SMALLINT"):
        return int
    if t == "DATETIME":
        return datetime.datetime
    return object
def load_schema(schema_path="schema.json"):
    path = Path(schema_path)
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    with path.open() as f:
        schema = json.load(f)
    # Build dataclasses for each table
    for table_name, columns in schema.items():
        fields = []
        for col in columns:
            pytype = map_column_type(col["type"])
            fields.append((col["name"], pytype, None))
        cls = make_dataclass(table_name, fields)
        TABLE_CLASSES[table_name] = cls
    return schema
import json
import datetime
import logging
from pathlib import Path
from dataclasses import make_dataclass
from typing import Any, Dict

logging.basicConfig(level=logging.INFO)

TABLE_CLASSES: Dict[str, Any] = {}

def map_column_type(type_str):
    """Maps a DB column type string to a Python type."""
    t = type_str.upper()
    if t.startswith("VARCHAR") or t.startswith("CHAR") or t.startswith("TEXT"):
        return str
    if t in ("LONG", "INTEGER", "INT", "SMALLINT"):
        return int
    if t == "DATETIME":
        return datetime.datetime
    return object

def load_schema(schema_path="schema.json"):
    """
    Loads the schema from a JSON file and builds dataclasses for each table.
    Raises FileNotFoundError if the schema file is missing.
    """
    path = Path(schema_path)
    if not path.exists():
        logging.error(f"Schema file not found: {schema_path}")
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    with path.open() as f:
        schema = json.load(f)
    logging.info(f"Loaded schema from {schema_path}")
    # Build dataclasses for each table
    for table_name, columns in schema.items():
        fields = []
        for col in columns:
            pytype = map_column_type(col["type"])
            fields.append((col["name"], pytype, None))
        cls = make_dataclass(table_name, fields)
        TABLE_CLASSES[table_name] = cls
        logging.info(f"Created dataclass for table: {table_name}")
    return schema
