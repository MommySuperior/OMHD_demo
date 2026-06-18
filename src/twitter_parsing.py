from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, timezone
import json

'''
Below is the function for parsing the HTML sources of the scraped X/Twitter pages.
The function takes a folder path as input and iterates over the JSON files in the folder.
From the HTML in each file the post and upload date and time are extracted.
Together with the URL and the extraction date and time, all data and metadata are output
as separate JSON files. The original file number is maintained.
'''

def parse_twitter_content (html_folder): 

    counter = 0
    
    for file in html_folder.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            doc = json.load(f)
            
        for url, content in doc.items():
            soup = BeautifulSoup(content, 'html.parser')
            post = None 
            date_p = None 

            article = soup.find("article")

            if article:
                div = article.find("div", attrs={"dir": "auto"})

                if div:
                    post = div.get_text("\n", strip=True)

            # Extract publication date from JSON-LD
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string)

                    if data.get("@type") == "SocialMediaPosting":
                        date_p = data.get("datePublished")
                        break

                except Exception:
                    continue

            if not post:
                continue
            
            date_c = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
            
            twitter_data = {
                "url" : url,
                "title" : None,
                "post" : post.strip() if post else None,
                "date posted" : date_p,
                "date extracted" : date_c,
                "timezone": "UTC"
                }
            
            file_name = file.stem.replace("html", "post")
            out = Path(__file__).parent.parent / "data" / "post_json" / "twitter_json" / f"{file_name}.json"
            
            with open(out, "w", encoding="utf-8") as f:
                json.dump(twitter_data, f, ensure_ascii=False, indent=4)
                counter = counter + 1
    print(f"Total number of posts and metadata extracted: {counter}")

twitter_html = Path(__file__).parent.parent / "data" / "html_json" / "twitter_html"
parsed_results = parse_twitter_content(twitter_html) 