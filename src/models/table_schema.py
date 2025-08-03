import json
import datetime
import logging
from pathlib import Path
from dataclasses import make_dataclass
from typing import Any, Dict

logging.basicConfig(level=logging.INFO)

TABLE_CLASSES: Dict[str, Any] = {}

def map_column_type(type_str):
    """Maps a DB column type string to a pandas/numpy type string."""
    if type_str is None:
        return 'object'
    t = str(type_str).upper()
    if t.startswith("VARCHAR") or t.startswith("CHAR") or t.startswith("TEXT"):
        return 'object'
    if t in ("LONG", "INTEGER", "INT", "SMALLINT"):
        return 'int64'
    if t == "DATETIME":
        return 'datetime64[ns]'
    if t in ("BIT", "DECIMAL"):
        return 'object'
    return 'object'

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
            # Convert string types back to Python types for dataclass
            type_str = map_column_type(col["type"])
            if type_str == 'object':
                pytype = object
            elif type_str == 'int64':
                pytype = int
            elif type_str == 'datetime64[ns]':
                pytype = datetime.datetime
            else:
                pytype = object
            fields.append((col["name"], pytype, None))
        cls = make_dataclass(table_name, fields)
        TABLE_CLASSES[table_name] = cls
        logging.info(f"Created dataclass for table: {table_name}")
    return schema
