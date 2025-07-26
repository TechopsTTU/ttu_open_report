
import datetime

def map_column_type(type_str):
    t = type_str.upper()
    if t.startswith("VARCHAR") or t.startswith("CHAR") or t.startswith("TEXT"):
        return str
    if t in ("LONG", "INTEGER", "INT", "SMALLINT"):
        return int
    if t == "DATETIME":
        return datetime.datetime
    return object
