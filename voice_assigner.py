import os
import random
import pandas as pd
from get_voices import get_voices  # Assuming this returns a CSV path

def voice_assigner(char_voice_dict):
    """
    Assign voice IDs to speakers.

    Args:
        char_voice_dict (dict): A dictionary of main characters with their preferred voice names.

    Returns:
        dict: A dictionary mapping each speaker to a voice ID.
    """

    cwd = os.getcwd()
    char_gender_txt_path = os.path.join(cwd, "chars_gender.txt")
    char_gender_dict = {}

    print(f"[DEBUG] Provided char_voice_dict: {char_voice_dict}")

    # Read character-gender mappings
    with open(char_gender_txt_path, "r") as f:
        for line in f:
            entry = line.strip().split(":")
            if len(entry) == 2:
                char_name = entry[0].strip().lower()
                gender = entry[1].strip().lower()
                char_gender_dict[char_name] = gender

    voices_csv_path = get_voices()  # Assumes it returns a CSV file path

    # Read voices CSV into DataFrame
    df_voices = pd.read_csv(voices_csv_path)

    # Build helper mappings
    voice_id_list = list(df_voices["voice_id"].values)
    voice_name_list = list(df_voices["name"].values)
    voice_tags = list(df_voices["tags"].values)

    voice_name_id_dict = dict(zip(voice_name_list, voice_id_list))
    voice_genders = ["male" if "Male" in tags else "female" for tags in voice_tags]
    voice_name_gender_dict = dict(zip(voice_name_list, voice_genders))

    voice_assignment = {}

    # Assign narrator
    narrator_voice_name = "Miles"
    if narrator_voice_name not in voice_name_id_dict:
        raise ValueError(f"Narrator voice '{narrator_voice_name}' not found in voices list.")

    voice_assignment["narrator"] = voice_name_id_dict[narrator_voice_name]

    # Prepare remaining voices
    remaining_voice_names = set(voice_name_list)
    remaining_voice_names.remove(narrator_voice_name)

    # Shuffle remaining voices for randomness in fallback
    remaining_voice_names = list(remaining_voice_names)
    random.shuffle(remaining_voice_names)

    # Assign voices to each character
    for speaker in char_gender_dict.keys():
        speaker_lower = speaker.lower()

        # Check if user provided a preferred voice
        if speaker_lower in (name.lower() for name in char_voice_dict.keys()):
            # Find the exact matching key from char_voice_dict (case insensitive)
            preferred_key = next(k for k in char_voice_dict if k.lower() == speaker_lower)
            preferred_voice_name = char_voice_dict[preferred_key]

            if preferred_voice_name not in voice_name_id_dict:
                print(f"[WARNING] Preferred voice '{preferred_voice_name}' for '{speaker}' not found in available voices.")
                continue

            voice_assignment[speaker] = voice_name_id_dict[preferred_voice_name]
            if preferred_voice_name in remaining_voice_names:
                remaining_voice_names.remove(preferred_voice_name)
            print(f"[INFO] Assigned preferred voice '{preferred_voice_name}' to '{speaker}'.")

        else:
            gender = char_gender_dict[speaker]
            found_voice = None

            # Search for a voice matching gender
            for voice_name in list(remaining_voice_names):
                if voice_name_gender_dict[voice_name].lower() == gender:
                    found_voice = voice_name
                    remaining_voice_names.remove(voice_name)
                    break

            # Fallback if no gender match is found
            if not found_voice and remaining_voice_names:
                found_voice = remaining_voice_names.pop()
                print(f"[WARNING] No {gender} voice left for '{speaker}'. Assigned '{found_voice}' instead.")

            if found_voice:
                voice_assignment[speaker] = voice_name_id_dict[found_voice]
                print(f"[INFO] Assigned voice '{found_voice}' to '{speaker}'.")

    print(f"[DEBUG] Final voice assignment: {voice_assignment}")
    return voice_assignment







# import os
# import pandas as pd
# from load_text import parse_text
# from get_voices import get_voices

# def voice_assigner(char_voice_dict):
    
#     """
#     Assign voice id's to speakers
#     Takes a dictionary of main characters with their preferred voice names
#     Assigns a voice id to each speaker according to the dictionary
#     Rest of the speakers are assigned voices randomly
#     Return the voice assignment dictionary
#     """
#     cwd = os.getcwd()
#     char_gender_txt_path = os.path.join(cwd, "chars_gender.txt")
#     char_gender_dict = {}
#     print(f" OOOOO char_voice_dict: {char_voice_dict}")  # debug statement
#     with open(char_gender_txt_path, "r") as f:
#         for line in f:  # Iterate over all lines
#             entry = line.strip().split(":")  
#             if len(entry) == 2:  # Ensure the line is well-formed
#                 char_gender_dict[entry[0].strip().lower()] = entry[1].strip().lower()
    
#     voices_csv_path = get_voices()

#     # currently assigning voices randomly (will need to update this later)
#     df_voices = pd.read_csv(voices_csv_path)
#     voice_id_list = list(df_voices["voice_id"].values)
#     # print(f"voice_id_list: {voice_id_list}")  # debug statement
#     voice_name_list = list(df_voices["name"].values)
#     voice_name_id_dict = dict(zip(voice_name_list, voice_id_list))
#     voice_tags = list(df_voices["tags"].values)
#     voice_genders = ["male" if "Male" in tags else "female" for tags in voice_tags]
#     voice_name_gender_dict = dict(zip(voice_name_list, voice_genders))
    
#     voice_assigment = {}
#     voice_assigment["narrator"] = voice_name_id_dict["Miles"]
#     voice_name_list.remove("Miles")
    
#     unassigned_voice_names = set(voice_name_list)

#     # _, characters = parse_text(story_path)

#     # print(f"unique speakers: {characters}")  # debug statement

#     for c, speaker in enumerate(char_gender_dict.keys()):
#         if speaker in char_voice_dict.keys():
#             voice_assigment[speaker] = voice_name_id_dict[char_voice_dict[speaker]]
#             unassigned_voice_names.remove(char_voice_dict[speaker])
#         else:
#             if char_gender_dict[speaker].lower() == "male":
#                 for voice_name in unassigned_voice_names:
#                     if voice_name_gender_dict[voice_name] == "male":
#                         voice_assigment[speaker] = voice_name_id_dict[voice_name]
#                         unassigned_voice_names.remove(voice_name)
#                         break
#                     else:
#                         continue
#             else:
#                 for voice_name in unassigned_voice_names:
#                     if voice_name_gender_dict[voice_name] == "female":
#                         voice_assigment[speaker] = voice_name_id_dict[voice_name]
#                         unassigned_voice_names.remove(voice_name)
#                         break
#                     else:
#                         continue

#     print(f"voice assignment: {voice_assigment}")  # debug statement
#     return voice_assigment
