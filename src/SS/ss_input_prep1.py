import spacy, re, json, os
from util import *  # Ensure util module has required methods like normalize_text, normalize_name, get_text_from_url, clean_gutenberg_text

# Load the Spacy model
nlp = spacy.load("en_core_web_trf")

# Titles to exclude
exclude_titles = {
    "mr", "mrs", "ms", "miss", "mx", "dr", "prof", "sir", "lord", "lady", "madam",
    "madame", "hon", "rev", "fr", "father", "pastor", "minister", "rabbi", "imam", 
    "sheikh", "cardinal", "archbishop", "bishop", "pope", "saint", "brother", "sister",
    "officer", "capt", "captain", "cmdr", "commander", "lt", "lieutenant", "maj", 
    "major", "col", "colonel", "gen", "general", "admiral", "sgt", "sergeant", 
    "cpl", "corporal", "pvt", "private", "chief", "deputy", "detective", "judge",
    "justice", "attorney", "ambassador", "sec", "secretary", "gov", "governor", 
    "sen", "senator", "rep", "representative", "pres", "president", "vp", "vice", 
    "chancellor", "minister", "prime", "premier", "chairman", "chairwoman",
    "duke", "duchess", "earl", "baron", "baroness", "count", "countess", "viscount",
    "marquis", "marchioness", "consul", "envoy", "patriarch", "matriarch", "tsar", 
    "czar", "emperor", "empress", "king", "queen", "prince", "princess", "shah", 
    "raj", "sheikh", "ayatollah", "mullah", "caliph", "imam"
}

def replace_names_spacy(text):
    nlp.max_length = 2000000
    doc = nlp(text)
    name_to_tag = {}
    tag_counter = 1
    dct = {}
    for ent in doc.ents:            
        if ent.label_ == "PERSON" and (ent.text.istitle() or ent.text.isupper()) and ent.root.pos_ == "PROPN" and 2 <= len(ent.text) <= 50 and not nlp.vocab[ent.text.lower()].is_stop:
            cleaned_name = normalize_text(ent.text)
            name_parts = cleaned_name.split()
            first_name = name_parts[0].lower() if name_parts else ""
            
            # Remove title if the first part is in exclude_titles
            if first_name in exclude_titles:
                name_parts = name_parts[1:]  # Remove the first part (title)

            if not name_parts:  # Skip if nothing is left after removing the title
                continue

            cleaned_name = " ".join(name_parts)

            prev_token = doc[ent.start - 1] if ent.start > 0 else None
            if prev_token and prev_token.pos_ not in {"DET", "ADJ"}:
                name_parts = cleaned_name.split()
                if len(name_parts) > 1:
                    dct[name_parts[0]] = ent.label_
                    dct[name_parts[-1]] = ent.label_
                else:
                    dct[cleaned_name] = ent.label_

                normalized_name = normalize_name(cleaned_name)
                
                name_parts = normalized_name.split()
                if len(name_parts) > 1:
                    first_name = name_parts[0]
                    last_name = name_parts[-1]
                    
                    if first_name not in name_to_tag:
                        name_to_tag[first_name] = f"NAME_{tag_counter}"
                        tag_counter += 1
                    
                    if last_name not in name_to_tag:
                        name_to_tag[last_name] = f"NAME_{tag_counter}"
                        tag_counter += 1
                    
                    text = re.sub(rf"\b{re.escape(cleaned_name)}\b", f"{name_to_tag[first_name]} {name_to_tag[last_name]}", text)
                else:
                    if normalized_name not in name_to_tag:
                        name_to_tag[normalized_name] = f"NAME_{tag_counter}"
                        tag_counter += 1
                    
                    text = re.sub(rf"\b{re.escape(cleaned_name)}\b", name_to_tag[normalized_name], text)
    
    return text, name_to_tag, dct

def main():
    meta_folder = "meta"
    short_story_folder = os.path.join(meta_folder, "shortstories")
    short_storys_json_path = os.path.join(meta_folder, "short_stories.json")

    # Load short_storys.json
    with open(short_storys_json_path, "r") as file:
        short_storys = json.load(file)

    for alias, full_name in short_storys.items():
        # Construct the path to the text file
        text_file_path = os.path.join(short_story_folder, f"full_{full_name.replace(' ', '_')}.txt")
        if not os.path.isfile(text_file_path):
            print(f"Missing text file for story: {full_name}")
            continue

        # Read the story text
        with open(text_file_path, "r", encoding="utf-8") as file:
            story_text = file.read()

        # Clean and tag the text
        story_tagged, name_to_tag, dct = replace_names_spacy(story_text)

        # Create a folder for the alias
        book_folder = os.path.join("books", alias)
        os.makedirs(book_folder, exist_ok=True)

        # Save processed files
        with open(os.path.join(book_folder, "complete_original_tagged.txt"), "w", encoding="utf-8") as file:
            file.write(story_tagged)

        with open(os.path.join(book_folder, "complete_original.txt"), "w", encoding="utf-8") as file:
            file.write(story_text)

        reversed_mapping = {v: k for k, v in name_to_tag.items()}
        with open(os.path.join(book_folder, "tags_character.json"), "w", encoding="utf-8") as file:
            json.dump(reversed_mapping, file)

        with open(os.path.join(book_folder, "all_characters.json"), "w", encoding="utf-8") as file:
            json.dump(dct, file)

        print(f"Processed and saved story for alias '{alias}'.")

if __name__ == "__main__":
    main()
