import os
import requests
import json


class ProductScraper:
    def __init__(self, folder, base_url, search_query) -> None:
        self.folder = folder
        self.base_url = base_url
        self.search_query = search_query

    def is_valid_product(self, product_name):
        # Check if product_name contains "AKT2" and "EPR"
        if "AKT2" in product_name and "EPR" in product_name:
            # Check if there are no other numbers in the product_name
            if not any(char.isdigit() for char in product_name):
                return True
        return False

    def scrape_products(self):
        # Create a directory to store the scraped product data
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        # Send a GET request to the XHR endpoint for product data
        xhr_url = f"{self.base_url}/_next/data/kxhLvQLxR36HnrpiGFM2b/en-nl/search.json?sorting=relevance&keywords={self.search_query}"
        response = requests.get(xhr_url)

        if response.status_code == 200:
            # Save the JSON response to a local file
            with open(f"{self.folder}/{self.search_query}_data.json", 'w', encoding='utf-8') as json_file:
                json.dump(response.json(), json_file,
                          indent=4, ensure_ascii=False)

            # Parse the JSON response
            product_data = response.json()

            # Extract and save product information
            for product in product_data.get('items', []):
                product_name = product.get('productName', 'Unknown')

                if self.is_valid_product(product_name):
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
    search_query = "AKT2"

    scraper = ProductScraper(folder_to_save_data, base_url, search_query)
    scraper.scrape_products()
