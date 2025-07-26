

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from extract import sanitize_filename

class TestSanitizeFilename(unittest.TestCase):
    def test_no_change_for_valid_name(self):
        self.assertEqual(sanitize_filename("NormalName123"), "NormalName123")

    def test_replace_invalid_characters(self):
        original = r"q:Count/Other*Name?<>|"
        safe = sanitize_filename(original)
        # All invalid Windows filename chars should become underscores
        for ch in r'\\/:*?"<>|':
            self.assertNotIn(ch, safe)
        self.assertTrue(all(c.isalnum() or c in ("-", "_") for c in safe))

if __name__ == "__main__":
    unittest.main()
