import os
import pandas as pd
from load_text import parse_text
from get_voices import get_voices

def voice_assigner(char_voice_dict):
    
    """
    Assign voice id's to speakers
    Takes a dictionary of main characters with their preferred voice names
    Assigns a voice id to each speaker according to the dictionary
    Rest of the speakers are assigned voices randomly
    Return the voice assignment dictionary
    """
    cwd = os.getcwd()
    char_gender_txt_path = os.path.join(cwd, "chars_gender.txt")
    char_gender_dict = {}

    with open(char_gender_txt_path, "r") as f:
        for line in f:  # Iterate over all lines
            entry = line.strip().split(":")  
            if len(entry) == 2:  # Ensure the line is well-formed
                char_gender_dict[entry[0].strip()] = entry[1].strip()
    
    voices_csv_path = get_voices()

    # currently assigning voices randomly (will need to update this later)
    df_voices = pd.read_csv(voices_csv_path)
    voice_id_list = df_voices["voice_id"].values
    # print(f"voice_id_list: {voice_id_list}")  # debug statement
    voice_name_list = df_voices["name"]
    voice_name_id_dict = dict(zip(voice_name_list, voice_id_list))
    voice_tags = df_voices["tags"]
    voice_genders = ["male" if "Male" in tags else "female" for tags in voice_tags]
    voice_name_gender_dict = dict(zip(voice_name_list, voice_genders))
    unassigned_voice_names = set(voice_name_list)

    # _, characters = parse_text(story_path)

    # print(f"unique speakers: {characters}")  # debug statement

    voice_assigment = {}

    for c, speaker in enumerate(char_gender_dict.keys()):
        if speaker in char_voice_dict.keys():
            voice_assigment[speaker] = voice_name_id_dict[char_voice_dict[speaker]]
            unassigned_voice_names.remove(char_voice_dict[speaker])
        else:
            if char_gender_dict[speaker].lower() == "male":
                for voice_name in unassigned_voice_names:
                    if voice_name_gender_dict[voice_name] == "male":
                        voice_assigment[speaker] = voice_name_id_dict[voice_name]
                        unassigned_voice_names.remove(voice_name)
                        break
                    else:
                        continue
            else:
                for voice_name in unassigned_voice_names:
                    if voice_name_gender_dict[voice_name] == "female":
                        voice_assigment[speaker] = voice_name_id_dict[voice_name]
                        unassigned_voice_names.remove(voice_name)
                        break
                    else:
                        continue

    return voice_assigment
