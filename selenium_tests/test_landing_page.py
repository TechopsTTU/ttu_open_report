import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_landing_page_loads(driver):
    driver.get("http://localhost:8502")
    time.sleep(2)
    assert "Toyo Tanso USA Open Report Dashboard" in driver.page_source
    assert "Welcome to the Toyo Tanso USA Open Report system." in driver.page_source
    assert driver.find_element(By.CLASS_NAME, "quick-link-btn")
    assert driver.find_element(By.CLASS_NAME, "fade-in")

def test_logo_present(driver):
    driver.get("http://localhost:8502")
    time.sleep(2)
    # Logo should be present on landing page (Streamlit serves images with hashed URLs)
    logo_imgs = driver.find_elements(By.TAG_NAME, "img")
    assert len(logo_imgs) > 0, "No images found on the page"
    # Check that at least one image is served from the media endpoint
    assert any("/media/" in img.get_attribute("src") for img in logo_imgs), "No logo image found"

def test_quick_links(driver):
    driver.get("http://localhost:8502")
    time.sleep(2)
    # Check all quick link buttons are present
    for label in ["Tables", "Queries", "Reports", "Forms"]:
        assert driver.find_element(By.LINK_TEXT, label)

def test_visual_effects(driver):
    driver.get("http://localhost:8502")
    time.sleep(2)
    # Check for animated background and fade-in
    body = driver.find_element(By.TAG_NAME, "body")
    style = body.get_attribute("style")
    assert "background" in style or "gradient" in driver.page_source
    # Fade-in class present
    assert driver.find_element(By.CLASS_NAME, "fade-in")
