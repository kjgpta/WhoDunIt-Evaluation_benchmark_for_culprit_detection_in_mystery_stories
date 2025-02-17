import os
import json

def storiesRequest(stories, prompts, models):
    api_url = "/v1/chat/completions"
    
    for model in models:
        for story in stories:
            for prom in prompts:
                all_requests = []

                file_name = os.path.join("data", f"{story}_{prom}_input.json")
                if not os.path.exists(file_name):
                    print(f"File {file_name} not found. Skipping...")
                    continue

                with open(file_name, 'r') as f:
                    data = json.load(f)[story]               

                # Extract necessary data
                for data_point in data:
                    story = data_point['story']
                    prompt_style = data_point['prompt_style']
                    text_type = data_point['text_type']
                    story_style = data_point['story_style']
                    tag_to_new_name_mapping = data_point['tag_to_new_name_mapping']
                    old_name_to_new_name_mapping = data_point['old_name_to_new_name_mapping']
                    text = data_point['text']
                    prompt = data_point['prompt']

                    # Create 10 requests per model
                    
                    for round_num in range(1, 11):
                        custom_id = f"{story}_{prompt_style}_{text_type}_{story_style}_{round_num}"
                        request_body = {
                            "custom_id": custom_id,
                            "method": "POST",
                            "url": api_url,
                            "story": story,
                            "prompt_style": prompt_style,
                            "text_type": text_type,
                            "story_style": story_style,
                            "tag_to_new_name_mapping": tag_to_new_name_mapping,
                            "old_name_to_new_name_mapping": old_name_to_new_name_mapping,
                            "round": round_num,
                            "body": {
                                "model": model,
                                "messages": [
                                    {"role": "user", "content": prompt},
                                    {"role": "system", "content": text}
                                ],
                                
                                "temperature": 0.5,
                                "top_p": 0.9,
                                "response_format": {"type": "json_object"},
                                "max_tokens": 500
                            }
                        }
                            
                            # Store the request in the list
                        all_requests.append(request_body)

                # Save all requests to a JSON file
                with open(os.path.join("batch", "batch_input", f"{model}_{story}_{prom}_reference.json"), "w") as outfile:
                    json.dump(all_requests, outfile)
                print(f"Total number of requests created: {len(all_requests)}")
                print(f"Batch requests saved to {model}_{story}_{prom}_reference.json")

def batchRequest(stories, prompts, models):
    for model in models:
        for story in stories:
            for prom in prompts:
                print(f"Processing {model} {story} {prom}...")
                file_name = os.path.join(os.path.join("batch", "batch_input"), f"{model}_{story}_{prom}_reference.json")
                if not os.path.exists(file_name):
                    print(f"File {file_name} not found. Skipping...")
                    continue

                with open(file_name, 'r') as f:
                    data = json.load(f)

                with open(os.path.join("batch", "api_input", f"{model}_{story}_{prom}_reference.jsonl"), 'w') as outfile:
                    for entry in data:
                        jsonl_entry = {
                            "custom_id": entry["custom_id"],
                            "method": entry["method"],
                            "url": entry["url"],
                            "body": entry["body"]
                        }
                        outfile.write(json.dumps(jsonl_entry) + '\n') 
                print(f"Processed {model} {story} {prom}...")

def main():
    with open('meta/short_stories.json', 'r') as file:
        books = json.load(file)

    with open('meta/prompts.json', 'r') as file:
        prompts = json.load(file)

    with open('meta/models.json', 'r') as file:
        models = json.load(file)

    stories = list(books.keys())
    prompts = list(prompts.keys())
    print("Creating batch input")
    storiesRequest(stories, prompts, models)
    print("Creating API input")
    batchRequest(stories, prompts,models)

if __name__ == "__main__":
    main()