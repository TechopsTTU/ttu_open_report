import subprocess
import time
import requests
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def app_server():
    proc = subprocess.Popen([
        "streamlit", "run", "app.py",
        "--server.headless", "true",
        "--server.port", "8507"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # give the server time to start
    time.sleep(5)
    yield "http://localhost:8507"
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()

@pytest.fixture()
def driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-data-dir=/tmp/chromedata-pytest')
    try:
        drv = webdriver.Chrome(options=options)
    except Exception:
        pytest.skip("Chrome driver not available")
    yield drv
    drv.quit()
