from util import *
import os, json, re, tiktoken

def replace_names_with_tags(text, name_to_tag):
    """
    Replace all occurrences of names in the text with corresponding tags (case-insensitive).
    """
    for name, tag in name_to_tag.items():
        # Escape the name for use in the regex and replace ignoring case
        name_pattern = re.escape(name)
        # Replace all occurrences of the name with the lowercase tag (case-insensitive)
        text = re.sub(rf"\b{name_pattern}\b", tag, text, flags=re.IGNORECASE)
    
    return text

def process_story(story_folder):
    tags_file_path = os.path.join(story_folder, "tags_character.json")
    text_file_path = os.path.join(story_folder, "partial_original.txt")
    result_file_path = os.path.join(story_folder, "partial_original_tagged.txt")
    
    with open(tags_file_path, 'r') as tags_file:
        tag_to_name = json.load(tags_file)
    
    name_to_tag = {v: k for k, v in tag_to_name.items()}
    
    with open(text_file_path, 'r', encoding="utf-8") as text_file:
        text = text_file.read()
    
    updated_text = replace_names_with_tags(text, name_to_tag)
    
    with open(result_file_path, 'w', encoding="utf-8") as result_file:
        result_file.write(updated_text)

def process_all_stories(killer_json_path):

    with open(killer_json_path, 'r') as killer_file:
        story_names = json.load(killer_file)
    
    for story_name in story_names:
        story_folder = os.path.join("books", story_name)
        try:
            process_story(story_folder)
            print(f"Processed story: {story_name}")
        except:
            print(f"Error processing story: {story_name}")

def main():
    meta_dir = 'meta'
    book_dir = 'books'

    killer_file = 'killers_ss.json'
    excluded_file = 'excluded_ss.json'

    killer_file_path = os.path.join(meta_dir, killer_file)
    excluded_file_path = os.path.join(meta_dir, excluded_file)

    with open(killer_file_path, 'r') as killer_file_obj:
        killer_data = json.load(killer_file_obj)
    
    killer = ""
    excluded_data = []
    # Iterate over the stories
    for story, killer_name in killer_data.items(): 
        # Assuming the story names are the same in both files
        killer = " ".join(killer_name)
        print(story + " :Processing " + killer)
        try:
            book_folder = os.path.join(book_dir, story)
            file_path = os.path.join(book_folder, "complete_original.txt")
            # print(file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file if line.strip()]

            text = ' '.join(lines)

            prompt = """
                        Analyze the given story carefully and identify the exact point where the actual culprit reveals they committed the crime.

                        The culprit is: """ + killer + """.
                        False identifiers: Ignore confessions from other characters. Only consider the confession from the actual culprit.
                        Key point: The line you return must be the exact text where the culprit admits their crime. Do not generate or alter any part of the line—use it exactly as it appears in the story.
                        The output should be a JSON object with two keys:

                        "culprit_reveals": A boolean (True if the culprit confesses, False if they do not).
                        "line": The exact line from the story where the confession happens (4-5 words maximum). If no such line exists, return an empty string ("").
                        Instructions:

                        Strictly follow the text provided—do not create or modify any lines.
                        If the culprit does not explicitly confess, return culprit_reveals: False and line: "".
                        Before generating output, confirm that the confession line is exactly present in the story.
                        Output only the JSON object with nothing extra—no code blocks or explanations.                
                    """
            try:
                response, flag = call_openai_api(text, prompt)
                if flag:
                    print(story + " :Error : " + str(response))
                    continue
                
                if is_valid_response(response):
                    response_json = json.loads(response)
                    with open(os.path.join(book_folder, "culprit.json"), "w") as file:
                        json.dump(response_json, file)
                    if response_json["culprit_reveals"] == True:
                        context_text, flag = extract_context_before_line(text, response_json["line"])
                    else:
                        context_text = text
                        flag = True
                        print(story + " :Culprit does not reveal")

                    with open(os.path.join(book_folder, "partial_original.txt"), "w", encoding="utf-8") as file:
                        file.write(context_text)

                    print(story + " :Success" if flag else story + " :line not found")
                else:
                    print(story + " :Wrong Response")
            except Exception as e:
                with open(os.path.join(book_folder, "partial_original.txt"), "w", encoding="utf-8") as file:
                    file.write(text)
                excluded_data.append(story)
                print(story + " : Token Limit : " + str(e))
        except FileNotFoundError:
            print("Error: The " + story + " was not found.")
    with open(excluded_file_path, 'w') as excluded_file_obj:
        json.dump(excluded_data, excluded_file_obj)
    process_all_stories(killer_file_path)

if __name__ == "__main__":
    main()