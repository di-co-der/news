import time
import aiohttp
import asyncio
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def clean_url(raw_url):
    url = raw_url.strip()
    if "#~dup~" in url:
        return None
    if not url.startswith("http"):
        url = "https://" + url
    return url

df = pd.read_excel("../company.xlsx")
urls = df['url'].dropna().map(clean_url).dropna().tolist()

def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

async def fetch(session, url, results, count):
    start = time.time()
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=35)) as response:
            await response.text()
            status = "success"
            if response.status == 200:
                count[0] += 1
    except Exception as e:
        status = f"error: {repr(e)}"
    duration = time.time() - start
    results.append((url, duration, status))
    print(f"{url} -> {status} in {duration:.2f}s")

async def crawl_urls(chunk, results, count):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, results, count) for url in chunk]
        await asyncio.gather(*tasks)

def run_thread(chunk, results, count):
    asyncio.run(crawl_urls(chunk, results, count))

def main():
    start_all = time.time()
    num_threads = 4

    url_chunks = chunkify(urls, num_threads)
    results = []
    count = [0]  # Mutable for threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(run_thread, chunk, results, count) for chunk in url_chunks]
        for f in futures:
            f.result()

    total_time = time.time() - start_all
    print(f"\nCrawled {len(urls)} URLs in {total_time:.2f} seconds")
    print(f"Successful crawled {count[0]}")
    pd.DataFrame(results, columns=["URL", "TimeTaken", "Status"]).to_csv("aiohttp_threaded.csv", index=False)

if __name__ == "__main__":
    main()
