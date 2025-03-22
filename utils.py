import os
import PyPDF2
import wave
import numpy as np
from groq import Groq
from config import Config
from generate_audio_files import generate_audio_files

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
    """
    Processes the text and generates audio files
    Returns the path to the final merged audio file
    """
    return generate_audio_files(text)