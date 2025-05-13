import pandas as pd
import asyncio
import time

from openai import responses
from playwright.async_api import async_playwright

df = pd.read_excel("../company.xlsx")
urls = df['url'].dropna().tolist()

urls = urls[:10]

count = 0
results = []

async def crawl_url(page, url):
    global count
    start = time.time()
    try:
        response = await page.goto(url)  # timeout
        # Optional: wait for content or take action
        # await page.wait_for_selector('body')
        status = "success"
        if (response and response.status == 200):
            count = count + 1
    except Exception as e:
        status = f"error: {e}"
    duration = time.time() - start
    results.append((url, duration, status))
    print(f"{url} -> {status} in {duration:.2f}s")

async def run():
    start_all = time.time()
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for url in urls:
            await crawl_url(page, url)

        await browser.close()

    total_time = time.time() - start_all
    print(f"\nCrawled {len(urls)} URLs in {total_time:.2f} seconds")
    print(f"successful crawled {count}")

asyncio.run(run())


