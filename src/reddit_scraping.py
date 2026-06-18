from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import random
import json

'''
Below is the function for scraping the Reddit pages, which takes a text file as input. 
The function uses a headed browser session and iterates over the URLs to scrape the HTML source of each page.
The URLs and corresponding HTML sources are stored as key-value pairs in JSON files.
'''
reddit_urls = Path(__file__).parent.parent / "data" / "urls_txt" / "reddit_urls.txt"

with open(reddit_urls, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]
    urls = list(dict.fromkeys(urls))

print(len(urls), "URLs stored in total")
print(f"First 10 URLs: {urls[:10]}")

def scrape_web_content(urls):
    d = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        )

        page = context.new_page()

# If the scraper crashes out due to too many requests (429), 
# change n to the number of the last file it scraped +1
# so if the last file was reddit_html_137, change n to 138

        n = 0
        for i, url in enumerate(urls[n:], start=n):
            try:
                page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=60000
                )

                html = page.content()
                out = Path(__file__).parent.parent / "data" / "html_json" / "reddit_html" / f"reddit_html_{i}.json"
                
                with open(out, "w", encoding="utf-8") as f:
                    json.dump({url: html}, f, ensure_ascii=False)

                print(f"SUCCESS: {url}")
                d = d + 1
                time.sleep(random.uniform(2, 4))

            except Exception as e:
                print(f"ERROR: {url}")
                print(e)

        browser.close()
    
    return d

scraped_results = scrape_web_content(urls)

print(f"\nNumber of pages scraped: {scraped_results}")