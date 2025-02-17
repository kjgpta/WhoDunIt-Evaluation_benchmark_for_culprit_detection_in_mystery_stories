import os, json, openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")

def getResults(stories):
    batch_dir = 'batch'

    with open(os.path.join(batch_dir, 'batch_ids.json'), 'r') as books_file:
        batch_ids = json.load(books_file)

    for batch_ref, batch_id in batch_ids.items():
        try:
            if batch_ref.split('_')[1] in stories:
                file_id = client.batches.retrieve(batch_id).output_file_id
                file_response = client.files.content(file_id).text

                json_objects = file_response.strip().split('\n')
                
                # Parse each JSON string and store it in a list
                parsed_data = []
                for json_str in json_objects:
                    try:
                        # Load the main JSON object
                        data = json.loads(json_str)
                        
                        # Check if 'content' exists and is a string that can be converted to JSON
                        if "response" in data and "body" in data["response"]:
                            choices = data["response"]["body"].get("choices", [])
                            for choice in choices:
                                message_content = choice["message"].get("content", "")
                                if message_content != None:
                                    message_content = message_content.strip()
                                try:
                                    # Parse the content string if it's in JSON format
                                    choice["message"]["content"] = json.loads(message_content)
                                except json.JSONDecodeError as e:
                                    # Skip parsing if content is not a valid JSON string
                                    print(f"Error parsing JSON for jsonerror: {e}")
                                    print(f"Content: {message_content.strip()}")
                                    pass
                                except TypeError as e:
                                    print(f"Error parsing JSON for typeerror: {e}")
                                    print(f"Content: {message_content}")
                                    pass
                        
                        parsed_data.append(data)
                    
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
                        continue

                with open(os.path.join("batch", "results", f"{batch_ref[:-6]}.json"), "w") as outfile:
                    json.dump(parsed_data, outfile, indent=4)
                print(f"Batch {batch_ref[:-6]} results have been saved successfully!")
        except Exception as e:
            print(f"Error: {e}")
            print(f"Batch {batch_ref}")
    print("Batch results have been saved successfully!")

def generate_results(stories, prompts, models):
    for model in models:
        result_arr = []
        output_path = os.path.join("results", f"{model}_output.json")
        if os.path.exists(output_path):
            with open(output_path, 'r') as file:
                result_arr = json.load(file)
        print(f"Reading input for {model}")
        for story in stories:
            print(f"Reading input for {story}")
            dct = {}
            for prom in prompts:
                with open(os.path.join(os.path.join("batch", "results"), f"{model}_{story}_{prom}_reference.json"), 'r') as file:
                    results = json.load(file)
                for result in results:
                    id = result['custom_id']
                    dct = {}
                    predata = {}
                    st, pr, tt, ss, rn = id.split('_')[0], id.split('_')[1], id.split('_')[2], id.split('_')[3], int(id.split('_')[4])
                    if ss != "original":
                        with open(os.path.join("books", story, f"name_{ss}_{tt}.json"), 'r') as file:
                            predata = json.load(file)

                    if st == story and pr == prom:
                        try:
                            cul = result['response']['body']['choices'][0]['message']['content']['culprit']
                        except:
                            cul = "NAN"
                            print(f"culprit not found for {model}, {id}")
                        dct = {
                            "model": model,
                            "story": st,
                            "prompt_style": pr,
                            "text_type": tt,
                            "story_style": ss,
                            "response": cul,
                            "old_name_to_new_name_mapping" : predata,
                            "round": rn
                        }
                    else:
                        print(f"Skipping {id}")

                    result_arr.append(dct)
            print(f"Results generated for {story}")
        
        with open(output_path, 'w') as file:
            json.dump(result_arr, file)
        
        print(f"Results generated for {model}")

def main():
    with open('meta/books.json', 'r') as file:
        books = json.load(file)

    with open('meta/prompts.json', 'r') as file:
        prompts = json.load(file)

    with open('meta/models.json', 'r') as file:
        models = json.load(file)

    done_stories = []
    done_file = 'meta/done.json'
    if os.path.exists(done_file):
        with open(done_file, 'r') as file:
            done_stories = json.load(file)
    
    # Load excluded stories
    excluded_stories = []
    excluded_file = 'meta/excluded.json'
    if os.path.exists(excluded_file):
        with open(excluded_file, 'r') as file:
            excluded_stories = json.load(file)

    # Filter out excluded stories
    stories = [story for story in books.keys() if story not in excluded_stories]

    # Load state or initialize
    state_file = 'batch_state.json'
    if os.path.exists(state_file):
        with open(state_file, 'r') as state:
            state_data = json.load(state)
    else:
        state_data = {"last_index": 0}

    start_index = state_data.get("last_index", 0)
    batch_size = 9
    stories = stories[start_index-batch_size:min(start_index, len(stories))]

    stories = [story for story in stories if story not in excluded_stories and story not in done_stories] 
    prompts = list(prompts.keys())
    
    print(stories)
    getResults(stories)
    
    generate_results(stories, prompts, models)

    with open(os.path.join("meta", "done.json"), 'w') as file:
        json.dump(stories, file)

if __name__ == "__main__":
    main()