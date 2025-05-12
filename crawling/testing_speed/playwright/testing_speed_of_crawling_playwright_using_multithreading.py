import pandas as pd
import time
import asyncio
from playwright.async_api import async_playwright
from concurrent.futures import ThreadPoolExecutor

df = pd.read_excel("../company.xlsx")
urls = df['url'].dropna().tolist()

urls = urls[:10]

results = []
success_count = 0
lock = asyncio.Lock()

# Split list into chunks for each thread
def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

async def crawl_url(page, url):
    global success_count
    start = time.time()
    try:
        response = await page.goto(url, timeout=30000)
        status_code = response.status if response else 0
        status = "success" if status_code == 200 else f"HTTP {status_code}"
        async with lock:
            if status_code == 200:
                success_count += 1
    except Exception as e:
        status = f"error: {repr(e)}"
    duration = time.time() - start
    async with lock:
        results.append((url, duration, status))
    print(f"{url} -> {status} in {duration:.2f}s")

async def thread_worker(thread_id, thread_urls):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for url in thread_urls:
            page = await browser.new_page()
            await crawl_url(page, url)
            await page.close()
        await browser.close()

def run_thread(thread_id, thread_urls):
    asyncio.run(thread_worker(thread_id, thread_urls))

def main():
    start_all = time.time()

    num_threads = 4  # adjust depending on your CPU/network
    url_chunks = chunkify(urls, num_threads)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(run_thread, i, chunk) for i, chunk in enumerate(url_chunks)]
        for future in futures:
            future.result()  # wait for all threads to finish

    total_time = time.time() - start_all
    print(f"\nCrawled {len(urls)} URLs in {total_time:.2f} seconds")
    print(f"Successfully crawled {success_count} with status 200")

    # pd.DataFrame(results, columns=["URL", "TimeTaken", "Status"]).to_csv("playwright_threaded.csv", index=False)

if __name__ == "__main__":
    main()


# Multithreading in Python + Async Code: A Mismatch
# Playwright is Fully Async
# Playwright is designed to maximize I/O-bound concurrency using asyncio.
# You can run many browser tasks in parallel using asyncio.gather efficiently with one browser.

# 🧵 Threads Don’t Help Async I/O
# Python threads don't speed up I/O-bound async code. In fact, they can interfere with the event loop.
# When you create one event loop per thread, each thread becomes isolated, reducing async efficiency.

# 📉 Per-Thread Overhead
# Each thread runs a new browser context, new pages, and its own event loop:
# More memory
# More startup time
# More I/O contention

# ⚖️ Context Switching Overhead
# Threads introduce context switching overhead in Python.
# But since Playwright’s async API is already optimized for async concurrency, threads just add noise