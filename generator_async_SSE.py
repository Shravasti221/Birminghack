from pyneuphonic import Neuphonic, TTSConfig
from pyneuphonic.player import AsyncAudioPlayer
import os
from dotenv import load_dotenv
import asyncio
import pandas as pd
from load_text import parse_text
from pyneuphonic._utils import async_save_audio

cwd = os.getcwd()
load_dotenv(dotenv_path=os.path.join(cwd, ".env"))

df_voices = pd.read_csv('voices.csv')
voice_id_list = df_voices["voice_id"]
voice_name_list = df_voices["name"]

# returning text list containing (index, speaker, speech) and unique speakers
text, unique_speakers = parse_text(os.path.join(cwd,"sample_story.txt"))

# random voice assignment to speakers
voice_assigment = {}
for c, speaker in enumerate(unique_speakers):
    voice_assigment[speaker] = voice_id_list[c]

async def main():
    
    client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))
    sse = client.tts.AsyncSSEClient()

    for line in text:
        speaker = line[1]
        speech = line[2]
        index = line[0]

        # Set the desired configurations: playback speed and voice
        tts_config = TTSConfig(speed=1, lang_code='en', voice_id=voice_assigment[speaker])

        async with AsyncAudioPlayer() as player:
            response = sse.send(speech, tts_config=tts_config)
            await async_save_audio(response, os.path.join(cwd, "output_audio", f"output_{index}.wav"))

asyncio.run(main())

