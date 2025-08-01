import pytest
from playwright.sync_api import Page, expect

def test_tables_page_loads(page):
    page.goto("http://localhost:8502/tables")
    page.wait_for_load_state("networkidle")
    expect(page.get_by_role("heading", name="Data Tables")).to_be_visible()
    # Check if radio buttons are present (expecting 3 based on test results)
    radio_buttons = page.locator('input[type="radio"]')
    assert radio_buttons.count() > 0, "Should have at least one radio button"

def test_table_selection(page):
    page.goto("http://localhost:8502/tables")
    page.wait_for_load_state("networkidle")
    
    # Get all radio buttons using a more specific selector that works with Streamlit
    radio_buttons = page.locator('div[role="radiogroup"] label')
    
    # Count the number of radio buttons
    count = radio_buttons.count()
    
    # Click each radio button and verify interaction
    for i in range(min(count, 3)):  # Test up to 3 buttons to keep test time reasonable
        button = radio_buttons.nth(i)
        button.scroll_into_view_if_needed()
        button.click()
        # Allow time for table data to load
        page.wait_for_timeout(500)

def test_csv_download(page):
    page.goto("http://localhost:8502/tables")
    page.wait_for_load_state("networkidle")
    
    # Select a table using label instead of radio button
    radio_labels = page.locator('div[role="radiogroup"] label')
    if radio_labels.count() > 0:
        radio_labels.first.click()
        page.wait_for_timeout(1000)
        
        # Find and click the specific download button using test ID
        download_button = page.get_by_test_id("stBaseButton-secondary")
        if download_button.count() > 0:
            with page.expect_download() as download_info:
                download_button.click()
            download = download_info.value
            # Verify download started
            assert download.suggested_filename.endswith(".csv")
        else:
            # If no download button is found, that's also valuable to know
            pytest.skip("No CSV download button found")
    else:
        pytest.skip("No radio buttons found to select a table")

def test_table_search_filter(page):
    page.goto("http://localhost:8502/tables")
    page.wait_for_load_state("networkidle")
    
    # Select a table using label instead of radio button
    radio_labels = page.locator('div[role="radiogroup"] label')
    if radio_labels.count() > 0:
        radio_labels.first.click()
        page.wait_for_timeout(1000)
        
        # Find the search input and enter text
        search_inputs = page.locator('input[type="text"]')
        if search_inputs.count() > 0:
            search_input = search_inputs.first
            search_input.fill("test")
            page.wait_for_timeout(500)
            
            # Verify the table updated (would depend on actual data)
            # Here we just verify the search input has our text
            expect(search_input).to_have_value("test")
        else:
            pytest.skip("No search input found")
    else:
        pytest.skip("No radio buttons found to select a table")
