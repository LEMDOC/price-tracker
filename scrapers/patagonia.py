import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def parse(_, desired_color, desired_size):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")  # optional, you can even try without headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)

    url = "https://eu.patagonia.com/de/de/product/mens-better-sweater-fleece-jacket/191743874994.html"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 20)

        # Try to handle cookie popup
        try:
            cookie_button = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()
            print("Accepted cookies")
            time.sleep(1)
        except Exception:
            print("No cookie popup found")

        # Wait for price element
        price_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.value[itemprop='price']"))
        )

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