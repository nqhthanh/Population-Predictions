from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

class DataCrawler:
    def __init__(self):
        # Initialize the WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.base_url = "https://danso.org/the-gioi/"
        self.dataframes = []

    def crawl_data(self):
        # Navigate to the base URL
        self.driver.get(self.base_url)
        time.sleep(5)  # Allow time for the page to load

        # Find all h3 tags and their corresponding href links
        h3_elements = self.driver.find_elements(By.TAG_NAME, 'h3')
        href_links = [h3.find_element(By.TAG_NAME, 'a').get_attribute('href') for h3 in h3_elements if h3.find_element(By.TAG_NAME, 'a')]

        # Iterate through each link found in h3 tags
        for link in href_links:
            self.driver.get(link)
            time.sleep(3)  # Allow time for the page to load

            # Find all the H1 tag to set the name of the Country
            h1_element = self.driver.find_element(By.TAG_NAME, 'h1')
            country_name = h1_element.text if h1_element else "Unknown"

            # Find the first table in the page
            tables = self.driver.find_elements(By.TAG_NAME, 'table')
            if tables:
                # Convert table to DataFrame
                df = pd.read_html(tables[0].get_attribute('outerHTML'))[0]
                df['country'] = country_name
                # Append the DataFrame to the list
                self.dataframes.append(df)

    def get_final_dataframe(self):
        # Concatenate all dataframes into one, ignoring indexes and handling different column lengths
        final_dataframe = pd.concat(self.dataframes, ignore_index=True, sort=False)
        return final_dataframe

    def close_driver(self):
        # Close the driver
        self.driver.quit()

