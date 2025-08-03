"""
Playwright configuration for UI testing with visible browser
"""
from playwright.sync_api import sync_playwright

def pytest_configure(config):
    """Configure Playwright to run with visible browser"""
    config.option.headed = True
    config.option.browser_name = "chromium"
    config.option.slowmo = 500  # Slow down for better visibility

def test_configuration():
    """Test configuration for browser visibility"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # Show browser window
            slow_mo=500,     # Slow down operations
            devtools=True,   # Open dev tools
            args=[
                '--start-maximized',
                '--disable-web-security',
                '--allow-running-insecure-content'
            ]
        )
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            record_video_dir='test-results/videos/',
            record_video_size={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        return page