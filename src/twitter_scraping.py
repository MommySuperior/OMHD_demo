from playwright.sync_api import sync_playwright
from pathlib import Path
import time
import random
import json

'''
(introduction)
'''

twitter_urls = Path(__file__).parent.parent / "data" / "urls_txt" / "twitter_urls.txt" # the path to the text document with URLs to X posts is stored in the variable `twitter_urls`

with open(twitter_urls, "r", encoding="utf-8") as f: # twitter_urls.txt is opened for reading 
    urls = [line.strip() for line in f if line.strip()] # the URLs are stripped and coverted to list items 
    urls = list(dict.fromkeys(urls)) # the URLs are deduplicted and put into a list 

print(len(urls), "URLs stored in total") # prints the total number of URLs in the text document
print(f"First 10 URLs: {urls[:10]}") # prints the first 10 URLs in the text document

def scrape_web_content(urls): # a function that takes a list of URLs as input
    d = 0 # a counter for counting the number of successfully scraped webpages
    with sync_playwright() as p: 
        browser = p.chromium.launch( 
            headless=False # enables a headed browser session to lower the risk of detection by anti-bot systems
        ) 

        context = browser.new_context( # the new_context() method creates an isolated browser session inside the browser 
            user_agent=( 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            ) # a custom user agent is set to mimick requests by a real user
        )

        page = context.new_page() # a browser tab is opened using the .new_page() method

        for i, url in enumerate(urls): # a for-loop to iterate over the URLs and assign a number to each URL
            try: # a try block to prevent the loop from crashing 
                page.goto( # the .goto() method navigates to the webpage corresponding to the URL 
                    url, # the URL that the .goto() method navigates to
                    wait_until="networkidle", # a safeguard to wait with scraping until all network activity has ceased 
                    timeout=60000 # ensures the scraper breaks off after 60 seconds so it will not get stuck when a webpage doesn't properly load
                )

                html = page.content()
                out = Path(__file__).parent.parent / "data" / "html_json" / "twitter_html" / f"twitter_html_{i}.json" # the output path ...
                
                with open(out, "w", encoding="utf-8") as f:
                    json.dump({url: html}, f, ensure_ascii=False)

                print(f"SUCCESS: {url}") # prints the URL of every webpage that has been successfully scraped
                d = d + 1 # ...
                time.sleep(random.uniform(2, 4)) # execution is paused randomly for 2 or 4 seconds

            except Exception as e: 
                print(f"ERROR: {url}") 
                print(e) 

        browser.close() 
    
    return d # returns the number of webpages successfully scraped

scraped_results = scrape_web_content(urls) 

print(f"\nNumber of pages scraped: {scraped_results}") # prints the number of webpages successfully scraped