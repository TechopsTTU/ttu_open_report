import pytest
from playwright.sync_api import Page, expect

def test_open_order_report_page_loads(page: Page):
    page.goto("http://localhost:8503/open_order_report")
    expect(page).to_have_title("Open Order Report")
    expect(page.locator("text=Open Order Report")).to_be_visible()

def test_open_order_report_data_display(page: Page):
    page.goto("http://localhost:8503/open_order_report")
    page.locator("text=Run Report").click()
    expect(page.locator(".dataframe")).to_be_visible()
    expect(page.locator("text=Download CSV")).to_be_visible()
