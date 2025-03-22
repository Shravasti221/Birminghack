from pyneuphonic import Neuphonic
import os
import pandas as pd
from dotenv import load_dotenv

cwd = os.getcwd()
load_dotenv(dotenv_path=os.path.join(cwd, ".env"))

client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))
response = client.voices.list()  # get's all available voices
voices = response.data['voices']

df_voice = pd.DataFrame(voices)
df_voice.to_csv('voices.csv', index=False)