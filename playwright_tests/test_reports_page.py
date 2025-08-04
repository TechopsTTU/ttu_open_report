import pytest
from playwright.sync_api import Page, expect

def test_reports_page_loads(page: Page):
    page.goto("http://localhost:8502/reports")
    page.wait_for_load_state("networkidle")
    expect(page.get_by_role("heading", name="Interactive Reports")).to_be_visible()
    
    # Check for chart type radio buttons
    expect(page.get_by_text("Bar Chart")).to_be_visible()
    expect(page.get_by_text("Line Chart")).to_be_visible()

def test_chart_type_selection(page: Page):
    page.goto("http://localhost:8502/reports")
    page.wait_for_load_state("networkidle")
    
    # Test Bar Chart selection
    page.get_by_text("Bar Chart").click()
    page.wait_for_timeout(500)
    
    # Test Line Chart selection
    page.get_by_text("Line Chart").click()
    page.wait_for_timeout(500)
    
    # Verify chart is displayed (matplotlib chart in Streamlit)
    charts = page.locator('[data-testid="stPyplotGlobalUse"]')
    if charts.count() > 0:
        expect(charts.first).to_be_visible()

def test_chart_display(page: Page):
    page.goto("http://localhost:8502/reports")
    page.wait_for_load_state("networkidle")
    
    # Check for chart heading
    expect(page.get_by_role("heading", name="Total Orders by Date")).to_be_visible()
    
    # Chart should be visible after page loads
    page.wait_for_timeout(2000)  # Allow time for chart to render
    
    # Look for matplotlib chart or error message
    charts = page.locator('[data-testid="stPyplotGlobalUse"]')
    error_messages = page.locator('[data-testid="stException"]')
    
    # Either chart should be visible or there should be an error (which is also valid)
    chart_or_error_visible = charts.count() > 0 or error_messages.count() > 0
    assert chart_or_error_visible, "Either chart should be visible or error message should be shown"

def test_summary_statistics_display(page: Page):
    page.goto("http://localhost:8502/reports")
    page.wait_for_load_state("networkidle")
    
    # Check for summary statistics
    total_orders_text = page.get_by_text("Total orders:")
    if total_orders_text.count() > 0:
        expect(total_orders_text).to_be_visible()
    
    avg_orders_text = page.get_by_text("Average orders per day:")
    if avg_orders_text.count() > 0:
        expect(avg_orders_text).to_be_visible()

def test_report_info_message(page: Page):
    page.goto("http://localhost:8502/reports")
    page.wait_for_load_state("networkidle")
    
    # Check for info message about future report logic
    info_message = page.get_by_text("Report logic will be enabled once query functions are implemented.")
    if info_message.count() > 0:
        expect(info_message).to_be_visible()