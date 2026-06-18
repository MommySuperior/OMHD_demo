from pathlib import Path
import json
import os

'''
Below is the function for normalizing the LinkedIn data.
The function takes JSON files as input and outputs the posts as text files.
A maximum of 220 files is handled to ensure that the number of posts 
per platform is equal for the topic modelling.
'''

linkedin_json = Path(__file__).parent.parent / "data" / "post_json" / "linkedin_json"
linkedin_text = Path(__file__).parent.parent / "data" / "post_txt" / "linkedin_txt"

def normalize_linkedin_posts(folder_path):

    converted = 0
    maximum = 220

    for file in os.listdir(folder_path):

        if converted >= maximum:
            break

        if file.endswith(".json"):
            json_path = os.path.join(folder_path, file)

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            post = data.get("post")

            file_name = Path(file).stem
            new_file_name = file_name + ".txt"
            txt_path = os.path.join(linkedin_text, new_file_name)

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(post)

            print(f"Converted: {file} -> {new_file_name}")
            converted = converted + 1
    print(f"Total number of files converted: {converted}")

normalize_linkedin_posts(linkedin_json)