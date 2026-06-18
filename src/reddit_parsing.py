from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, timezone
import json

'''
Below is the function for parsing the HTML sources of the scraped Reddit pages.
The function takes a folder path as input and iterates over the JSON files in the folder.
From the HTML in each file the post, post title, and upload date and time are extracted.
Together with the URL and the extraction date and time, all data and metadata are output
as separate JSON files. The original file number is maintained.
'''

def parse_reddit_content (html_folder):

    counter = 0
    
    for file in html_folder.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            doc = json.load(f)
            
        for url, content in doc.items():
            soup = BeautifulSoup(content, 'html.parser')
            header = soup.find("h1")
            
            post_container = soup.find("shreddit-post-text-body")
            post = None
            
            if post_container:
                post = post_container.find("div", {"slot": "text-body"})
            if not post:
                continue
            
            post_element = soup.find("shreddit-post")
            time_tag = post_element.find("time") if post_element else None
            
            date_p = time_tag.get("datetime") if time_tag and time_tag.has_attr("datetime") else None
            
            date_c = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
            
            reddit_data = {
                "url" : url,
                "title" : header.get_text(strip=True) if header else None,
                "post" : post.get_text("\n", strip=True) if post else None,
                "date posted" : date_p,
                "date extracted" : date_c,
                "timezone": "UTC"
                }
            
            file_name = file.stem.replace("html", "post")
            out = Path(__file__).parent.parent / "data" / "post_json" / "reddit_json" / f"{file_name}.json" # the output path to which the new JSON files are written
            
            with open(out, "w", encoding="utf-8") as f:
                json.dump(reddit_data, f, ensure_ascii=False, indent=4)
                counter = counter + 1
    print(f"Total number of posts and metadata extracted: {counter}")

reddit_html = Path(__file__).parent.parent / "data" / "html_json" / "reddit_html" # the input path to the folder with JSON files containing the HTML sources
parsed_results = parse_reddit_content(reddit_html)
