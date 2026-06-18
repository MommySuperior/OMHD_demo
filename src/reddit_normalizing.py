from pathlib import Path
import json
import os

'''
Below is the function for normalizing the Reddit data.
The function takes JSON files as input and outputs the posts as text files.
A maximum of 220 files is handled to ensure that the number of posts 
per platform is equal for the topic modelling.
'''

reddit_json = Path(__file__).parent.parent / "data" / "post_json" / "reddit_json"
reddit_text = Path(__file__).parent.parent / "data" / "post_txt" / "reddit_txt"

def normalize_reddit_posts(folder_path):

    converted = 0
    maximum = 220

    for file in os.listdir(folder_path):

        if converted >= maximum:
            break

        if file.endswith(".json"):
            json_path = os.path.join(folder_path, file)

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            title = data.get("title") # the post title is extracted from the JSON file and stored in the variable `title`
            post = data.get("post").removesuffix("\nRead more") # the post content is extracted from the JSON file, the last line is removed, and the post is stored in the variable `post`
            full_post = f"{title}\n\n{post}" # the post and post title are merged into one string and stored in the variable `full_post`

            file_name = Path(file).stem
            new_file_name = file_name + ".txt"
            txt_path = os.path.join(reddit_text, new_file_name)

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_post)

            print(f"Converted: {file} -> {new_file_name}")
            converted = converted + 1
    print(f"Total number of files converted: {converted}")

normalize_reddit_posts(reddit_json)