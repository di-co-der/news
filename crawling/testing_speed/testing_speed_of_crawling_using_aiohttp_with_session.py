import time
import aiohttp
import asyncio
import pandas as pd


def clean_url(raw_url):
    url = raw_url.strip()
    # Remove invalid patterns
    if "#~dup~" in url:
        return None
    # Ensure scheme
    if not url.startswith("http"):
        url = "https://" + url
    return url

df = pd.read_excel("company.xlsx")
urls = df['url'].dropna().map(clean_url).dropna().tolist()

results = []
count = 0

async def fetch(session, url):
    global count
    start = time.time()
    try:
        async with session.get(url, timeout = aiohttp.ClientTimeout(total=35, connect=20, sock_connect=5, sock_read=10)) as response:
            await response.text()  # actually read the response
            status = "success"
            if(response.status == 200):
                count = count + 1
    except Exception as e:
        status = f"error: {repr(e)}"
    duration = time.time() - start
    results.append((url, duration, status))
    print(f"{url} -> {status} in {duration:.2f}s")

async def main():
    start_all = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        await asyncio.gather(*tasks)
    total_time = time.time() - start_all
    print(f"\nCrawled {len(urls)} URLs in {total_time:.2f} seconds")
    print(f"successful crawled {count}")

    # Optional: Save results
    pd.DataFrame(results, columns=["URL", "TimeTaken", "Status"]).to_csv("aiohttp_results.csv", index=False)

# Entry point
asyncio.run(main())


