import re, requests, json, os, openai, random, unicodedata, random
from dotenv import load_dotenv

load_dotenv()

def extract_context_before_line(text, search_line):
    # Step 1: Find the index of the search line in the text
    index = text.find(search_line)
    
    if index != -1:
        # If the search_line is found, extract everything before it
        context_text = text[:index]
        return context_text, True
    else:
        # If search_line is not found, return the whole text and False
        return text, False


def is_valid_response(response_text):
    try:
        response_json = json.loads(response_text)
    except json.JSONDecodeError:
        return False
    
    if not isinstance(response_json, dict):
        return False

    required_keys = ["culprit_reveals", "line"]
    if not all(key in response_json for key in required_keys):
        return False

    if not isinstance(response_json["culprit_reveals"], bool):
        return False
    if not isinstance(response_json["line"], str):
        return False

    return True

def extract_info(text):
    return json.dumps({"extracted_info": text})

def call_openai_api(text, prompt):
    try:
        from openai import OpenAI
        client = OpenAI()

        openai.api_key = os.getenv("OPENAI_API_KEY")

        messages = [
            {"role": "user", "content": prompt},
            {"role": "system", "content": text}
        ]

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.0,
            response_format={ "type": "json_object" },

        )
        response_message = response.choices[0].message.content
        return response_message, False
    except Exception as e:
        return e, True

def get_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8'  # Set the encoding to utf-8
    return response.text

def normalize_name(name):
    name = re.sub(r"'s\b", "", name) 
    name = re.sub(r"[’]", "", name)   
    name = re.sub(r"[.]", "", name)     
    name = re.sub(r"[\r\n]+", " ", name) 
    name = name.strip()                 
    name = name.lower()
    
    return name

def normalize_text(name):
    # Normalize Unicode characters to their closest ASCII equivalent (e.g., é -> e)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # Remove any character that is not a letter (A-Z or a-z)
    name = re.sub(r'[^a-zA-Z\s]', '', name)
    
    # Strip extra spaces and return
    return name.strip()

def clean_gutenberg_text(text):
    in_story = False
    cleaned_text = []
    lines = text.splitlines()

    for line in lines:
        normalized_line = line.strip()

        if "*** START OF THE PROJECT GUTENBERG EBOOK" in normalized_line:
            in_story = True
            continue  

        if "*** END OF THE PROJECT GUTENBERG EBOOK" in normalized_line:
            in_story = False
            continue  

        if in_story:
            if re.match(r'^\s*\d+\.\s+', normalized_line): 
                continue
            
            if normalized_line:
                cleaned_text.append(normalized_line)
    story_text = '\n'.join(cleaned_text)
    
    return story_text

def replacing_tags(file_name, tag_mappings, text):
    # Path to the JSON file in the 'meta' folder
    file_path = os.path.join('meta', file_name)
    
    # Read the names from the JSON file
    with open(file_path, 'r') as file:
        names_data = json.load(file)
    
    # Create dictionaries to store new mappings
    tag_to_new_name_mapping = {}
    old_name_to_new_name_mapping = {}

    # Assign new random names to each tag
    used_names = set()
    
    for name_tag, old_name in tag_mappings.items():
        if len(used_names) < len(names_data):
            unused_names = list(set(names_data) - used_names)
        if len(unused_names) > 0:
            new_name = random.choice(unused_names)
        else:
            new_name = random.choice(names_data)

        used_names.add(new_name)
        tag_to_new_name_mapping[name_tag] = new_name
        old_name_to_new_name_mapping[old_name] = new_name
    
    # Replace the name tags in the text with the new names
    for name_tag, new_name in tag_to_new_name_mapping.items():
        text = re.sub(rf'\b{name_tag}\b', new_name.capitalize(), text)
    
    return tag_to_new_name_mapping, old_name_to_new_name_mapping, text

def replacing_and_randomizing_tags(tag_mappings, text):
    # Create dictionaries to store new mappings
    tag_to_new_name_mapping = {}
    old_name_to_new_name_mapping = {}
    used_names = set()

    # List of names to randomize
    all_names = list(tag_mappings.values())

    # Shuffle the names to create random mapping
    random.shuffle(all_names)

    # Assign new random names to each tag and update both mappings
    for index, (name_tag, old_name) in enumerate(tag_mappings.items()):
        new_name = all_names[index]
        
        if len(used_names) < len(all_names):
            unused_names = list(set(all_names) - used_names)
        if len(unused_names) > 0:
            new_name = random.choice(unused_names)
        else:
            new_name = random.choice(all_names)
        
        used_names.add(new_name)
        tag_to_new_name_mapping[name_tag] = new_name
        old_name_to_new_name_mapping[old_name] = new_name

    # Replace the name tags in the text with the new names
    for name_tag, new_name in tag_to_new_name_mapping.items():
        text = re.sub(rf'\b{name_tag}\b', new_name.capitalize(), text)
    
    return tag_to_new_name_mapping, old_name_to_new_name_mapping, text

def replace_culprit_with_characters(culprit_tags, character_tags, text):
    # Create dictionaries to store new mappings
    tag_to_new_name_mapping = {}
    old_name_to_new_name_mapping = {}
    used_names = set()

    # List of non-culprit character tags
    non_culprit_tags = [tag for tag in character_tags if tag not in culprit_tags]

    # Shuffle the non-culprit tags to create random mapping for the culprits
    random.shuffle(non_culprit_tags)

    # Assign new random character tags to each culprit tag and update mappings
    for index, (culprit_tag, culprit_name) in enumerate(culprit_tags.items()):
        new_tag = non_culprit_tags[index]
        new_name = character_tags[new_tag]

        # Ensure the new name hasn't been used and isn't the same as the culprit's original name
        while new_name == culprit_name or new_name in used_names:
            new_tag = random.choice(non_culprit_tags)
            new_name = character_tags[new_tag]

        used_names.add(new_name)
        tag_to_new_name_mapping[culprit_tag] = new_name
        old_name_to_new_name_mapping[culprit_name] = new_name

    # For all other non-culprit tags, keep the same name
    for tag, name in character_tags.items():
        if tag not in culprit_tags:
            tag_to_new_name_mapping[tag] = name

    # Replace the tags in the text with the corresponding names (including swapped culprits)
    for name_tag, new_name in tag_to_new_name_mapping.items():
        text = re.sub(rf'\b{name_tag}\b', new_name.capitalize(), text)

    return tag_to_new_name_mapping, old_name_to_new_name_mapping, text



def read_and_format_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    formatted_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            formatted_lines.append(stripped_line)
    
    return ' '.join(formatted_lines)