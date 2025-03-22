import os
import PyPDF2
import wave
import numpy as np
from groq import Groq
from config import Config

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text.strip()


def call_groq_api(text):
    client = Groq(api_key = os.environ.get("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Process this text and summarize."},
            {"role": "user", "content": text}
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )
    return completion.choices[0].message.content

def process_voices(text):
    
    
    
    
    # sample_rate = 44100
    # duration = len(text) // 10  # Approximate duration
    # amplitude = 16000
    # audio_data = (np.sin(2.0 * np.pi * np.arange(sample_rate * duration) * 440.0 / sample_rate) * amplitude).astype(np.int16)

    # filename = "output.wav"
    # wav_path = os.path.join(Config.AUDIO_FOLDER, filename)

    # with wave.open(wav_path, "w") as wf:
    #     wf.setnchannels(1)
    #     wf.setsampwidth(2)
    #     wf.setframerate(sample_rate)
    #     wf.writeframes(audio_data.tobytes())

    return filename
