import requests
from bs4 import BeautifulSoup

url = 'https://www.amazon.in/s?k=phone'

headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    "User-Agent1": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}


def get_page():
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    return response

def fetch_products(soup):
    products = {}
    results = soup.find_all('div', {'data-component-type': 's-search-result'})

    for item in results:
        title_tag = item.find('h2', class_='a-size-medium')
        price_tag = item.find('span', class_='a-price-whole')

        if title_tag and price_tag:
            title_span = title_tag.find('span')
            title = title_span.text.strip() if title_span else title_tag.text.strip()
            price = price_tag.text.strip().replace(',', '')
            products[title] = f"₹{price}"

    return products

page = get_page()
soup = BeautifulSoup(page.content, 'html.parser')
products = fetch_products(soup)

for title, price in products.items():
    print(f"{title} : {price}\n" )
