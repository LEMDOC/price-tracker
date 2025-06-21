from bs4 import BeautifulSoup

def parse(response, desired_color, desired_size):
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())

    # Get price element
    price_element = soup.find('span', class_='product-prices__price')
    if not price_element:
        print("Price not found.")
        return None, False

    price_text = price_element.get_text().strip()

    # Remove euro sign and comma, convert to float
    price_text_clean = price_text.replace('€', '').replace(',', '.').strip()
    try:
        price = float(price_text_clean)
    except:
        print("Price parse error.")
        return None, False

    # Simple check for color/size (approximation)
    page_text = soup.get_text().lower()
    color_available = desired_color.lower() in page_text
    size_available = desired_size.lower() in page_text

    available = color_available and size_available

    return price, available