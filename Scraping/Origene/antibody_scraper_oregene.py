import requests
import re
from bs4 import BeautifulSoup

# Define the base URL and search query
base_url = "https://www.origene.com"
search_query = "AKT3"

# Create a session to handle cookies (optional)
session = requests.Session()

# Set the User-Agent header (optional)
headers = {
    "User-Agent": "Your_User_Agent_String_Here"
}

# Perform a search for "AKT3"
search_url = f"{base_url}/search?category=Antibodies&q={search_query}"

try:
    response = session.get(search_url, headers=headers)
    response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all product links with class "name"
    product_links = soup.find_all("a", class_="name")

    # Initialize a list to store product information
    products_info = []

    for link in product_links:
        product_name = link.text.strip()
        product_url = base_url + link["href"]

        # Visit the product page and scrape additional information
        product_response = session.get(product_url, headers=headers)
        product_soup = BeautifulSoup(product_response.text, "html.parser")

        # Extract CAT# using regex
        cat_match = re.search(
            r'<h2 class="sku mt-0">CAT#: (.+?)</h2>', str(product_soup))
        cat_num = cat_match.group(1) if cat_match else 'N/A'

        # Extract long description using regex
        description_match = re.search(
            r'<p class="long-description mt-3">(.+?)</p>', str(product_soup))
        product_description = description_match.group(
            1).strip() if description_match else 'N/A'

        # Extract available and sold-out sizes using regex
        size_match = re.findall(
            r'(<a class="btn btn-sm btn-product-options" href=".+?">(.+?)</a>)|(<span class="btn btn-sm btn-product-options disabled">(.+?)</span>)', str(product_soup))

        available_sizes = [s[1] for s in size_match if s[1]]
        sold_out_sizes = [s[3] for s in size_match if s[3]]

        # Create a dictionary to store all information for this product
        product_info = {
            "name": product_name,
            "url": product_url,
            "cat_num": cat_num,
            "description": product_description,
            "available_sizes": available_sizes,
            "sold_out_sizes": sold_out_sizes
        }

        # Append the product information to the list
        products_info.append(product_info)

    # Print or process the scraped product information
    for product in products_info:
        print(f"Product Name: {product['name']}")
        print(f"Product URL: {product['url']}")
        print(f"CAT#: {product['cat_num']}")
        print(f"Product Description: {product['description']}")
        print(
            f"Available Sizes: {', '.join(product['available_sizes']) if product['available_sizes'] else 'N/A'}")
        print(
            f"Sold Out Sizes: {', '.join(product['sold_out_sizes']) if product['sold_out_sizes'] else 'N/A'}")
        print("-----")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while making the request: {e}")

except Exception as e:
    print(f"An error occurred: {e}")
