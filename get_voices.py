from pyneuphonic import Neuphonic
import os
import pandas as pd
from dotenv import load_dotenv

def get_voices():
    """
    Get all available voices, filters english voices and then store them in a csv file
    Returns the path to the voices csv file
    """
    cwd = os.getcwd()
    load_dotenv(dotenv_path=os.path.join(cwd, ".env"))

    client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))
    response = client.voices.list()  # get's all available voices
    voices = response.data['voices']

    df_voice = pd.DataFrame(voices)
    df_voice = df_voice[df_voice['lang_code'] == 'en']  # filter english voices
    save_path = os.path.join(cwd, 'voices.csv')
    df_voice.to_csv(save_path, index=False)
    return save_path