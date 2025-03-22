from pyneuphonic import Neuphonic, TTSConfig
from pyneuphonic.player import AsyncAudioPlayer
import os
from dotenv import load_dotenv
import asyncio
import pandas as pd
from load_text import parse_text
from pyneuphonic._utils import async_save_audio
from voice_assigner import voice_assigner
from merge_audio_files import merge_audio_files

def generate_audio_files(story_text_path):
    """
    Generates audio files from the text file and stores it into the output_audio folder
    Takes the path to processed story text file as input
    """
    cwd = os.getcwd()
    load_dotenv(dotenv_path=os.path.join(cwd, ".env"))

    # returning text list containing (index, speaker, speech) and unique speakers
    text, unique_speakers = parse_text(story_text_path)
    voice_assigment = voice_assigner(story_text_path)

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
    final_audio_path = merge_audio_files()
    return final_audio_path


path = generate_audio_files(os.path.join(os.getcwd(), "sample_story.txt"))
print(path)