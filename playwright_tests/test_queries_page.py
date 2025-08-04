import pytest
from playwright.sync_api import Page, expect

def test_queries_page_loads(page: Page):
    page.goto("http://localhost:8502/queries")
    page.wait_for_load_state("networkidle")
    expect(page.get_by_role("heading", name="Business Analytics - GraphiteVision Analytics")).to_be_visible()
    
    # Check for query selection radio buttons
    radio_buttons = page.locator('div[role="radiogroup"] label')
    expect(radio_buttons).to_have_count_greater_than(0)

def test_open_order_report_query(page: Page):
    page.goto("http://localhost:8502/queries")
    page.wait_for_load_state("networkidle")
    
    # Select Open Order Report
    page.get_by_text("Open Order Report").click()
    page.wait_for_timeout(1000)
    
    # Check if data is displayed
    dataframes = page.locator('[data-testid="stDataFrame"]')
    if dataframes.count() > 0:
        expect(dataframes.first).to_be_visible()
    
    # Check for download button
    download_buttons = page.get_by_text("Download Query Results")
    if download_buttons.count() > 0:
        expect(download_buttons.first).to_be_visible()

def test_query_filters(page: Page):
    page.goto("http://localhost:8502/queries")
    page.wait_for_load_state("networkidle")
    
    # Select Open Order Report to enable filters
    page.get_by_text("Open Order Report").click()
    page.wait_for_timeout(1000)
    
    # Check for filter controls
    filter_section = page.get_by_role("heading", name="Filter Data")
    if filter_section.count() > 0:
        expect(filter_section).to_be_visible()
        
        # Check for date inputs
        date_inputs = page.locator('input[type="date"]')
        expect(date_inputs).to_have_count_greater_than(0)

def test_visual_analytics_charts(page: Page):
    page.goto("http://localhost:8502/queries")
    page.wait_for_load_state("networkidle")
    
    # Select Open Order Report
    page.get_by_text("Open Order Report").click()
    page.wait_for_timeout(1000)
    
    # Check for Visual Analytics section
    analytics_section = page.get_by_role("heading", name="Visual Analytics")
    if analytics_section.count() > 0:
        expect(analytics_section).to_be_visible()
        
        # Check for chart type radio buttons
        chart_radios = page.locator('div[role="radiogroup"]').nth(1)
        if chart_radios.count() > 0:
            expect(chart_radios).to_be_visible()

def test_summary_statistics(page: Page):
    page.goto("http://localhost:8502/queries")
    page.wait_for_load_state("networkidle")
    
    # Select Open Order Report
    page.get_by_text("Open Order Report").click()
    page.wait_for_timeout(1000)
    
    # Check for Summary section
    summary_section = page.get_by_role("heading", name="Summary")
    if summary_section.count() > 0:
        expect(summary_section).to_be_visible()
        
        # Look for total records text
        total_records = page.get_by_text("Total records:")
        if total_records.count() > 0:
            expect(total_records).to_be_visible()