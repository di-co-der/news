import pandas as pd
import time
import asyncio
from multiprocessing import Process, Manager
from playwright.async_api import async_playwright

# Load URLs
df = pd.read_excel("../company.xlsx")
urls = df['url'].dropna().tolist()

urls = urls[:10]

# Split list into chunks
def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

async def crawl_url(page, url, results, success_counter):
    start = time.time()
    try:
        response = await page.goto(url, timeout=30000)
        status_code = response.status if response else 0
        status = "success" if status_code == 200 else f"HTTP {status_code}"
        if status_code == 200:
            success_counter[0] += 1
    except Exception as e:
        status = f"error: {repr(e)}"
    duration = time.time() - start
    results.append((url, duration, status))
    print(f"{url} -> {status} in {duration:.2f}s")

async def worker(urls, results, success_counter):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for url in urls:
            page = await browser.new_page()
            await crawl_url(page, url, results, success_counter)
            await page.close()
        await browser.close()

def run_process(urls, results, success_counter):
    asyncio.run(worker(urls, results, success_counter))

def main():
    start_all = time.time()
    num_processes = 4  # You can adjust based on your CPU
    url_chunks = chunkify(urls, num_processes)

    with Manager() as manager:
        results = manager.list()
        success_counter = manager.list([0])  # list so it's mutable

        processes = []
        for chunk in url_chunks:
            p = Process(target=run_process, args=(chunk, results, success_counter))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        # Convert results back to DataFrame
        # pd.DataFrame(results, columns=["URL", "TimeTaken", "Status"]).to_csv("playwright_multiprocess.csv", index=False)

        total_time = time.time() - start_all
        print(f"\nCrawled {len(urls)} URLs in {total_time:.2f} seconds")
        print(f"Successfully crawled {success_counter[0]} with status 200")

if __name__ == "__main__":
    main()
