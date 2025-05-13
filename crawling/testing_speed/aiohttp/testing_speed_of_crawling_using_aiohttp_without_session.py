import aiohttp
import asyncio
import pandas as pd
import time

# Load URLs from Excel
df = pd.read_excel("../company.xlsx")
urls = df['url'].dropna().tolist()
# urls = urls[:3000]  # limit for testing

results = []

async def fetch(url):
    start = time.time()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                await response.text()
                status = "success"
    except Exception as e:
        status = f"error: {e}"
    duration = time.time() - start
    results.append((url, duration, status))
    print(f"{url} -> {status} in {duration:.2f}s")

async def main():
    start_all = time.time()
    tasks = [fetch(url) for url in urls]
    await asyncio.gather(*tasks)
    total_time = time.time() - start_all
    print(f"\nCrawled {len(urls)} URLs in {total_time:.2f} seconds")

    # Optional: Save results
    # pd.DataFrame(results, columns=["URL", "TimeTaken", "Status"]).to_csv("aiohttp_results.csv", index=False)

# Entry point
asyncio.run(main())
