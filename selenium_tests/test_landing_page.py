import time
import pytest
from selenium.webdriver.common.by import By

def test_landing_page_loads(driver, app_server):
    driver.get(app_server)
    time.sleep(2)
    assert "GraphiteVision Analytics" in driver.page_source
    assert "Advanced Data Analytics for Toyo Tanso USA" in driver.page_source
    assert driver.find_element(By.CLASS_NAME, "modern-btn")
    assert driver.find_element(By.CLASS_NAME, "fade-in")

def test_logo_present(driver, app_server):
    driver.get(app_server)
    time.sleep(2)
    # Logo should be present on landing page (Streamlit serves images with hashed URLs)
    logo_imgs = driver.find_elements(By.TAG_NAME, "img")
    assert len(logo_imgs) > 0, "No images found on the page"
    # Check that at least one image is served from the media endpoint
    assert any("/media/" in img.get_attribute("src") for img in logo_imgs), "No logo image found"

def test_quick_links(driver, app_server):
    driver.get(app_server)
    time.sleep(2)
    # Check all modern navigation buttons are present
    for label in ["Data Tables", "Analytics", "Reports", "Data Entry"]:
        assert label in driver.page_source

def test_visual_effects(driver, app_server):
    driver.get(app_server)
    time.sleep(2)
    # Check for animated background and fade-in
    body = driver.find_element(By.TAG_NAME, "body")
    style = body.get_attribute("style")
    assert "background" in style or "gradient" in driver.page_source
    # Fade-in class present
    assert driver.find_element(By.CLASS_NAME, "fade-in")
