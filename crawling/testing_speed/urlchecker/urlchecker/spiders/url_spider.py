import scrapy
import pandas as pd
import time
from collections import Counter

class UrlSpider(scrapy.Spider):
    name = "url_spider"

    def start_requests(self):
        df = pd.read_excel("../company.xlsx")

        def clean_url(raw_url):
            url = raw_url.strip()
            if "#~dup~" in url:
                return None
            if not url.startswith("http"):
                url = "https://" + url
            return url

        urls = df['url'].dropna().map(clean_url).dropna().tolist()
        # urls = urls[:10]

        self.start_time = time.time()
        self.success_count = 0
        self.results = []
        self.status_counter = Counter()

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.errback_general,
                meta={'start': time.time(), 'url': url},
                dont_filter=True
            )

    def parse(self, response):
        duration = time.time() - response.meta['start']
        url = response.meta['url']
        if response.status == 200:
            self.success_count += 1
            status = "success"
        else:
            status = f"HTTP {response.status}"

        self.status_counter[str(response.status)] += 1
        self.results.append((url, duration, status))
        self.log(f"{url} -> {status} in {duration:.2f}s")

    def errback_general(self, failure):
        request = failure.request
        url = request.meta['url']
        duration = time.time() - request.meta['start']

        if failure.check(scrapy.spidermiddlewares.httperror.HttpError):
            response = failure.value.response
            status_code = response.status
            status = f"HTTP {status_code}"
            self.status_counter[str(status_code)] += 1
        else:
            status = f"error: {repr(failure.value)}"
            self.status_counter["other_error"] += 1

        self.results.append((url, duration, status))
        self.log(f"{url} -> {status} in {duration:.2f}s")

    def closed(self, reason):
        total_time = time.time() - self.start_time
        self.log(f"\nCrawled {len(self.results)} URLs in {total_time:.2f} seconds")
        self.log(f"Successfully crawled {self.success_count} URLs")

        self.log("HTTP Status Summary:")
        for code, count in self.status_counter.items():
            self.log(f"  {code}: {count} URLs")

        # Save to CSV
        df = pd.DataFrame(self.results, columns=["URL", "TimeTaken", "Status"])
        df.to_csv("scrapy_results.csv", index=False)