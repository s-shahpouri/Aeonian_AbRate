import os
import requests
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class ProductScraper:
    def __init__(self, folder, base_url, search_query, secret_word) -> None:
        self.folder = folder
        self.base_url = base_url
        self.search_query = search_query
        self.secret_word = secret_word

    def is_valid_product(self, product_name):
        product_name = product_name.lower()
        if search_query in product_name and secret_word in product_name and "anti" in product_name:
            print(product_name)
            return True

    def find_xhr_url(self):
        # Initialize ChromeDriver
        driver = webdriver.Chrome()

        # Open the website
        driver.get(self.base_url)

        # Assuming you need to execute a search to trigger the XHR request
        # Replace 'q' with the actual name or ID of the search box
        search_box = driver.find_element(By.XPATH, '//*[@id="searchBoxId"]')
        search_box.send_keys(self.search_query)
        search_box.send_keys(Keys.RETURN)

        # Pause to allow XHR request to complete
        time.sleep(5)

        # Extracting all network requests
        xhr_url = None
        for entry in driver.execute_script("return window.performance.getEntries();"):
            if entry['initiatorType'] == 'xmlhttprequest':
                match = re.search(
                    rf'(?i){re.escape(self.base_url)}/_next/data/([a-zA-Z0-9]+)/en-nl/search.json\?sorting=relevance&keywords={re.escape(self.search_query)}', entry['name'])
                if match:
                    xhr_url = match.group(0)
                    break

        # Close the browser
        driver.quit()

        return xhr_url

    def scrape_products(self):
        # Create a directory to store the scraped product data
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        # Find the XHR URL dynamically
        xhr_url = self.find_xhr_url()

        if not xhr_url:
            print("Could not find the XHR URL.")
            return

        # Fetch the data from the XHR URL
        response = requests.get(xhr_url)
        print(response.text)

        if response.status_code == 200:
            # Save the JSON response to a local file
            with open(f"{self.folder}/{self.search_query}_data.json", 'w', encoding='utf-8') as json_file:
                json.dump(response.json(), json_file,
                          indent=4, ensure_ascii=False)

            # Parse the JSON response
            product_data = response.json().get('pageProps', {}).get(
                'searchResults', {}).get('items', [])

            # Extract and save product information
            for product in product_data:
                product_name = product.get('productName', 'Unknown')
                # print(product_name)

                if self.is_valid_product(product_name):
                    # print("......")
                    product_price = product.get('Price', 'N/A')
                    product_description = product.get('Description', 'N/A')

                    # Store the product information in a dictionary
                    product_info = {
                        'Name': product_name,
                        'Price': product_price,
                        'Description': product_description
                    }

                    # Save the product data as a JSON file
                    filename = f"{self.folder}/{product_name}.json"
                    with open(filename, 'w', encoding='utf-8') as json_file:
                        json.dump(product_info, json_file,
                                  indent=4, ensure_ascii=False)
        else:
            print(
                f"Failed to retrieve data. Status code: {response.status_code}")


if __name__ == "__main__":
    folder_to_save_data = "abcam_products"
    base_url = "https://www.abcam.com"
    search_query = "AKT3".lower()
    secret_word = "EPR".lower()

    scraper = ProductScraper(
        folder_to_save_data, base_url, search_query, secret_word)
    scraper.scrape_products()
