from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def parse(_, desired_color, desired_size):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service("/opt/homebrew/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://eu.patagonia.com/de/de/product/mens-better-sweater-fleece-jacket/191743874994.html"
    driver.get(url)

    try:
        # Wait up to 15 seconds for price to appear
        wait = WebDriverWait(driver, 15)

        # Try to handle cookie popup
        try:
            cookie_button = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()
            print("Accepted cookies")
            time.sleep(1)  # give time to refresh after accepting cookies
        except Exception as e:
            print("No cookie popup found")

        # Wait for price element to load
        price_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.value[itemprop='price']"))
        )
        price_text = price_element.text.strip().replace('€', '').replace(',', '.')
        price = float(price_text)

        # Check color and size availability (simplified)
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


# For quick test:
if __name__ == "__main__":
    parse(None, "stonewash", "M")