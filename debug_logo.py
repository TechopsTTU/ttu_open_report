import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost:8502")
    time.sleep(3)
    
    print("Page source contains TTU_LOGO.jpg:", "TTU_LOGO.jpg" in driver.page_source)
    
    logo_imgs = driver.find_elements(By.TAG_NAME, "img")
    print(f"Found {len(logo_imgs)} images")
    for i, img in enumerate(logo_imgs):
        src = img.get_attribute("src")
        print(f"Image {i}: {src}")
        
finally:
    driver.quit()
