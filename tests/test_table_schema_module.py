

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from models.table_schema import map_column_type
import datetime

class TestMapColumnType(unittest.TestCase):
    """Verify column type mapping returns expected pandas-style strings."""

    def test_string_type(self):
        self.assertEqual(map_column_type("VARCHAR(50)"), "object")

    def test_integer_type(self):
        self.assertEqual(map_column_type("LONG"), "int64")
        self.assertEqual(map_column_type("INTEGER"), "int64")

    def test_datetime_type(self):
        self.assertEqual(map_column_type("DATETIME"), "datetime64[ns]")

    def test_unknown_type_defaults_to_object(self):
        self.assertEqual(map_column_type("SOMETHING_ELSE"), "object")

if __name__ == "__main__":
    unittest.main()
