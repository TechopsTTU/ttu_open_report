import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
import time

class StreamlitTablesPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use Edge browser for tests, specify driver path using Service
        service = Service("C:/edgedriver_win64/msedgedriver.exe")
        cls.driver = webdriver.Edge(service=service)
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:8502/tables")
        time.sleep(3)  # Wait for Streamlit to load

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_tables_page_loads(self):
        self.driver.get("http://localhost:8502/tables")
        time.sleep(1)
        # Check if the Tables page loads and the radio button is present
        self.assertIn("Tables", self.driver.page_source)
        radio_buttons = self.driver.find_elements(By.TAG_NAME, "input")
        self.assertTrue(any(rb.get_attribute("type") == "radio" for rb in radio_buttons))

    def test_table_selection(self):
        self.driver.get("http://localhost:8502/tables")
        time.sleep(2)
        radio_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        for rb in radio_buttons:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", rb)
                if rb.is_displayed() and rb.is_enabled():
                    rb.click()
                    time.sleep(1)
                    self.assertTrue(rb.is_selected())
            except Exception as e:
                print(f"Radio button not interactable: {e}")

    def test_schema_display(self):
        self.driver.get("http://localhost:8502/tables")
        time.sleep(2)
        radio_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
        if radio_buttons:
            try:
                self.driver.execute_script("arguments[0].scrollIntoView();", radio_buttons[0])
                if radio_buttons[0].is_displayed() and radio_buttons[0].is_enabled():
                    radio_buttons[0].click()
                    time.sleep(1)
                    self.assertIn("Schema", self.driver.page_source)
            except Exception as e:
                self.fail(f"Radio button not interactable: {e}")
        else:
            self.fail("No radio buttons found on Tables page.")

    def test_data_preview(self):
        self.driver.get("http://localhost:8502/tables")
        time.sleep(1)
        # Check if data preview table is present
        self.assertIn("Preview", self.driver.page_source)
        tables = self.driver.find_elements(By.TAG_NAME, "table")
        self.assertTrue(len(tables) > 0)

    def test_csv_download(self):
        self.driver.get("http://localhost:8502/tables")
        time.sleep(2)
        self.assertTrue(any("Download" in b.text for b in self.driver.find_elements(By.TAG_NAME, "button")), "Download button not found.")

if __name__ == "__main__":
    unittest.main()
