from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def parse(_, desired_color, desired_size):
    # Setup headless Chrome browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service("/opt/homebrew/bin/chromedriver")  # <-- Update if your chromedriver is in a different path

    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://eu.patagonia.com/de/de/product/mens-better-sweater-fleece-jacket/191743874994.html"
    driver.get(url)

    # Give JavaScript time to load
    time.sleep(5)

    try:
        price_element = driver.find_element(By.CLASS_NAME, "product-prices__price")
        price_text = price_element.text.strip().replace('€', '').replace(',', '.')
        price = float(price_text)

        page_text = driver.page_source.lower()
        color_available = desired_color.lower() in page_text
        size_available = desired_size.lower() in page_text
        available = color_available and size_available

        print(f"DEBUG: Price {price} €, Available: {available}")
        return price, available

    except Exception as e:
        print("Error extracting price:", e)
        return None, False

    finally:
        driver.quit()

        if __name__ == "__main__":
    parse(None, "stonewash", "M")