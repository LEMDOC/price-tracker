import json
import asyncio
from scrapers.patagonia import parse

async def check_prices():
    with open("config.json", "r") as f:
        products = json.load(f)

    for product in products:
        print(f"Checking product: {product['url']}")
        try:
            # We pass color and size like your working standalone version
            price, available = await parse(product['color'], product['size'])
            print(f"Price: {price} €, Available: {available}")

            if price <= product['target_price'] and available:
                print(f"!!! Price dropped below target: {price} € for {product['color']} size {product['size']} !!!")
        except Exception as e:
            print(f"Error checking product: {e}")

if __name__ == "__main__":
    asyncio.run(check_prices())