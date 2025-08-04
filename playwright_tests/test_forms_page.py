import pytest
from playwright.sync_api import Page, expect

def test_forms_page_loads(page: Page):
    page.goto("http://localhost:8502/forms")
    page.wait_for_load_state("networkidle")
    expect(page.get_by_role("heading", name="Business Data Entry Portal")).to_be_visible()
    
    # Check for tabs
    expect(page.get_by_role("tab", name="New Customer Order")).to_be_visible()
    expect(page.get_by_role("tab", name="Product Management")).to_be_visible()
    expect(page.get_by_role("tab", name="Customer Information")).to_be_visible()

def test_customer_order_form(page: Page):
    page.goto("http://localhost:8502/forms")
    page.wait_for_load_state("networkidle")
    
    # Select the New Customer Order tab
    page.get_by_role("tab", name="New Customer Order").click()
    
    # Fill out the order form
    page.fill('input[placeholder="Enter unique order ID"]', "TEST-ORD-001")
    page.fill('input[placeholder="Customer code (e.g., ACMECORP)"]', "TESTCORP")
    page.fill('input[placeholder="Full company name"]', "Test Corporation Inc")
    page.fill('input[placeholder="Customer\'s purchase order"]', "PO-12345")
    page.fill('input[placeholder="Enter product code"]', "TEST-PART-001")
    page.fill('input[placeholder="Product description"]', "Test Product Description")
    
    # Verify form fields are filled
    expect(page.locator('input[placeholder="Enter unique order ID"]')).to_have_value("TEST-ORD-001")
    expect(page.locator('input[placeholder="Customer code (e.g., ACMECORP)"]')).to_have_value("TESTCORP")

def test_product_management_form(page: Page):
    page.goto("http://localhost:8502/forms")
    page.wait_for_load_state("networkidle")
    
    # Select the Product Management tab
    page.get_by_role("tab", name="Product Management").click()
    
    # Fill out product form
    page.fill('input[placeholder="Unique product code"]', "TEST-PROD-001")
    page.fill('input[placeholder="Product display name"]', "Test Product Name")
    
    # Select category from dropdown
    page.select_option('select', 'Graphite Components')
    
    # Verify fields are filled
    expect(page.locator('input[placeholder="Unique product code"]')).to_have_value("TEST-PROD-001")
    expect(page.locator('input[placeholder="Product display name"]')).to_have_value("Test Product Name")

def test_customer_information_form(page: Page):
    page.goto("http://localhost:8502/forms")
    page.wait_for_load_state("networkidle")
    
    # Select the Customer Information tab
    page.get_by_role("tab", name="Customer Information").click()
    
    # Fill out customer form
    page.fill('input[placeholder="Unique customer code"]', "TEST-CUST-001")
    page.fill('input[placeholder="Full legal company name"]', "Test Customer Corp")
    page.fill('input[placeholder="Contact person name"]', "John Doe")
    page.fill('input[placeholder="contact@company.com"]', "john@testcorp.com")
    
    # Verify fields are filled
    expect(page.locator('input[placeholder="Unique customer code"]')).to_have_value("TEST-CUST-001")
    expect(page.locator('input[placeholder="Full legal company name"]')).to_have_value("Test Customer Corp")

def test_recent_activity_section(page: Page):
    page.goto("http://localhost:8502/forms")
    page.wait_for_load_state("networkidle")
    
    # Check if Recent Form Submissions section is visible
    expect(page.get_by_role("heading", name="Recent Form Submissions")).to_be_visible()
    
    # The section should either show data or a message
    recent_section = page.locator('text="Recent Form Submissions"').locator("..").locator("..")
    expect(recent_section).to_be_visible()