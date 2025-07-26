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
        cls.driver.get("http://localhost:8501/tables")
        time.sleep(3)  # Wait for Streamlit to load

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_tables_page_loads(self):
        self.driver.get("http://localhost:8501/tables")
        time.sleep(1)
        # Check if the Tables page loads and the radio button is present
        self.assertIn("Tables", self.driver.page_source)
        radio_buttons = self.driver.find_elements(By.TAG_NAME, "input")
        self.assertTrue(any(rb.get_attribute("type") == "radio" for rb in radio_buttons))

    def test_table_selection(self):
        self.driver.get("http://localhost:8501/tables")
        time.sleep(1)
        # Try selecting each table radio button
        radio_buttons = self.driver.find_elements(By.TAG_NAME, "input")
        for rb in radio_buttons:
            if rb.get_attribute("type") == "radio":
                rb.click()
                time.sleep(1)
                self.assertTrue(rb.is_selected())

    def test_schema_display(self):
        self.driver.get("http://localhost:8501/tables")
        time.sleep(1)
        # Check if schema is displayed after table selection
        radio_buttons = self.driver.find_elements(By.TAG_NAME, "input")
        if radio_buttons:
            radio_buttons[0].click()
            time.sleep(1)
            self.assertIn("Schema", self.driver.page_source)
        else:
            self.fail("No radio buttons found on Tables page.")

    def test_data_preview(self):
        self.driver.get("http://localhost:8501/tables")
        time.sleep(1)
        # Check if data preview table is present
        self.assertIn("Preview", self.driver.page_source)
        tables = self.driver.find_elements(By.TAG_NAME, "table")
        self.assertTrue(len(tables) > 0)

    def test_csv_download(self):
        self.driver.get("http://localhost:8501/tables")
        time.sleep(1)
        # Check if download button is present
        self.assertIn("Download CSV", self.driver.page_source)
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        self.assertTrue(any("Download" in b.text for b in buttons))

if __name__ == "__main__":
    unittest.main()
