import os
import json
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")

def batching(stories, prompt_styles, models, output_batch_file, start_index=0, batch_size=20):
    batch_ids = {}
    batch_dir = 'batch'
    end_index = min(start_index + batch_size, len(stories))
    current_batch = stories[start_index:end_index]
    batch_path = os.path.join(batch_dir, 'ss_batch_ids.json')
    if os.path.exists(batch_path):
        with open(batch_path, 'r') as file:
            batch_ids = json.load(file)

    for model in models:
        for story in current_batch:
            for prompt_style in prompt_styles:
                # Construct the jsonl file path
                jsonl_file_path = os.path.join(batch_dir, "api_input", f"{model}_{story}_{prompt_style}_reference.jsonl")
                
                # Send the file to OpenAI
                batch_input_file = client.files.create(
                    file=open(jsonl_file_path, "rb"),
                    purpose="batch"
                )
                batch_input_file_id = batch_input_file.id

                # Create batch request
                batch_response = client.batches.create(
                    input_file_id=batch_input_file_id,
                    endpoint="/v1/chat/completions",
                    completion_window="24h",
                    metadata={
                        "description": f"Batch for {model}, {story}, {prompt_style}"
                    }
                )

                # Save batch id corresponding to jsonl file
                batch_ids[f"{model}_{story}_{prompt_style}_reference.jsonl"] = batch_response.id
                print(f"Batch created for {model}, {story}, {prompt_style}")

    # Append batch IDs to the existing output file
    if os.path.exists(output_batch_file):
        with open(output_batch_file, 'r') as outfile:
            existing_data = json.load(outfile)
            batch_ids.update(existing_data)

    with open(output_batch_file, 'w') as outfile:
        json.dump(batch_ids, outfile, indent=4)

    print(f"Batch IDs saved to {output_batch_file}")

    return end_index

def main():
    # Load meta files
    with open('meta/short_stories.json', 'r') as file:
        books = json.load(file)

    with open('meta/prompts.json', 'r') as file:
        prompts = json.load(file)

    with open('meta/models.json', 'r') as file:
        models = json.load(file)

    # Load excluded stories
    excluded_stories = []
    excluded_file = 'meta/excluded_ss.json'
    if os.path.exists(excluded_file):
        with open(excluded_file, 'r') as file:
            excluded_stories = json.load(file)

    # Filter out excluded stories
    stories = [story for story in books.keys() if story not in excluded_stories]

    # Load state or initialize
    state_file = 'ss_batch_state.json'
    if os.path.exists(state_file):
        with open(state_file, 'r') as state:
            state_data = json.load(state)
    else:
        state_data = {"last_index": 0}

    start_index = state_data.get("last_index", 0)
    batch_size = 20
    output_batch_file = "batch_ids.json"

    # Call batching for the current chunk
    next_index = batching(stories, list(prompts.keys()), models, os.path.join('batch', output_batch_file), start_index, batch_size)

    # Save updated state
    state_data["last_index"] = next_index
    with open(state_file, 'w') as state:
        json.dump(state_data, state)

    print(f"Processing completed for batch starting at index {start_index} and ending at index {next_index}.")

if __name__ == "__main__":
    main()
