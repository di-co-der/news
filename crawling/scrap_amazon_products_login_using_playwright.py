import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

EMAIL = "raghavdivyansh9@gmail.com"
PASSWORD = "Hetro158@"
login_url = (
    "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        #requests and responses
        async def log_request(request):
            print(f"\n>> REQUEST {request.method} {request.url}")
            for key, value in request.headers.items():
                print(f"  {key}: {value}")

        async def log_response(response):
            print(f"\n<< RESPONSE {response.status} {response.url}")
            for key, value in response.headers.items():
                print(f"  {key}: {value}")

        context.on("request", log_request)
        context.on("response", log_response)

        page = await context.new_page()

        await page.goto(login_url)

        # step1:
        await page.wait_for_selector('input[name="email"]')
        await page.fill('input[name="email"]', EMAIL)
        await page.click('span#continue input[type="submit"]')

        # Step 2:
        await page.wait_for_selector('input[name="password"]', timeout=5000)
        await page.fill('input[name="password"]', PASSWORD)
        await page.press('input[name="password"]', 'Enter')

        # Step 3:
        await page.wait_for_timeout(6000)

        # Step 4: Navigate to product page
        product_url = "https://www.amazon.in/s?k=phone"
        await page.goto(product_url)
        await page.wait_for_timeout(5000)

        # Step 5: Get HTML and parse
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')

        # Step 6: Extract sample product data (may vary based on actual HTML)
        product_dict = {}
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            title_tag = item.find('h2', class_='a-size-medium')
            price_tag = item.find('span', class_='a-price-whole')

            if title_tag and price_tag:
                title_span = title_tag.find('span')
                title = title_span.text.strip() if title_span else title_tag.text.strip()
                price = price_tag.text.strip().replace(',', '')
                product_dict[title] = f"₹{price}"

        for title, price in product_dict.items():
            print(f"{title} : {price}\n")

        await browser.close()

asyncio.run(run())