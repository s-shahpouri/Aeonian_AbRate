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
        product_page_html = product_response.text
        product_soup = BeautifulSoup(product_response.text, "html.parser")

        # Extract the necessary fields using regex
        sku_search = re.search(r'CAT#:\s*(\w+)', product_page_html)
        sku = sku_search.group(1) if sku_search else 'N/A'

        long_description_search = re.search(
            r'<p class="long-description mt-3">(.*?)</p>', product_page_html, re.DOTALL)
        long_description = long_description_search.group(
            1).strip() if long_description_search else 'N/A'

        sizes = re.findall(
            r'<a class="btn btn-sm btn-product-options".*?>(.*?)</a>|<span class="btn btn-sm btn-product-options disabled">(.*?)</span>', product_page_html)

        sizes = [size[0] or size[1] for size in sizes]
        formulation = re.findall(
            r'<p class="smaller text-muted mb-1">.*?Formulation:.*?<span class="btn btn-sm btn-product-options.*?">(.*?)</span>', product_page_html, re.DOTALL)

        conjugation = re.findall(
            r'<p class="smaller text-muted mb-1">.*?Conjugation:.*?<span class="btn btn-sm btn-product-options.*?">(.*?)</span>', product_page_html, re.DOTALL)

        special_offer_search = re.search(
            r'<p>\s*<a class="origene-orange".*?>(.*?)</a>\s*</p>', product_page_html, re.DOTALL)
        special_offer = special_offer_search.group(
            1).strip() if special_offer_search else 'N/A'

        product_info = {
            "name": product_name,
            "url": product_url,
            "sku": sku,
            "long_description": long_description,
            "sizes": sizes,
            "formulation": formulation,
            "conjugation": conjugation,
            "special_offer": special_offer
        }

        products_info.append(product_info)

    # Print or process the scraped product information
    for product in products_info:
        print(f"Product Name: {product['name']}")
        print(f"Product URL: {product['url']}")
        print(f"SKU: {product['sku']}")
        print(f"Long Description: {product['long_description']}")
        print(f"Sizes: {', '.join(product['sizes'])}")
        print(f"Formulation: {', '.join(product['formulation'])}")
        print(f"Conjugation: {', '.join(product['conjugation'])}")
        print(f"Special Offer: {product['special_offer']}")
        print("-----")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while making the request: {e}")

except Exception as e:
    print(f"An error occurred: {e}")
