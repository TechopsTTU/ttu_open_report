"""
Selenium test to verify navigation buttons work correctly
"""
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytest.skip("Selenium tests disabled in this environment", allow_module_level=True)

def test_navigation_buttons_working():
    """Test that all navigation buttons actually work and navigate to correct pages"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to main page
        driver.get("http://localhost:8502")
        time.sleep(3)
        
        # Verify main page loads
        assert "GraphiteVision Analytics" in driver.page_source
        print("✅ Main page loaded successfully")
        
        # Test Data Tables button
        driver.get("http://localhost:8502")
        time.sleep(2)
        
        # Find and click Data Tables link
        tables_link = driver.find_element(By.XPATH, "//a[@href='/tables']")
        tables_link.click()
        time.sleep(2)
        
        # Verify we're on tables page
        assert "/tables" in driver.current_url
        assert "Tables" in driver.page_source
        print("✅ Data Tables button works correctly")
        
        # Test Analytics button
        driver.get("http://localhost:8502")
        time.sleep(2)
        
        analytics_link = driver.find_element(By.XPATH, "//a[@href='/queries']")
        analytics_link.click()
        time.sleep(2)
        
        assert "/queries" in driver.current_url
        assert ("Analytics" in driver.page_source or "Business Analytics" in driver.page_source)
        print("✅ Analytics button works correctly")
        
        # Test Reports button
        driver.get("http://localhost:8502")
        time.sleep(2)
        
        reports_link = driver.find_element(By.XPATH, "//a[@href='/reports']")
        reports_link.click()
        time.sleep(2)
        
        assert "/reports" in driver.current_url
        assert "Reports" in driver.page_source
        print("✅ Reports button works correctly")
        
        # Test Data Entry button
        driver.get("http://localhost:8502")
        time.sleep(2)
        
        forms_link = driver.find_element(By.XPATH, "//a[@href='/forms']")
        forms_link.click()
        time.sleep(2)
        
        assert "/forms" in driver.current_url
        assert ("Forms" in driver.page_source or "Data Entry" in driver.page_source)
        print("✅ Data Entry button works correctly")
        
        print("\n🎉 All navigation buttons are working perfectly!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise e
    finally:
        driver.quit()

if __name__ == "__main__":
    print("Testing GraphiteVision Analytics navigation button functionality...")
    print("Make sure the Streamlit app is running on http://localhost:8502\n")
    test_navigation_buttons_working()
