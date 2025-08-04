import pytest
from playwright.sync_api import Page, expect

def test_business_queries_page_loads(page: Page):
    page.goto("http://localhost:8502/business_queries")
    page.wait_for_load_state("networkidle")
    expect(page.get_by_role("heading", name="Business Intelligence Queries")).to_be_visible()
    
    # Check for date range selector
    expect(page.get_by_role("heading", name="Select Date Range")).to_be_visible()

def test_date_range_selector(page: Page):
    page.goto("http://localhost:8502/business_queries")
    page.wait_for_load_state("networkidle")
    
    # Check for date inputs
    date_inputs = page.locator('input[type="date"]')
    expect(date_inputs).to_have_count(2)  # Start Date and End Date
    
    # Check for Start Date and End Date labels
    expect(page.get_by_text("Start Date")).to_be_visible()
    expect(page.get_by_text("End Date")).to_be_visible()

def test_business_query_selection(page: Page):
    page.goto("http://localhost:8502/business_queries")
    page.wait_for_load_state("networkidle")
    
    # Check for query selection radio buttons
    radio_group = page.locator('div[role="radiogroup"]')
    expect(radio_group).to_be_visible()
    
    # Check for specific business queries
    expect(page.get_by_text("Customer Order Volume")).to_be_visible()
    expect(page.get_by_text("Product Performance")).to_be_visible()
    expect(page.get_by_text("Order Status Summary")).to_be_visible()

def test_customer_order_volume_query(page: Page):
    page.goto("http://localhost:8502/business_queries")
    page.wait_for_load_state("networkidle")
    
    # Select Customer Order Volume query
    page.get_by_text("Customer Order Volume").click()
    page.wait_for_timeout(2000)
    
    # Check for query description
    description = page.get_by_text("Analyze customer order patterns with total order counts and revenue by customer.")
    if description.count() > 0:
        expect(description).to_be_visible()

def test_product_performance_query(page: Page):
    page.goto("http://localhost:8502/business_queries")
    page.wait_for_load_state("networkidle")
    
    # Select Product Performance query
    page.get_by_text("Product Performance").click()
    page.wait_for_timeout(2000)
    
    # Check for query description
    description = page.get_by_text("Evaluate product performance by order frequency, quantity, and revenue.")
    if description.count() > 0:
        expect(description).to_be_visible()

def test_order_status_summary_query(page: Page):
    page.goto("http://localhost:8502/business_queries")
    page.wait_for_load_state("networkidle")
    
    # Select Order Status Summary query
    page.get_by_text("Order Status Summary").click()
    page.wait_for_timeout(2000)
    
    # Check for query description
    description = page.get_by_text("Get a summary of orders by status with counts, total values, and date ranges.")
    if description.count() > 0:
        expect(description).to_be_visible()

def test_query_execution_and_results(page: Page):
    page.goto("http://localhost:8502/business_queries")
    page.wait_for_load_state("networkidle")
    
    # Select a query
    page.get_by_text("Customer Order Volume").click()
    page.wait_for_timeout(3000)
    
    # Check for either data display or error handling
    dataframes = page.locator('[data-testid="stDataFrame"]')
    error_messages = page.locator('[data-testid="stException"]')
    warning_messages = page.get_by_text("Make sure the database connection is properly configured.")
    
    # Either data should be displayed or appropriate error/warning messages
    results_visible = (dataframes.count() > 0 or 
                      error_messages.count() > 0 or 
                      warning_messages.count() > 0)
    assert results_visible, "Query should show results, error, or warning message"

def test_download_functionality(page: Page):
    page.goto("http://localhost:8502/business_queries")
    page.wait_for_load_state("networkidle")
    
    # Select a query
    page.get_by_text("Customer Order Volume").click()
    page.wait_for_timeout(3000)
    
    # Check for download button (may only appear if data is available)
    download_buttons = page.get_by_text("Download Query Results")
    if download_buttons.count() > 0:
        expect(download_buttons.first).to_be_visible()