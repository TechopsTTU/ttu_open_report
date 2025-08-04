from selenium import webdriver
import pytest

# List of page URLs relative to the base URL
PAGES = [
    "/",          # Homepage
    "/about",     # About page
    "/contact",   # Contact page
    # ...other pages...
]

@pytest.fixture(scope="module")
def driver():
	drv = webdriver.Chrome()  # adjust driver as needed
	yield drv
	drv.quit()

def test_all_pages_load(driver):
	base_url = "http://localhost:8000"  # adjust base URL as needed for production
	for page in PAGES:
		driver.get(base_url + page)
		assert driver.title, f"Page {page} did not load properly"