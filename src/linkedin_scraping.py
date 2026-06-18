from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import random
import json

linkedin_urls = Path(__file__).parent.parent / "data" / "urls_txt" / "linkedin_urls.txt"

with open(linkedin_urls, "r", encoding="utf-8") as f:
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

        for i, url in enumerate(urls):
            out = Path(__file__).parent.parent / "data" / "html_json" / "linkedin_html" / f"linkedin_html_{i}.json"
            if out.exists():
                continue
            try:
                page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=60000
                )

                html = page.content()
                
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