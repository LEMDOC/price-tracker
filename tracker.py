import requests
import json
import time
import schedule
from notifier import send_email
import scrapers.patagonia as patagonia

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}

scraper_map = {
    'patagonia': patagonia
}

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def check_product(product):
    url = product['url']
    site = product['site']
    target_price = product['target_price']
    color = product['color']
    size = product['size']

    print(f"Checking: {url}")

    try:
        response = requests.get(url, headers=HEADERS)
    except Exception as e:
        print(f"Request failed: {e}")
        return

    if site not in scraper_map:
        print(f"No scraper for site: {site}")
        return

    price, available = scraper_map[site].parse(response, color, size)

    if price is None:
        return

    print(f"Price: {price} € | Available: {available}")

    if price <= target_price and available:
        subject = f"SALE: {site.title()} - {color} size {size} at {price} €"
        body = f"{url}\nTarget price: {target_price} €\nCurrent price: {price} €"
        send_email(subject, body)

def job():
    print(f"\n--- Checking products --- {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    products = load_config()
    for product in products:
        check_product(product)

schedule.every().hour.do(job)

print("Price Tracker started. Checking every hour...")
job()  # First immediate run

while True:
    schedule.run_pending()
    time.sleep(60)