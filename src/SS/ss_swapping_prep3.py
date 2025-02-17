from util import *

def main():
    meta_dir = 'meta'
    books_dir = 'books'
    # Load killer.json from meta folder
    with open(os.path.join(meta_dir, 'killers_ss.json'), 'r') as killer_file:
        killer_info = json.load(killer_file)

    # Iterate over each story in books.json
    for folder_name, _ in killer_info.items():
        print(f"Processing story: {folder_name}")
        story_dir = os.path.join(books_dir, folder_name)
        
        # Prepare paths for each required file in the story directory
        result_txt_path = os.path.join(story_dir, 'complete_original_tagged.txt')
        before_reveal_result_txt_path = os.path.join(story_dir, 'partial_original_tagged.txt')
        identity_revealed_json_path = os.path.join(story_dir, 'culprit.json')
        tags_character_json_path = os.path.join(story_dir, 'tags_character.json')
        
        # Read and format text from the required files
        complete_text_tags_text = read_and_format_text(result_txt_path)
        before_reveal_tags_text = read_and_format_text(before_reveal_result_txt_path)

        # Read JSON data from identity_revealed.json
        with open(identity_revealed_json_path, 'r') as identity_file:
            explicit_revealing = json.load(identity_file)
        
        # Read character tags from tags_character.json
        with open(tags_character_json_path, 'r') as character_tags_file:
            character_tags = json.load(character_tags_file)
        
        # Extract killer information from killer.json
        killer_names = " ".join(killer_info[folder_name]).split()
        real_culprit_tags = {key: value for key, value in character_tags.items() if value in killer_names}
        
        tag_to_new_name_mapping_1_0, old_name_to_new_name_mapping_1_0, replaced_text_1_0 = replace_culprit_with_characters(real_culprit_tags, character_tags, complete_text_tags_text)
        tag_to_new_name_mapping_1_1, old_name_to_new_name_mapping_1_1, replaced_text_1_1 = replace_culprit_with_characters(real_culprit_tags, character_tags, before_reveal_tags_text)

        tag_to_new_name_mapping_2_0, old_name_to_new_name_mapping_2_0, replaced_text_2_0 = replacing_and_randomizing_tags(character_tags, complete_text_tags_text)
        tag_to_new_name_mapping_2_1, old_name_to_new_name_mapping_2_1, replaced_text_2_1 = replacing_and_randomizing_tags(character_tags, before_reveal_tags_text)

        tag_to_new_name_mapping_3_0, old_name_to_new_name_mapping_3_0, replaced_text_3_0 = replacing_tags('harry_potter.json', character_tags, complete_text_tags_text)
        tag_to_new_name_mapping_3_1, old_name_to_new_name_mapping_3_1, replaced_text_3_1 = replacing_tags('harry_potter.json', character_tags, before_reveal_tags_text)

        tag_to_new_name_mapping_4_0, old_name_to_new_name_mapping_4_0, replaced_text_4_0 = replacing_tags('hollywood_celebs.json', character_tags, complete_text_tags_text)
        tag_to_new_name_mapping_4_1, old_name_to_new_name_mapping_4_1, replaced_text_4_1 = replacing_tags('hollywood_celebs.json', character_tags, before_reveal_tags_text)

        tag_to_new_name_mapping_5_0, old_name_to_new_name_mapping_5_0, replaced_text_5_0 = replacing_tags('indian_celebs.json', character_tags, complete_text_tags_text)
        tag_to_new_name_mapping_5_1, old_name_to_new_name_mapping_5_1, replaced_text_5_1 = replacing_tags('indian_celebs.json', character_tags, before_reveal_tags_text)

        # Writing for killer swap
        with open(os.path.join(story_dir, 'tag_culprit_complete.json'), 'w') as result_file:
            json.dump(tag_to_new_name_mapping_1_0, result_file)
        
        with open(os.path.join(story_dir, 'name_culprit_complete.json'), 'w') as result_file:
            json.dump(old_name_to_new_name_mapping_1_0, result_file)

        with open(os.path.join(story_dir, 'complete_culprit'), "w", encoding="utf-8") as file:
            file.write(replaced_text_1_0)

        with open(os.path.join(story_dir, 'tag_culprit_partial.json'), 'w') as result_file:
            json.dump(tag_to_new_name_mapping_1_1, result_file)
        
        with open(os.path.join(story_dir, 'name_culprit_partial.json'), 'w') as result_file:
            json.dump(old_name_to_new_name_mapping_1_1, result_file)

        with open(os.path.join(story_dir, 'partial_culprit'), "w", encoding="utf-8") as file:
            file.write(replaced_text_1_1)

        # Writing for all characters swap
        with open(os.path.join(story_dir, 'tag_all_complete.json'), 'w') as result_file:
            json.dump(tag_to_new_name_mapping_2_0, result_file)
        
        with open(os.path.join(story_dir, 'name_all_complete.json'), 'w') as result_file:
            json.dump(old_name_to_new_name_mapping_2_0, result_file)

        with open(os.path.join(story_dir, 'complete_all'), "w", encoding="utf-8") as file:
            file.write(replaced_text_2_0)

        with open(os.path.join(story_dir, 'tag_all_partial.json'), 'w') as result_file:
            json.dump(tag_to_new_name_mapping_2_1, result_file)
        
        with open(os.path.join(story_dir, 'name_all_partial.json'), 'w') as result_file:
            json.dump(old_name_to_new_name_mapping_2_1, result_file)

        with open(os.path.join(story_dir, 'partial_all'), "w", encoding="utf-8") as file:
            file.write(replaced_text_2_1)
        
        # Writing for Harry Potter swap
        with open(os.path.join(story_dir, 'tag_hp_complete.json'), 'w') as result_file:
            json.dump(tag_to_new_name_mapping_3_0, result_file)
        
        with open(os.path.join(story_dir, 'name_hp_complete.json'), 'w') as result_file:
            json.dump(old_name_to_new_name_mapping_3_0, result_file)

        with open(os.path.join(story_dir, 'complete_hp'), "w", encoding="utf-8") as file:
            file.write(replaced_text_3_0)

        with open(os.path.join(story_dir, 'tag_hp_partial.json'), 'w') as result_file:
            json.dump(tag_to_new_name_mapping_3_1, result_file)
        
        with open(os.path.join(story_dir, 'name_hp_partial.json'), 'w') as result_file:
            json.dump(old_name_to_new_name_mapping_3_1, result_file)

        with open(os.path.join(story_dir, 'partial_hp'), "w", encoding="utf-8") as file:
            file.write(replaced_text_3_1)
        
        # Writing for Hollywood Celebs swap
        with open(os.path.join(story_dir, 'tag_hollywood_complete.json'), 'w') as result_file:
            json.dump(tag_to_new_name_mapping_4_0, result_file)
        
        with open(os.path.join(story_dir, 'name_hollywood_complete.json'), 'w') as result_file:
            json.dump(old_name_to_new_name_mapping_4_0, result_file)

        with open(os.path.join(story_dir, 'complete_hollywood'), "w", encoding="utf-8") as file:
            file.write(replaced_text_4_0)

        with open(os.path.join(story_dir, 'tag_hollywood_partial.json'), 'w') as result_file:
            json.dump(tag_to_new_name_mapping_4_1, result_file)
        
        with open(os.path.join(story_dir, 'name_hollywood_partial.json'), 'w') as result_file:
            json.dump(old_name_to_new_name_mapping_4_1, result_file)

        with open(os.path.join(story_dir, 'partial_hollywood'), "w", encoding="utf-8") as file:
            file.write(replaced_text_4_1)

        # Writing for Bollywood Celebs swap
        with open(os.path.join(story_dir, 'tag_bollywood_complete.json'), 'w') as result_file:
            json.dump(tag_to_new_name_mapping_5_0, result_file)
        
        with open(os.path.join(story_dir, 'name_bollywood_complete.json'), 'w') as result_file:
            json.dump(old_name_to_new_name_mapping_5_0, result_file)

        with open(os.path.join(story_dir, 'complete_bollywood'), "w", encoding="utf-8") as file:
            file.write(replaced_text_5_0)

        with open(os.path.join(story_dir, 'tag_bollywood_partial.json'), 'w') as result_file:
            json.dump(tag_to_new_name_mapping_5_1, result_file)
        
        with open(os.path.join(story_dir, 'name_bollywood_partial.json'), 'w') as result_file:
            json.dump(old_name_to_new_name_mapping_5_1, result_file)

        with open(os.path.join(story_dir, 'partial_bollywood'), "w", encoding="utf-8") as file:
            file.write(replaced_text_5_1)
        
        print(f"Processed story: {folder_name}")
    
if __name__ == '__main__':
    main()