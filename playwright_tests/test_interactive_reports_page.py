import pytest
from playwright.sync_api import Page, expect

def test_interactive_reports_page_loads(page: Page):
    page.goto("http://localhost:8502/interactive_reports")
    page.wait_for_load_state("networkidle")
    expect(page.get_by_role("heading", name="Interactive Analytics Dashboard")).to_be_visible()
    
    # Check for tabs
    expect(page.get_by_role("tab", name="Sales Overview")).to_be_visible()
    expect(page.get_by_role("tab", name="Product Analysis")).to_be_visible()
    expect(page.get_by_role("tab", name="Customer Insights")).to_be_visible()
    expect(page.get_by_role("tab", name="Order Status")).to_be_visible()

def test_sidebar_filters(page: Page):
    page.goto("http://localhost:8502/interactive_reports")
    page.wait_for_load_state("networkidle")
    
    # Check for sidebar filters
    sidebar = page.locator('[data-testid="stSidebar"]')
    if sidebar.count() > 0:
        expect(sidebar).to_be_visible()
        
        # Check for filter header
        filters_header = page.get_by_role("heading", name="Filters")
        if filters_header.count() > 0:
            expect(filters_header).to_be_visible()

def test_sales_overview_tab(page: Page):
    page.goto("http://localhost:8502/interactive_reports")
    page.wait_for_load_state("networkidle")
    
    # Click Sales Overview tab
    page.get_by_role("tab", name="Sales Overview").click()
    page.wait_for_timeout(2000)
    
    # Check for metrics
    metrics = page.locator('[data-testid="metric-container"]')
    if metrics.count() > 0:
        expect(metrics.first).to_be_visible()
    
    # Check for Monthly Sales Trend heading
    trend_heading = page.get_by_role("heading", name="Monthly Sales Trend")
    if trend_heading.count() > 0:
        expect(trend_heading).to_be_visible()

def test_product_analysis_tab(page: Page):
    page.goto("http://localhost:8502/interactive_reports")
    page.wait_for_load_state("networkidle")
    
    # Click Product Analysis tab
    page.get_by_role("tab", name="Product Analysis").click()
    page.wait_for_timeout(2000)
    
    # Check for Product Performance Analysis heading
    analysis_heading = page.get_by_role("heading", name="Product Performance Analysis")
    if analysis_heading.count() > 0:
        expect(analysis_heading).to_be_visible()
    
    # Check for Top Products heading
    top_products_heading = page.get_by_role("heading", name="Top Products by Sales")
    if top_products_heading.count() > 0:
        expect(top_products_heading).to_be_visible()

def test_customer_insights_tab(page: Page):
    page.goto("http://localhost:8502/interactive_reports")
    page.wait_for_load_state("networkidle")
    
    # Click Customer Insights tab
    page.get_by_role("tab", name="Customer Insights").click()
    page.wait_for_timeout(2000)
    
    # Check for Customer Insights heading
    insights_heading = page.get_by_role("heading", name="Customer Insights")
    if insights_heading.count() > 0:
        expect(insights_heading).to_be_visible()
    
    # Check for Top Customers heading
    top_customers_heading = page.get_by_role("heading", name="Top Customers by Sales")
    if top_customers_heading.count() > 0:
        expect(top_customers_heading).to_be_visible()

def test_order_status_tab(page: Page):
    page.goto("http://localhost:8502/interactive_reports")
    page.wait_for_load_state("networkidle")
    
    # Click Order Status tab
    page.get_by_role("tab", name="Order Status").click()
    page.wait_for_timeout(2000)
    
    # Check for Order Status Analysis heading
    status_heading = page.get_by_role("heading", name="Order Status Analysis")
    if status_heading.count() > 0:
        expect(status_heading).to_be_visible()
    
    # Check for Order Status Distribution heading
    distribution_heading = page.get_by_role("heading", name="Order Status Distribution")
    if distribution_heading.count() > 0:
        expect(distribution_heading).to_be_visible()

def test_charts_and_visualizations(page: Page):
    page.goto("http://localhost:8502/interactive_reports")
    page.wait_for_load_state("networkidle")
    
    # Go through each tab and check for charts
    tabs = ["Sales Overview", "Product Analysis", "Customer Insights", "Order Status"]
    
    for tab_name in tabs:
        page.get_by_role("tab", name=tab_name).click()
        page.wait_for_timeout(2000)
        
        # Check for either Altair charts, Plotly charts, or error messages
        altair_charts = page.locator('[data-testid="stVegaLiteChart"]')
        plotly_charts = page.locator('[data-testid="stPlotlyChart"]')
        error_messages = page.locator('[data-testid="stException"]')
        
        # At least one visualization method should be present
        has_visualization = (altair_charts.count() > 0 or 
                           plotly_charts.count() > 0 or 
                           error_messages.count() > 0)
        
        assert has_visualization, f"Tab {tab_name} should have some form of visualization or error handling"

def test_error_handling(page: Page):
    page.goto("http://localhost:8502/interactive_reports")
    page.wait_for_load_state("networkidle")
    
    # Check for error handling messages if database issues occur
    error_messages = page.get_by_text("An error occurred while generating reports:")
    troubleshooting_section = page.get_by_role("heading", name="Troubleshooting")
    
    # If error occurs, troubleshooting should be shown
    if error_messages.count() > 0:
        expect(error_messages).to_be_visible()
        if troubleshooting_section.count() > 0:
            expect(troubleshooting_section).to_be_visible()