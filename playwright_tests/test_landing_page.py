import pytest
from playwright.sync_api import Page, expect

def test_landing_page_loads(page):
    page.goto("http://localhost:8502")
    expect(page).to_have_title("GraphiteVision Analytics")
    expect(page.locator("text=Advanced Data Analytics for Toyo Tanso USA")).to_be_visible()
    expect(page.locator(".modern-btn").first).to_be_visible()
    # Check for visible fade-in elements (skip the first hidden one)
    expect(page.locator(".fade-in").nth(1)).to_be_visible()

def test_logo_present(page):
    page.goto("http://localhost:8502")
    # Logo should be present on landing page (Streamlit serves images with hashed URLs)
    logo_imgs = page.locator("img")
    expect(logo_imgs).to_have_count(1)  # At least 1 image
    
    # Check for any image served from the media endpoint
    imgs_with_media = page.locator('img[src*="/media/"]')
    expect(imgs_with_media).to_have_count(1)  # At least 1 media image

def test_quick_links(page):
    page.goto("http://localhost:8502")
    # Check all modern navigation buttons are present using more specific selectors
    expect(page.get_by_role("button", name="📊 Data Tables")).to_be_visible()
    expect(page.get_by_role("button", name="🔍 Analytics")).to_be_visible()
    expect(page.get_by_role("button", name="📈 Reports")).to_be_visible()
    expect(page.get_by_role("button", name="📝 Data Entry")).to_be_visible()

def test_visual_effects(page):
    page.goto("http://localhost:8502")
    # Check CSS animations are defined by looking for visible fade-in elements
    # Skip the first hidden element and check for a visible one
    expect(page.locator(".fade-in").nth(1)).to_be_visible()
