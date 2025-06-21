import json
import asyncio
import schedule
import time
from datetime import datetime
from scrapers.patagonia import parse

async def check_prices():
    with open("config.json", "r") as f:
        products = json.load(f)

    for product in products:
        print(f"--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        print(f"Checking product: {product['url']}")
        try:
            price, available = await parse(product['color'], product['size'])
            print(f"Name: {product.get('name', 'Unknown product')}")
            print(f"Color: {product['color']}, Size: {product['size']}")
            print(f"Price: {price} €, Available: {available}")

            if price <= product['target_price'] and available:
                print(f"!!! Price dropped below target: {price} € for {product['color']} size {product['size']} !!!")
        except Exception as e:
            print(f"Error checking product: {e}")

def job():
    asyncio.run(check_prices())

if __name__ == "__main__":
    # Run immediately once on startup
    job()

    # Schedule: run every hour
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)