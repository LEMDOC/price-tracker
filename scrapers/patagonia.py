import asyncio
from playwright.async_api import async_playwright

async def parse(url, desired_color, desired_size):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url)

        try:
            await page.wait_for_selector("#onetrust-accept-btn-handler", timeout=5000)
            await page.click("#onetrust-accept-btn-handler")
            print("Accepted cookies")
        except:
            print("No cookie popup found (or appeared too late)")

        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(3)

        await page.wait_for_selector('span.value[itemprop="price"]', timeout=20000, state='attached')
        price_element = await page.query_selector('span.value[itemprop="price"]')
        price_content = await price_element.get_attribute("content")
        price = float(price_content.replace(',', '.'))

        page_text = await page.content()
        color_available = desired_color.lower() in page_text.lower()
        size_available = desired_size.lower() in page_text.lower()
        available = color_available and size_available

        print(f"DEBUG: Price {price} €, Available: {available}")
        return price, available

# Only for standalone testing
if __name__ == "__main__":
    test_url = "https://eu.patagonia.com/de/de/product/mens-better-sweater-fleece-jacket/191743874994.html"
    asyncio.run(parse(test_url, "stonewash", "M"))