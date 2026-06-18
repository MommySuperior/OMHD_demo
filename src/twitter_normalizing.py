from pathlib import Path
import json
import os

'''
Below is the function for normalizing the X/Twitter data.
The function takes JSON files as input and outputs the posts as text files.
A maximum of 220 files is handled to ensure that the number of posts 
per platform is equal for the topic modelling.
'''

twitter_json = Path(__file__).parent.parent / "data" / "post_json" / "twitter_json" # the path to the folder with JSON files is stored in the variable `twitter_json`
twitter_text = Path(__file__).parent.parent / "data" / "post_txt" / "twitter_txt" # the path to the output folder is stored in the variable `twitter_text`

def normalize_twitter_posts(folder_path): # a function that takes a folder path as input

    converted = 0 # a counter for counting the number of converted files
    maximum = 220 # the maximum number of files to be converted

    for file in os.listdir(folder_path): # a for-loop to iterate over the files in the folder twitter_json

        if converted >= maximum: # an if-statement to set the condition for when the maximum of 220 files has been reached
            break # the function stops converting files when the condition in the if-statement has been met

        if file.endswith(".json"): # an if-statement to set the condition for when a file ends with the .json extension
            json_path = os.path.join(folder_path, file) 
            
            with open(json_path, "r", encoding="utf-8") as f: 
                data = json.load(f) # the content of the JSON file is stored in the variable `data`

            post = data.get("post") # the post content is extracted from the JSON file and stored in the variable `post`

            file_name = Path(file).stem # the filename of the JSON file is stemmed, meaning the .json extension is removed
            new_file_name = file_name + ".txt" # a .txt extension is added to the filename
            txt_path = os.path.join(twitter_text, new_file_name) 

            with open(txt_path, "w", encoding="utf-8") as f: 
                f.write(post) # the post content is written to a new text file

            print(f"Converted: {file} -> {new_file_name}") # prints the old filename and the new filename
            converted = converted + 1 # 1 is added to the counter for each converted file
    print(f"Total number of files converted: {converted}") # prints the total number of files converted

normalize_twitter_posts(twitter_json) # the folder path is loaded into the function