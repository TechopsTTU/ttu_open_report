import time
import requests

def wait_for_streamlit(url="http://localhost:8502", timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print(f"Streamlit server is up at {url}")
                return True
        except Exception:
            pass
        print("Waiting for Streamlit server...")
        time.sleep(2)
    print(f"Streamlit server not available after {timeout} seconds.")
    return False

if __name__ == "__main__":
    wait_for_streamlit()
