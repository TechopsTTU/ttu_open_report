"""
Test 03: Page Load Tests
Tests Streamlit page imports and basic initialization
"""
import pytest
import sys
import importlib
import importlib.util
import os
from pathlib import Path

# Add required paths for imports
sys.path.append('src')


class TestPageLoads:
    """Test if the Streamlit pages can be imported without errors"""
    
    def test_app_py_imports(self):
        """Test main app.py imports correctly"""
        spec = importlib.util.spec_from_file_location("app", "app.py")
        assert spec is not None, "Could not locate app.py"
        app_module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(app_module)
            assert hasattr(app_module, "main"), "app.py should have a main function"
        except ImportError as e:
            pytest.fail(f"Failed to import app.py: {e}")
        except Exception as e:
            pytest.fail(f"Error initializing app.py: {e}")
    
    def _test_page_import(self, page_path):
        """Helper method to test importing a specific page"""
        if not os.path.exists(page_path):
            pytest.fail(f"Page file does not exist: {page_path}")
            
        try:
            spec = importlib.util.spec_from_file_location("page_module", page_path)
            assert spec is not None, f"Could not locate module spec for {page_path}"
            page_module = importlib.util.module_from_spec(spec)
            
            # Add the path with src to the sys.path before loading
            original_path = sys.path.copy()
            if 'src' not in sys.path:
                sys.path.append('src')
                
            spec.loader.exec_module(page_module)
            
            # Reset sys.path
            sys.path = original_path
            
            return True
        except ImportError as e:
            pytest.fail(f"Failed to import {page_path}: {e}")
            return False
        except Exception as e:
            pytest.fail(f"Error initializing {page_path}: {e}")
            return False
    
    def test_tables_page_imports(self):
        """Test tables page imports correctly"""
        self._test_page_import("pages/1_tables.py")
    
    def test_queries_page_imports(self):
        """Test queries page imports correctly"""
        self._test_page_import("pages/2_queries.py")
    
    def test_reports_page_imports(self):
        """Test reports page imports correctly"""
        self._test_page_import("pages/3_reports.py")
    
    def test_forms_page_imports(self):
        """Test forms page imports correctly"""
        self._test_page_import("pages/4_forms.py")
    
    def test_open_order_report_page_imports(self):
        """Test open order report page imports correctly"""
        self._test_page_import("pages/5_open_order_report.py")
    
    def test_business_queries_page_imports(self):
        """Test business queries page imports correctly"""
        self._test_page_import("pages/business_queries.py")
    
    def test_interactive_reports_page_imports(self):
        """Test interactive reports page imports correctly"""
        self._test_page_import("pages/interactive_reports.py")


if __name__ == "__main__":
    pytest.main([__file__])
