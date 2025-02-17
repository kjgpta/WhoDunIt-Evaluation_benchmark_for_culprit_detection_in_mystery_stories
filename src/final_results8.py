import os, json
import pandas as pd
from collections import defaultdict

def validation(response, killer, mapping_orig):
    if response is None or response == "" or response == "NAN":
        return False
    response = response.lower().split()
    killer = killer.lower()
    if mapping_orig == {}:
        for name in response:
            if name in killer:
                return True
        return False

    mapping = {}
    for key, value in mapping_orig.items():
        mapping[value.lower()] = key.lower()

    flag = False
    for name in response:
        if name in mapping:
            if mapping[name] in killer:
                flag = True
    
    return flag

def final_results_generation(output_file_json, output_file_excel, models):
    result_dir = 'results'
    final_data = []
    
    # Process each model's data
    for model_name in models:
        with open(os.path.join(result_dir, f"{model_name}_validated.json"), 'r') as f:
            data = json.load(f)
        
        # Dictionary to store grouped data
        grouped_data = defaultdict(lambda: {"valid_true": 0, "valid_false": 0})

        # Group data by the specified keys and count validity true/false
        for entry in data:
            key = (
                entry["model"],
                entry["story"],
                entry["prompt_style"],
                entry["text_type"],
                entry["story_style"],
            )
            if entry["validity"]:
                grouped_data[key]["valid_true"] += 1
            else:
                grouped_data[key]["valid_false"] += 1
        
        # Create final structured data with correct_response calculation
        for key, counts in grouped_data.items():
            correct_response = (
                counts["valid_true"] >= counts["valid_false"]
            )
            
            final_data.append({
                "model": key[0],
                "story": key[1],
                "prompt_style": key[2],
                "text_type": key[3],
                "story_style": key[4],
                "correct_response": correct_response
            })
    
    # Write the processed data to the JSON output file
    with open(output_file_json, 'w') as f:
        json.dump(final_data, f, indent=4)
    print(f"Data successfully saved to {output_file_json}")
    
    # Save the processed data to an Excel file
    df = pd.DataFrame(final_data)
    df.to_excel(output_file_excel, index=False)
    print(f"Data successfully saved to {output_file_excel}")

def main():
    meta_dir = 'meta'
    result_dir = 'results'

    with open('meta/models.json', 'r') as file:
        models = json.load(file)

    killer_file = 'killer.json'
    killers_ss_file = 'killers_ss.json'

    killer_file_path = os.path.join(meta_dir, killer_file)
    killers_ss_file_path = os.path.join(meta_dir, killers_ss_file)

    with open(killer_file_path, 'r') as killer_file_obj:
        killer_data = json.load(killer_file_obj)

    with open(killers_ss_file_path, 'r') as killers_ss_file_obj:
        killers_ss_data = json.load(killers_ss_file_obj)

    # Combine both dictionaries
    killer_data.update(killers_ss_data)

    for model_name in models:
        res = []

        with open(os.path.join(result_dir, f"{model_name}_output.json"), 'r') as killer_file_obj:
            gpt_output = json.load(killer_file_obj)
        print(f"Validating {model_name} output")
        for data in gpt_output:
            model = data['model']
            story = data['story']
            prompt_style = data['prompt_style']
            text_type = data['text_type']
            story_style = data['story_style']
            killer_name = data['response']
            round = data['round']
            validity = validation(killer_name, " ".join(killer_data[story]), data['old_name_to_new_name_mapping'])

            res.append({
                'model': model,
                'story': story,
                'prompt_style': prompt_style,
                'text_type': text_type,
                'story_style': story_style,
                'validity': validity,
                'round': round
            })

        with open(os.path.join(result_dir, f"{model_name}_validated.json"), 'w') as killer_file_obj:
            json.dump(res, killer_file_obj, indent=4)

        print(f"{model} output")

    final_results_generation(
        os.path.join("results", "final_output.json"), 
        os.path.join("results", "final_output.xlsx"), models
    )

if __name__ == "__main__":
    main()