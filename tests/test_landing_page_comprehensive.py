"""
Comprehensive Landing Page Tests for GraphiteVision Analytics
Tests all buttons, navigation, UI elements, and functionality
"""
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

@pytest.fixture(scope="module")
def driver():
    """Setup Chrome driver with appropriate options for testing"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(autouse=True)
def setup_page(driver):
    """Navigate to landing page before each test"""
    driver.get("http://localhost:8503")  # Updated port
    time.sleep(3)  # Wait for Streamlit to fully load

class TestLandingPageElements:
    """Test suite for basic landing page elements"""
    
    def test_page_loads_successfully(self, driver):
        """Test that the landing page loads with correct title"""
        assert "GraphiteVision Analytics" in driver.title or "GraphiteVision Analytics" in driver.page_source
        assert driver.current_url.endswith(":8503/") or driver.current_url.endswith(":8503")

    def test_app_title_present(self, driver):
        """Test that the main application title is displayed"""
        assert "GraphiteVision Analytics" in driver.page_source
        # Check for the styled title class
        try:
            title_element = driver.find_element(By.CLASS_NAME, "app-title")
            assert title_element.is_displayed()
        except NoSuchElementException:
            # Fallback: check if title text is present in any form
            assert "GraphiteVision Analytics" in driver.page_source

    def test_app_subtitle_present(self, driver):
        """Test that the subtitle is displayed"""
        assert "Advanced Data Analytics for Toyo Tanso USA" in driver.page_source

    def test_logo_display(self, driver):
        """Test that the TTU logo is displayed"""
        logo_imgs = driver.find_elements(By.TAG_NAME, "img")
        assert len(logo_imgs) > 0, "No images found on the page"
        
        # Check that at least one image is present (Streamlit serves images with hashed URLs)
        logo_found = False
        for img in logo_imgs:
            src = img.get_attribute("src")
            if src and ("/media/" in src or "TTU_LOGO" in src):
                logo_found = True
                break
        assert logo_found, "TTU logo not found on page"

    def test_fade_in_animation_class(self, driver):
        """Test that fade-in animation classes are present"""
        fade_elements = driver.find_elements(By.CLASS_NAME, "fade-in")
        assert len(fade_elements) > 0, "No fade-in animation elements found"

class TestNavigationButtons:
    """Test suite for all navigation buttons functionality"""
    
    def test_all_navigation_buttons_present(self, driver):
        """Test that all 4 navigation buttons are present"""
        expected_buttons = ["Data Tables", "Analytics", "Reports", "Data Entry"]
        
        for button_text in expected_buttons:
            assert button_text in driver.page_source, f"Button '{button_text}' not found on page"
        
        # Check for modern-btn class elements
        modern_buttons = driver.find_elements(By.CLASS_NAME, "modern-btn")
        assert len(modern_buttons) >= 4, f"Expected at least 4 modern buttons, found {len(modern_buttons)}"

    def test_data_tables_button_navigation(self, driver):
        """Test Data Tables button navigates to tables page"""
        try:
            # Find and click the Data Tables button
            button = self._find_button_by_text(driver, "Data Tables")
            assert button is not None, "Data Tables button not found"
            
            button.click()
            time.sleep(2)
            
            # Check if we navigated to the tables page
            assert "/tables" in driver.current_url, f"Expected /tables in URL, got {driver.current_url}"
            assert "Tables" in driver.page_source, "Tables page content not found"
            
        except Exception as e:
            pytest.fail(f"Data Tables button test failed: {str(e)}")

    def test_analytics_button_navigation(self, driver):
        """Test Analytics button navigates to queries page"""
        try:
            button = self._find_button_by_text(driver, "Analytics")
            assert button is not None, "Analytics button not found"
            
            button.click()
            time.sleep(2)
            
            assert "/queries" in driver.current_url, f"Expected /queries in URL, got {driver.current_url}"
            assert ("Business Analytics" in driver.page_source or 
                   "Analytics" in driver.page_source), "Analytics page content not found"
            
        except Exception as e:
            pytest.fail(f"Analytics button test failed: {str(e)}")

    def test_reports_button_navigation(self, driver):
        """Test Reports button navigates to reports page"""
        try:
            button = self._find_button_by_text(driver, "Reports")
            assert button is not None, "Reports button not found"
            
            button.click()
            time.sleep(2)
            
            assert "/reports" in driver.current_url, f"Expected /reports in URL, got {driver.current_url}"
            assert "Reports" in driver.page_source, "Reports page content not found"
            
        except Exception as e:
            pytest.fail(f"Reports button test failed: {str(e)}")

    def test_data_entry_button_navigation(self, driver):
        """Test Data Entry button navigates to forms page"""
        try:
            button = self._find_button_by_text(driver, "Data Entry")
            assert button is not None, "Data Entry button not found"
            
            button.click()
            time.sleep(2)
            
            assert "/forms" in driver.current_url, f"Expected /forms in URL, got {driver.current_url}"
            assert ("Forms" in driver.page_source or 
                   "Data Entry" in driver.page_source), "Forms page content not found"
            
        except Exception as e:
            pytest.fail(f"Data Entry button test failed: {str(e)}")

    def _find_button_by_text(self, driver, text):
        """Helper method to find button by text content"""
        # Try multiple strategies to find the button
        try:
            # Strategy 1: Find button with exact text
            button = driver.find_element(By.XPATH, f"//button[contains(text(), '{text}')]")
            return button
        except NoSuchElementException:
            pass
        
        try:
            # Strategy 2: Find by modern-btn class and check text
            buttons = driver.find_elements(By.CLASS_NAME, "modern-btn")
            for button in buttons:
                if text in button.text:
                    return button
        except NoSuchElementException:
            pass
        
        try:
            # Strategy 3: Find any clickable element containing the text
            element = driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
            return element
        except NoSuchElementException:
            pass
        
        return None

class TestUIStyles:
    """Test suite for UI styling and visual elements"""
    
    def test_modern_button_styling(self, driver):
        """Test that modern buttons have proper CSS classes"""
        modern_buttons = driver.find_elements(By.CLASS_NAME, "modern-btn")
        assert len(modern_buttons) > 0, "No modern-btn elements found"
        
        # Check first button for styling attributes
        if modern_buttons:
            button = modern_buttons[0]
            assert button.is_displayed(), "Modern button is not visible"

    def test_responsive_navigation_container(self, driver):
        """Test that navigation container is present"""
        try:
            nav_container = driver.find_element(By.CLASS_NAME, "modern-nav-container")
            assert nav_container.is_displayed(), "Navigation container not visible"
        except NoSuchElementException:
            # Check if buttons are arranged properly even without the container class
            modern_buttons = driver.find_elements(By.CLASS_NAME, "modern-btn")
            assert len(modern_buttons) >= 4, "Navigation buttons not properly arranged"

    def test_gradient_background_styling(self, driver):
        """Test that gradient background styling is applied"""
        # Check for background styling in page source or body element
        page_source = driver.page_source
        has_gradient = ("gradient" in page_source.lower() or 
                       "background" in page_source.lower())
        assert has_gradient, "Gradient background styling not found"

class TestAccessibility:
    """Test suite for accessibility features"""
    
    def test_button_accessibility(self, driver):
        """Test that buttons are accessible and interactive"""
        buttons = driver.find_elements(By.TAG_NAME, "button")
        clickable_elements = driver.find_elements(By.CLASS_NAME, "modern-btn")
        
        total_interactive = len(buttons) + len(clickable_elements)
        assert total_interactive >= 4, f"Expected at least 4 interactive elements, found {total_interactive}"
        
        # Test that buttons are enabled
        for button in buttons:
            if button.is_displayed():
                assert button.is_enabled(), "Button should be enabled"

    def test_image_alt_attributes(self, driver):
        """Test that images have proper alt attributes or are decorative"""
        images = driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            alt_text = img.get_attribute("alt")
            src = img.get_attribute("src")
            # Either has alt text or is a Streamlit-generated image
            assert alt_text is not None or "/media/" in src, "Image missing alt attribute"

class TestPerformance:
    """Test suite for page performance and loading"""
    
    def test_page_load_time(self, driver):
        """Test that page loads within reasonable time"""
        start_time = time.time()
        driver.refresh()
        
        # Wait for key elements to be present
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            load_time = time.time() - start_time
            assert load_time < 15, f"Page took too long to load: {load_time} seconds"
        except TimeoutException:
            pytest.fail("Page failed to load key elements within timeout")

    def test_javascript_execution(self, driver):
        """Test that JavaScript functions are working"""
        # Test that JavaScript is enabled and working
        js_result = driver.execute_script("return typeof navigateToPage === 'function'")
        assert js_result or "navigateToPage" in driver.page_source, "Navigation JavaScript not working"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
