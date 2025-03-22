import os
import PyPDF2
import wave
import re
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
    clean_text = text.replace("\n", "")
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Process this text and summarize."},
            {"role": "user", "content": """Task: how many characters are there in the story who speak or have a dialogue? list them in the form (character1, character2...,charactern) 
Also restructure the entire text to the form of a drama skit. (like in the format given below):
person1 (whoever it is):
person2 (whoever it is):
and so on for n characters. Assign all background details and text with no speakers to the narrator. don't modify words or any other details and donot include headings like scene 1, 2 etc. or explain who the speaker is talking to, unless explicitly mentioned in the text itself.
also answer to the point. don't introduce the answer or ask if further assistance is needed at the end. Just stick to the point. (MAKE SURE THAT YOU STICK TO THESE INSTRUCTIONS. I DON'T NEED ANY EXTRA INFORMATION. DON'T EXPLAIN BACK THE TASK TO ME AGAIN,OR PUT HEADINGS FOR THE TWO TASKS) also donot put gestures like 'thinking', 'nodding', 'smiling' to character dialogues. assign such things to narrator. only assign spoken words to character
as explained above, THE OUTPUT SHOULD START WITH:

(character1, character2,...charactern)\n\n\n"""+clean_text}

        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False
    )
    return completion.choices[0].message.content

def extract_and_save_text(input_text, filename="groq_output.txt"):
    match = re.search(r"</think>\s*\(.*?\)\s*", input_text)
    if match:
        extracted_text = input_text[match.end():].strip()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(extracted_text)
        return filename
    return None


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
