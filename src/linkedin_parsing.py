from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, timezone
import json

'''
Below is the function for parsing the HTML sources of the scraped LinkedIn pages.
The function takes a folder path as input and iterates over the JSON files in the folder.
From the HTML in each file the post, post title, and upload date and time are extracted.
Together with the URL and the extraction date and time, all data and metadata are output
as separate JSON files. The original file number is maintained.
'''

def parse_linkedin_content (html_folder):
    
    counter = 0

    for file in html_folder.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            doc = json.load(f)
            
        for url, content in doc.items():
            soup = BeautifulSoup(content, 'html.parser')
            
            data = None

            for script in soup.select('script[type="application/ld+json"]'):
                try:
                    candidate = json.loads(script.string)
                except Exception:
                    continue

                if candidate.get("@type") == "SocialMediaPosting":
                    data = candidate
                    break

            if not data:
                continue

            date_c = (
                datetime.now(timezone.utc)
                .isoformat(timespec="milliseconds")
                .replace("+00:00", "Z")
            )

            linkedin_data = {
                "url": url,
                "title": data.get("headline") if data.get("headline") else None,
                "post": data.get("articleBody"),
                "date posted": data.get("datePublished"),
                "date extracted": date_c,
                "timezone": "UTC"
            }
            
            file_name = file.stem.replace("html", "post")
            out = Path(__file__).parent.parent / "data" / "post_json" / "linkedin_json" / f"{file_name}.json"
            
            with open(out, "w", encoding="utf-8") as f:
                json.dump(linkedin_data, f, ensure_ascii=False, indent=4)
                counter = counter + 1
    print(f"Total number of posts and metadata extracted: {counter}")

linkedin_html = Path(__file__).parent.parent / "data" / "html_json" / "linkedin_html"
parsed_results = parse_linkedin_content(linkedin_html)