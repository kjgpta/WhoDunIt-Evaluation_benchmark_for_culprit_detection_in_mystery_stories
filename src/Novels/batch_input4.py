import json, os

def prompt(prompting_startegy):
    pre_prompt = f"""
                    You are a detective that helps to analyze crime stories and find culprits. 
                    You are given a story and you need to identify the culprit based on the story. 
                    You need to provide a detailed explanation of how you reached your conclusion. 
                    The task is to identify the culprit responsible for the crime in the provided story. 
                    Carefully examine the provided story and identify the actual culprit responsible for the crime. 
                    You are expected to thoroughly consider all current and past events, character actions, dialogues, and any evidence or clues presented in the story to reach a logical conclusion about the true culprit.

                    **Prompting Strategy:** \n {prompting_startegy} 
                """
    
    post_prompt = """
                    Given above is the prompting strategy I'm using to generate the response.

                    The task is to identify the culprit who is a person and not an object which is responsible for the crime in the provided story. 
                    Carefully examine the provided story and identify the actual culprit responsible for the crime. You are expected to thoroughly consider all current and past events, character actions, dialogues, and any evidence or clues presented in the story to reach a logical conclusion about the true culprit.

                    Requirements:
                    Explanation: 
                    1. Provide a detailed reasoning based on the events of the story that leads to the identification of the culprit. Include all relevant clues and connections.

                    Culprit: 
                    1. Provide the full name of the culprit which is a person as mentioned in the story, but:
                    2. Do not include any titles (e.g., Mr., Mrs., Dr.).
                    3. Do not use special characters, numbers, or non-alphabetic symbols (e.g., punctuation marks, hashtags).
                    4. Only the name should appear, without any extra information or formatting.
                    
                    Response Format:
                    Your response must be a valid JSON object with the following structure:
                    {
                        "explanation" : A string containing your detailed reasoning for identifying the culprit. This string must contain only alphabetic characters (A-Z, a-z) and spaces—no punctuation, numbers, or other symbols.
                        "culprit" : A string with the full name of the culprit, containing only alphabetic characters and spaces. No special symbols, titles, or extra formatting.
                    }
                    
                    Important Considerations:
                    Do not include any titles (e.g., Mr., Mrs., Dr.). Only the name should appear, without any extra information or formatting.
                    Ensure that the JSON object uses only alphabetic characters in both the explanation and the culprit’s name.
                    Avoid using any form of code formatting, symbols, or numbers in your response.
                    The JSON object should be clean and free of unnecessary characters to maintain simplicity and clarity.
                    The culprit should be identified based on the story provided and also his name should be mentioned as it is in the story.
                    Also there should not be any title of anything apart from name of the culprit in the culprit field.
                    Keep in mind that the response should only be name and no other character or symbols like numerals, punctuations, etc.
                """
    return pre_prompt + post_prompt

def main():
    books_dir = 'books'
    with open('meta/prompts.json', 'r') as file:
        prompts = json.load(file)

    with open('meta/books.json', 'r') as file:
        books = json.load(file)

    text_types = ['complete', 'partial']
    story_styles = ['original', 'culprit', 'all', 'hp', 'hollywood', 'bollywood']


    for story, _ in books.items():
        for prompt_style, prompt_desc in prompts.items():
            result_json = {}
            print(f"Processing Story: {story} Prompt: {prompt_style}.")
            # print(f"Prompt {prompt_style}.")
            for text_type in text_types:
                # print(f"Text type {text_type}.")
                for story_style in story_styles:
                    # print(f"Story style {story_style}.")
                    text = ""
                    tag_to_new_name_mapping = {}
                    old_name_to_new_name_mapping = {}
                    if story_style == 'original':
                        with open(os.path.join(books_dir, story, f'{text_type}_{story_style}.txt'), 'r', encoding="utf-8") as text_file:
                            text = text_file.read()
                    else:
                        with open(os.path.join(books_dir, story, f'{text_type}_{story_style}'), 'r', encoding="utf-8") as text_file:
                            text = text_file.read()
                    
                    if story_style != 'original':
                        with open(os.path.join(books_dir, story, f'tag_{story_style}_{text_type}.json'), 'r') as f:
                            tag_to_new_name_mapping = json.load(f)
                        
                        with open(os.path.join(books_dir, story, f'name_{story_style}_{text_type}.json'), 'r') as f:
                            old_name_to_new_name_mapping = json.load(f)

                    if story not in result_json:
                        result_json[story] = []

                    result_json[story].append(
                        {
                        "story": story,
                        "prompt_style": prompt_style,
                        "text_type": text_type,
                        "story_style": story_style,
                        "tag_to_new_name_mapping" : tag_to_new_name_mapping,
                        "old_name_to_new_name_mapping" : old_name_to_new_name_mapping,
                        "text" : text,
                        "prompt" : prompt(prompt_desc)
                        }
                    )
                    
                    
            result_file_path = os.path.join("data", f"{story}_{prompt_style}_input.json")
            with open(result_file_path, 'w') as result_file:
                json.dump(result_json, result_file)
            print(f"Processed Story: {story} Prompt: {prompt_style}.")

if __name__ == "__main__":
    main()