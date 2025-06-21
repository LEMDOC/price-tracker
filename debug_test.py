import requests
from bs4 import BeautifulSoup

# Use your product URL here
url = "https://eu.patagonia.com/de/de/product/mens-better-sweater-fleece-jacket/191743874994.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')

# Print out full HTML content to debug
print(soup.prettify())