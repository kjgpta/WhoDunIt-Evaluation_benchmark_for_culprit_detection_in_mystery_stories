import os
import json
import glob
import pandas as pd
from tqdm import tqdm

# Paths
META_FOLDER = "./meta"
BOOKS_FOLDER = "./books"
output_folder = "dataset"

OUTPUT_JSONL = os.path.join(output_folder,"./augmented_data.jsonl")
OUTPUT_EXCEL = os.path.join(output_folder,"./augmented.xlsx")

# Load metadata files
with open(os.path.join(META_FOLDER, "all_stories.json"), "r") as f:
    all_stories = json.load(f)
with open(os.path.join(META_FOLDER, "all_authors.json"), "r") as f:
    all_authors = json.load(f)
with open(os.path.join(META_FOLDER, "all_Story_pages.json"), "r") as f:
    all_story_pages = json.load(f)
with open(os.path.join(META_FOLDER, "killer.json"), "r") as f:
    killer = json.load(f)
with open(os.path.join(META_FOLDER, "killers_ss.json"), "r") as f:
    ss_killer = json.load(f)

# Merge killer and ss_killer
merged_killer = {**killer, **ss_killer}

# Augmentations
AUGMENTATIONS = ["all", "hp", "hollywood", "bollywood"]

# Function to replace names in the killers with augmented names
def replace_killer_names(killer_list, augmentation, alias):
    with open(os.path.join("books", alias, f"name_{augmentation}_complete.json"), "r") as f:
        name_map = json.load(f)
    normalized_name_map = {key.lower(): value for key, value in name_map.items()}
    
    # Replace words in killer names using the normalized name map
    augmented_killers = []
    for phrase in killer_list:
        # Split the killer name into words and replace each word using the normalized name map
        words = phrase.split()
        new_killer = " ".join(normalized_name_map.get(word.lower(), word) for word in words)
        
        # Convert the new name to lowercase for consistency
        augmented_killers.append(new_killer.lower())
    
    return augmented_killers, normalized_name_map

# Read all data and create the dataset
dataset = []

for alias, book_title in tqdm(all_stories.items()):
    author = all_authors.get(alias, "Unknown Author")
    length = all_story_pages.get(alias)
    if isinstance(length, dict):
        length = length.get("length", "Unknown Length")
    else:
        length = str(length)  # Convert non-dictionary length to string
    
    # Read the story text
    story_text = ""
    story_folder = os.path.join(BOOKS_FOLDER, alias)
    

    # Get original killer info
    original_killers = merged_killer.get(alias, [])
    
    # Process each augmentation
    for augmentation in AUGMENTATIONS:
        page_path = os.path.join(story_folder, f"complete_{augmentation}")
        if os.path.exists(page_path):
            with open(page_path, "r", encoding="utf-8") as f:
                story_text = f.read()
        
        if story_text == "":
            print(f"Story text not found for {book_title} ({alias}) with augmentation {augmentation}. Skipping...")
            continue  # Skip stories with no content

        augmented_killers, name_map = replace_killer_names(original_killers, augmentation, alias)
        
        # Create metadata
        if augmentation == "hp":
            entity_replacement_style = "Harry Potter"
        elif augmentation == "all":
            entity_replacement_style = "All Characters"
        else:
            entity_replacement_style = augmentation
        
        metadata = {
            "entity_replacement_style": f"REPLACE_{entity_replacement_style.upper()}",
            "name_id_map": name_map,
        }
        
        # Add to dataset
        dataset.append({
            "title": book_title,
            "author": author,
            "length": length,  
            "culprit_ids": augmented_killers,
            "text": story_text,
            "metadata": metadata,
        })

# Save as JSONL
with open(OUTPUT_JSONL, "w") as f:
    for entry in dataset:
        f.write(json.dumps(entry) + "\n")

# Save as Excel
df = pd.DataFrame(dataset)
df.to_excel(OUTPUT_EXCEL, index=False)

print(f"Dataset created with {len(dataset)} entries.")
