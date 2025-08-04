#!/usr/bin/env python3
"""
Run Playwright tests with visible browser for UI debugging
"""
import subprocess
import sys
import time
import threading
from pathlib import Path

def start_streamlit():
    """Start Streamlit server in background"""
    try:
        cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8502", "--server.headless=true"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Starting Streamlit server on port 8502...")
        return process
    except Exception as e:
        print(f"Failed to start Streamlit: {e}")
        return None

def wait_for_server():
    """Wait for Streamlit server to be ready"""
    import urllib.request
    import urllib.error
    
    for i in range(30):  # Wait up to 30 seconds
        try:
            urllib.request.urlopen("http://localhost:8502", timeout=2)
            print("Streamlit server is ready!")
            return True
        except urllib.error.URLError:
            print(f"Waiting for server... ({i+1}/30)")
            time.sleep(1)
    
    print("Server failed to start within 30 seconds")
    return False

def run_playwright_tests():
    """Run Playwright tests with visible browser"""
    print("Running Playwright tests with visible browser...")
    
    # Set environment variables for visible browser
    env = {
        "PWDEBUG": "1",  # Enable debug mode
    }
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "playwright_tests/",
        "--headed",  # Show browser
        "--slowmo=500",  # Slow down for visibility
        "-v",  # Verbose output
        "--tb=short"  # Short traceback format
    ]
    
    try:
        result = subprocess.run(cmd, env={**subprocess.os.environ, **env}, check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to run tests: {e}")
        return False

def main():
    """Main function to orchestrate test run"""
    print("Setting up UI test environment...")
    
    # Start Streamlit server
    streamlit_process = start_streamlit()
    if not streamlit_process:
        return 1
    
    try:
        # Wait for server to be ready
        if not wait_for_server():
            return 1
        
        # Run tests
        success = run_playwright_tests()
        
        if success:
            print("All tests passed!")
            return 0
        else:
            print("Some tests failed. Check output above.")
            return 1
            
    finally:
        # Clean up: terminate Streamlit server
        if streamlit_process:
            streamlit_process.terminate()
            print("Stopped Streamlit server")

if __name__ == "__main__":
    exit(main())