from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the base URL and search query
base_url = "https://www.origene.com"
search_query = "AKT3"

# Initialize a Selenium webdriver (make sure to download and configure the Chrome webdriver)
driver = webdriver.Chrome()

# Navigate to the search URL
search_url = f"{base_url}/search?category=Antibodies&q={search_query}"
driver.get(search_url)

# Wait for the product links to be present (adjust the timeout as needed)
wait = WebDriverWait(driver, 10)
product_links = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "name")))

# Extract product names and URLs using JavaScript execution
products = []
for link in product_links:
    product_name = driver.execute_script(
        "return arguments[0].textContent;", link)
    product_url = link.get_attribute("href")
    products.append({"name": product_name.strip(), "url": product_url})

# Print the scraped product names and URLs
for product in products:
    print(f"Product Name: {product['name']}")
    print(f"Product URL: {product['url']}")

# Close the Selenium webdriver
driver.quit()
