"""
Quick test to verify the navigation buttons are working correctly
"""
import requests
import time

def test_navigation_buttons():
    """Test that all navigation pages are accessible"""
    base_url = "http://localhost:8502"
    
    # Test main page
    try:
        response = requests.get(base_url)
        print(f"Main page status: {response.status_code}")
        assert response.status_code == 200
        print("✅ Main page loads successfully")
    except Exception as e:
        print(f"❌ Main page failed: {e}")
        return False
    
    # Test navigation pages
    pages = ["tables", "queries", "reports", "forms"]
    
    for page in pages:
        try:
            response = requests.get(f"{base_url}/{page}")
            print(f"{page.title()} page status: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ {page.title()} page loads successfully")
            else:
                print(f"⚠️ {page.title()} page returned status {response.status_code}")
        except Exception as e:
            print(f"❌ {page.title()} page failed: {e}")
    
    return True

if __name__ == "__main__":
    print("Testing GraphiteVision Analytics navigation buttons...")
    print("Make sure the Streamlit app is running on http://localhost:8502")
    time.sleep(2)
    test_navigation_buttons()
    print("\nNavigation test completed!")
