import pytest
import requests

@pytest.mark.usefixtures("app_server")
def test_initialization(app_server):
    resp = requests.get(app_server)
    assert resp.status_code == 200

@pytest.mark.usefixtures("app_server")
def test_sanity_homepage(driver, app_server):
    driver.get(app_server)
    assert "GraphiteVision Analytics" in driver.page_source

@pytest.mark.usefixtures("app_server")
def test_smoke_navigation(driver, app_server):
    for page in ["/tables", "/queries", "/reports", "/forms"]:
        driver.get(f"{app_server}{page}")
        assert driver.title or "GraphiteVision" in driver.page_source
