import os
import pandas as pd
from load_text import parse_text

def voice_assigner(story_path):
    
    """
    Assign voice id's to speakers
    Return the voice assignment dictionary
    """

    cwd = os.getcwd()

    # currently assigning voices randomly (will need to update this later)
    df_voices = pd.read_csv(os.path.join(cwd, 'voices.csv'))
    voice_id_list = df_voices["voice_id"]
    voice_name_list = df_voices["name"]

    _, unique_speakers = parse_text(story_path)

    voice_assigment = {}
    for c, speaker in enumerate(unique_speakers):
        voice_assigment[speaker] = voice_id_list[c]

    return voice_assigment
