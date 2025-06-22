from notifier import send_email
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
        print(f"\033[97m--- {now} ---\033[0m")  # White timestamp
        logging.info(f"--- {now} ---")

        print(f"\033[90mChecking product: {product['url']}\033[0m")
        logging.info(f"Checking product: {product['url']}")

        try:
            price, available = await parse(product['url'], product['color'], product['size'])
            
            print(f"\033[95mName: {product.get('name', 'Unknown product')}\033[0m")  # Purple name
            print(f"\033[97mColor: {product['color']}\033[0m")  # White
            print(f"\033[97mSize: {product['size']}\033[0m")    # White
            print(f"Price: {price} €")
            print(f"Available: {available}")

            # ✅ SEND EMAIL ONLY IF PRICE <= TARGET AND AVAILABLE
            if price <= product['target_price'] and available:
                print(f"\033[92m!!! Sending email: Price below target and available! \033[0m")
                subject = f"PRICE ALERT: {product.get('name')} now at {price}€"
                body = (
                    f"Product: {product.get('name')}\n"
                    f"URL: {product['url']}\n"
                    f"Color: {product['color']}\n"
                    f"Size: {product['size']}\n"
                    f"Price: {price} €\n"
                    f"Target price: {product['target_price']} €\n"
                    f"Available: {available}"
                )
                send_email(subject, body)

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