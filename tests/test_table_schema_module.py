
import unittest
from models.table_schema import map_column_type
import datetime

class TestMapColumnType(unittest.TestCase):
    def test_string_type(self):
        self.assertIs(map_column_type("VARCHAR(50)"), str)

    def test_integer_type(self):
        self.assertIs(map_column_type("LONG"), int)
        self.assertIs(map_column_type("INTEGER"), int)

    def test_datetime_type(self):
        self.assertIs(map_column_type("DATETIME"), datetime.datetime)

    def test_unknown_type_defaults_to_object(self):
        self.assertIs(map_column_type("SOMETHING_ELSE"), object)

if __name__ == "__main__":
    unittest.main()
