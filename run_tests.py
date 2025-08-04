"""
Master Test Suite for TTU Open Report Application

This script runs all test modules in the correct order to validate the application.
"""
import pytest
import sys
import os
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

def run_tests():
    """Run all tests in a specific order"""
    logger.info("Starting TTU Open Report test suite...")
    
    test_order = [
        "tests/test_01_database_connection.py",  # Basic database connectivity
        "tests/test_02_query_functions.py",      # Query functionality
        "tests/test_03_page_loads.py",           # Page imports
        "tests/test_04_data_extraction.py",      # Data extraction
        "tests/test_05_ui_components.py",        # UI components
        "tests/test_06_core_application.py",     # Core application
    ]
    
    # First check if all test files exist
    missing_files = [f for f in test_order if not Path(f).exists()]
    if missing_files:
        logger.error("Missing test files: %s", missing_files)
        return False
    
    success = True
    for test_file in test_order:
        logger.info("Running %s...", test_file)
        result = pytest.main(["-v", test_file])
        
        if result != 0:
            logger.error("Test failed: %s", test_file)
            success = False
        else:
            logger.info("Test passed: %s", test_file)
    
    if success:
        logger.info("All tests passed successfully!")
    else:
        logger.error("Some tests failed. Please check the logs for details.")
    
    return success


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
