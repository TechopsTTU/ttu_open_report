import json
import datetime
import logging
from pathlib import Path
from dataclasses import make_dataclass
from typing import Any, Dict, Type

logging.basicConfig(level=logging.INFO)

TABLE_CLASSES: Dict[str, Any] = {}

def map_column_type(type_str):
    """Map a DB column type string to a pandas-friendly dtype string."""
    if not type_str:
        return "object"

    t = type_str.lower()

    if t.startswith("varchar") or t.startswith("char") or t.startswith("text"):
        return "object"
    if t in ("long", "integer", "int", "smallint"):
        return "int64"
    if t in ("decimal", "numeric"):
        return "object"
    if t in ("float", "real", "double"):
        return "float64"
    if t.startswith("datetime") or t in ("date", "timestamp"):
        return "datetime64[ns]"
    return "object"

def map_column_type_to_python(type_str: str) -> Type:
    """Map a DB column type string to a native Python type."""
    if not type_str:
        return str

    t = type_str.lower()

    if t.startswith("varchar") or t.startswith("char") or t.startswith("text") or t == "string":
        return str
    if t in ("long", "integer", "int", "smallint"):
        return int
    if t in ("decimal", "numeric"):
        return float
    if t in ("float", "real", "double"):
        return float
    if t.startswith("datetime") or t in ("date", "timestamp"):
        return datetime.datetime
    if t == "bit":
        return bool
    return str

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
            pytype = map_column_type_to_python(col["type"])
            fields.append((col["name"], pytype, None))
        cls = make_dataclass(table_name, fields)
        TABLE_CLASSES[table_name] = cls
        logging.info(f"Created dataclass for table: {table_name}")
    return schema
