"""
Test 06: Application Core Tests
Tests for the core application functionality
"""
import pytest
import sys
import importlib.util
import os
from pathlib import Path

# Add required paths for imports
sys.path.append('.')


class TestCoreApplication:
    """Test core application functionality"""
    
    def test_app_py_exists(self):
        """Test that app.py exists"""
        assert Path("app.py").exists(), "app.py file should exist"
    
    def test_app_py_has_main_function(self):
        """Test that app.py has a main function"""
        spec = importlib.util.spec_from_file_location("app", "app.py")
        assert spec is not None, "Could not find app.py module"
        app = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(app)
            assert hasattr(app, "main"), "app.py should have a main function"
            assert callable(app.main), "main should be callable"
        except Exception as e:
            pytest.fail(f"Failed to import app.py: {e}")
    
    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists"""
        assert Path("requirements.txt").exists(), "requirements.txt file should exist"
    
    def test_requirements_txt_contains_essential_packages(self):
        """Test that requirements.txt contains essential packages"""
        with open("requirements.txt", "r") as f:
            content = f.read().lower()
        
        essential_packages = ["streamlit", "pandas", "matplotlib", "plotly", "pytest"]
        for package in essential_packages:
            assert package.lower() in content, f"requirements.txt should contain {package}"
    
    def test_environment_variables_set(self):
        """Test that environment variables are properly set"""
        # This is a safer test that doesn't assume specific environment variables
        env_file = Path(".env")
        assert env_file.exists(), ".env file should exist"
        
        with open(env_file, "r") as f:
            content = f.read()
        
        assert "LOCAL_DB_TYPE=" in content, ".env should contain LOCAL_DB_TYPE"
        assert "ACTIVE_ENV=" in content, ".env should contain ACTIVE_ENV"
    
    def test_static_resources_available(self):
        """Test that static resources are available"""
        # Test for TTU logo
        logo_path = Path("static/TTU_LOGO.jpg")
        if not logo_path.exists():
            logo_path = Path("resources/static/TTU_LOGO.jpg")
        
        assert logo_path.exists(), "TTU logo should exist in static directory"
    
    def test_src_directory_structure(self):
        """Test that src directory has the correct structure"""
        src_dir = Path("src")
        assert src_dir.exists(), "src directory should exist"
        assert (src_dir / "models").exists(), "src/models directory should exist"
        assert (src_dir / "models" / "__init__.py").exists(), "src/models/__init__.py should exist"
        assert (src_dir / "models" / "query_definitions.py").exists(), "src/models/query_definitions.py should exist"
        assert (src_dir / "models" / "table_schema.py").exists(), "src/models/table_schema.py should exist"


if __name__ == "__main__":
    pytest.main([__file__])
