import json
import datetime
import logging
from dataclasses import make_dataclass
from pathlib import Path
from typing import Any, Dict

logging.basicConfig(level=logging.INFO)

TABLE_CLASSES: Dict[str, Any] = {}


def map_column_type(type_str: str | None) -> str:
    """Map a DB column type string to a pandas-friendly type."""
    if type_str is None:
        return "object"
    t = str(type_str).upper()

    if t.startswith(("VARCHAR", "CHAR", "TEXT")):
        return "object"
    if t in {"LONG", "INTEGER", "INT", "SMALLINT"}:
        return "int64"
    if t in {"DATETIME", "DATETIME2"}:
        return "datetime64[ns]"
    if t in {"BIT", "DECIMAL"}:
        return "object"
    return "object"


def load_schema(schema_path: str = "schema.json") -> Dict[str, Any]:
    """Load a table schema from JSON and build dataclasses for each table."""
    path = Path(schema_path)
    if not path.exists():
        logging.error("Schema file not found: %s", schema_path)
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with path.open() as f:
        schema = json.load(f)
    logging.info("Loaded schema from %s", schema_path)

    for table_name, columns in schema.items():
        fields = []
        for col in columns:
            dtype = map_column_type(col["type"])
            if dtype == "int64":
                pytype = int
            elif dtype == "datetime64[ns]":
                pytype = datetime.datetime
            else:
                pytype = object
            fields.append((col["name"], pytype, None))
        cls = make_dataclass(table_name, fields)
        TABLE_CLASSES[table_name] = cls
        logging.info("Created dataclass for table: %s", table_name)
    return schema
