import os
from dotenv import load_dotenv
from pyneuphonic import Neuphonic, TTSConfig
from pyneuphonic.player import AudioPlayer

cwd = os.getcwd()
load_dotenv(dotenv_path=os.path.join(cwd, ".env"))

# Load the API key from the environment
client = Neuphonic(api_key=os.environ.get('NEUPHONIC_API_KEY'))

sse = client.tts.SSEClient()

# TTSConfig is a pydantic model so check out the source code for all valid options
tts_config = TTSConfig(
    speed=1.05,
    lang_code='en', # replace the lang_code with the desired language code.
    voice_id='e564ba7e-aa8d-46a2-96a8-8dffedade48f'  # use client.voices.list() to view all available voices
)

# Create an audio player with `pyaudio`
with AudioPlayer() as player:
    response = sse.send('Hello, world! this is an ai developed voice chatbot', tts_config=tts_config)
    player.play(response)

    player.save_audio('output_1.wav')  # save the audio to a .wav file