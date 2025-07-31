import time
import pytest
from selenium.webdriver.common.by import By

@pytest.mark.usefixtures("app_server")
def test_tables_page_loads(driver, app_server):
    driver.get(f"{app_server}/tables")
    time.sleep(1)
    assert "Tables" in driver.page_source
    radio_buttons = driver.find_elements(By.TAG_NAME, "input")
    assert any(rb.get_attribute("type") == "radio" for rb in radio_buttons)

@pytest.mark.usefixtures("app_server")
def test_csv_download_button_present(driver, app_server):
    driver.get(f"{app_server}/tables")
    time.sleep(1)
    assert any("Download" in b.text for b in driver.find_elements(By.TAG_NAME, "button"))
