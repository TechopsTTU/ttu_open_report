import pytest

def pytest_configure(config):
    # This helps ensure that the Streamlit app is running before tests start
    config.addinivalue_line(
        "markers", "requires_streamlit: mark test as requiring a running Streamlit app"
    )

@pytest.fixture(scope="session", autouse=True)
def check_streamlit_running(request):
    """Check if Streamlit app is running at http://localhost:8502"""
    import urllib.request
    import urllib.error
    import time
    
    # Skip check if the test is not marked as requiring Streamlit
    for item in request.node.items:
        if "requires_streamlit" not in item.keywords:
            return
    
    # Try to connect to Streamlit server
    max_retries = 3
    for i in range(max_retries):
        try:
            urllib.request.urlopen("http://localhost:8502", timeout=5)
            # If we get here, the server is running
            return
        except urllib.error.URLError:
            if i < max_retries - 1:
                print(f"Waiting for Streamlit server to start (attempt {i+1}/{max_retries})...")
                time.sleep(2)
            else:
                pytest.skip("Streamlit server not running on http://localhost:8502. Start it with 'streamlit run app.py --server.port=8502'")
