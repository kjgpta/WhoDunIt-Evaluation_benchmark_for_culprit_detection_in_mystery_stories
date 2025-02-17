import os
import json
import pandas as pd
from pathlib import Path

# Define paths
meta_folder = "meta"
books_folder = "books"
output_folder = "dataset"
output_jsonl = os.path.join(output_folder, "original_data.jsonl")
output_excel = os.path.join(output_folder, "original.xlsx")
# Load JSON files
with open(os.path.join(meta_folder, "all_stories.json"), "r") as f:
    all_stories = json.load(f)

with open(os.path.join(meta_folder, "all_authors.json"), "r") as f:
    all_authors = json.load(f)

with open(os.path.join(meta_folder, "all_story_pages.json"), "r") as f:
    all_story_pages = json.load(f)

with open(os.path.join(meta_folder, "killer.json"), "r") as f:
    killer = json.load(f)

with open(os.path.join(meta_folder, "killers_ss.json"), "r") as f:
    ss_killer = json.load(f)

# Merge killer.json and ss_killer.json
merged_killers = {**killer, **ss_killer}

# Prepare dataset
dataset = []

# Iterate over all aliases in all_stories
for alias, book_name in all_stories.items():
    book_folder = os.path.join(books_folder, alias)
    text_file_path = os.path.join(book_folder, "complete_original.txt")
    
    # Skip if the text file doesn't exist
    if not os.path.isfile(text_file_path):
        print(f"Text file not found for {book_name} ({alias}). Skipping...")
        continue
    
    # Read text content
    with open(text_file_path, "r", encoding="utf-8") as f:
        text_content = f.read()
    
    # Extract author
    author = all_authors.get(alias, "Unknown Author")
    
    # Extract length
    length = all_story_pages.get(alias)
    if isinstance(length, dict):
        length = length.get("length", "Unknown Length")
    else:
        length = str(length)  # Convert non-dictionary length to string
    # Extract culprit_ids
    culprit_ids = merged_killers.get(alias, [])
    
    # Append to dataset
    dataset.append({
        "title": book_name,
        "author": author,
        "length": length,
        "culprit_ids": culprit_ids,
        "text": text_content
    })

# Save dataset as JSONL
with open(output_jsonl, "w", encoding="utf-8") as f:
    for entry in dataset:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# Save dataset as Excel
df = pd.DataFrame(dataset)
df.to_excel(output_excel, index=False)

print(f"Dataset has been saved as {output_jsonl} and {output_excel}.")
