import json
import asyncio
import schedule
import time
from datetime import datetime
import logging
from scrapers.patagonia import parse

# Configure logging
logging.basicConfig(
    filename="price_tracker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def check_prices():
    with open("config.json", "r") as f:
        products = json.load(f)

    for product in products:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\033[93m--- {now} ---\033[0m")  # Yellow timestamp
        logging.info(f"--- {now} ---")
        print(f"Checking product: {product['url']}")
        logging.info(f"Checking product: {product['url']}")

        try:
            price, available = await parse(product['url'], product['color'], product['size'])
            print(f"\033[94mName: {product.get('name', 'Unknown product')}\033[0m")  # Blue product name
            print(f"Color: {product['color']}, Size: {product['size']}")
            print(f"\033[92mPrice: {price} €, Available: {available}\033[0m")  # Green price

            logging.info(f"Name: {product.get('name', 'Unknown product')}")
            logging.info(f"Color: {product['color']}, Size: {product['size']}")
            logging.info(f"Price: {price} €, Available: {available}")

            if price <= product['target_price'] and available:
                print(f"\033[91m!!! Price dropped below target: {price} € for {product['color']} size {product['size']} !!!\033[0m")  # Red alert
                logging.info(f"!!! Price dropped below target: {price} € for {product['color']} size {product['size']} !!!")
        except Exception as e:
            print(f"\033[91mError checking product: {e}\033[0m")
            logging.error(f"Error checking product: {e}")

def job():
    asyncio.run(check_prices())

if __name__ == "__main__":
    job()
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(60)