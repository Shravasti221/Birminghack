import os
import pandas as pd
from load_text import parse_text
from get_voices import get_voices

def voice_assigner(story_path):
    
    """
    Assign voice id's to speakers
    Return the voice assignment dictionary
    """

    voices_csv_path = get_voices()

    # currently assigning voices randomly (will need to update this later)
    df_voices = pd.read_csv(voices_csv_path)
    voice_id_list = df_voices["voice_id"].values
    # print(f"voice_id_list: {voice_id_list}")  # debug statement
    voice_name_list = df_voices["name"]

    _, unique_speakers = parse_text(story_path)

    # print(f"unique speakers: {unique_speakers}")  # debug statement

    voice_assigment = {}
    for c, speaker in enumerate(unique_speakers):
        voice_assigment[speaker] = voice_id_list[c%len(voice_id_list)]

    return voice_assigment
