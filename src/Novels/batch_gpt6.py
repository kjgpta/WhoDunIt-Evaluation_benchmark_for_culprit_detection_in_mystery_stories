import os
import json
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")

def batching(stories, prompt_styles, models, output_batch_file):
    batch_ids = {}
    batch_dir = 'batch'
    for model in models:
        for story in stories:
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

    # Write all batch ids to a JSON file
    with open(output_batch_file, 'w') as outfile:
        json.dump(batch_ids, outfile, indent=4)

    print(f"Batch IDs saved to {output_batch_file}")

def main():
    with open('meta/books.json', 'r') as file:
        books = json.load(file)

    with open('meta/prompts.json', 'r') as file:
        prompts = json.load(file)

    with open('meta/models.json', 'r') as file:
        models = json.load(file)

    stories = list(books.keys())
    prompts = list(prompts.keys())
    output_batch_file = "batch_ids.json"

    batching(stories, prompts, models, os.path.join('batch', output_batch_file))

if __name__ == "__main__":
    main()
