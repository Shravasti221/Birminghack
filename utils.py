import os
import PyPDF2
import re
from groq import Groq
from config import Config
import nltk
import pyaudio
from generator_async_SSE import generate_audio_files
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
from get_voices import get_voices
import pandas as pd

def clean_text(s):
    return re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', s)

def available_voices():
    voices_csv_path = get_voices()
    df_voices = pd.read_csv(voices_csv_path)
    voice_id_list = df_voices["voice_id"].values
    voice_name_list = df_voices["name"]
    return list(zip(voice_id_list, voice_name_list))

def get_characters(text):
    client = Groq(api_key = os.environ.get("GROQ_API_KEY"))    
    clean_text = text.replace("\n", "")
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {"role": "system", "content": "do as directed below and strictly follow the instructions. I need name. DONOT answer in json format. answer in text form."},
            {"role": "user", "content": """"Extract all character names which have a dialogue in the following story and return them in the following format: "'character1': 'gender', 'character2': 'gender', ...". The format has each 'character:gender' pair separated by a "comma". If the gender of the speaker is not explicitly mentioned, mention the gender label as 'inconclusive'. Do not include non-character entities.
Assign unique character name identifiers to each character and ensure that the name identifier is a single word doesn't have any space or word break in it. Use numerals to differentiate between two characters with similar character names, e.g. "stepsister1", "stepsister2". Give answer in text form and don't include any extra information at the beginning or end of response."""+ " The story is as follows: " + clean_text + "\n\n Make sure to follow the format 'character1': 'gender', 'character2': 'gender'."}
        ],
        temperature=0.6,
        max_completion_tokens=50000,
        top_p=1,
        stream=False
    )
    output= completion.choices[0].message.content
    print(output)
    match = re.search(r"</think>\s*", output)
    if match:
        extracted_text = output[match.end():].strip()
        return extracted_text
    else:
        return output

def get_frequent_characters(text, characters):
    appearances = [(char, text.lower().count(char.lower())) for char in characters]
    return [char[0] for char in sorted(appearances, key=lambda x: x[1], reverse=True)[:5]]

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text.strip()

def call_groq_api(text, characters):
    client = Groq(api_key = os.environ.get("GROQ_API_KEY"))    
    clean_text = text.replace("\n", "")
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {"role": "system", "content": f"do as directed below and strictly follow the instructions. DO NOT SUMMARIZE. any text without a speaker must be assigned to the narrator. The following characters are present in the story: {characters}. Assign spoken dialogue to these characters."},
            {"role": "user", "content": """"I am giving you a text. Convert the entire text into a drama skit format with the following structure:  

- Assign spoken dialogue to only those characters which have spoken dialogue in the given story. Use the following format:  
  person1: spoken words (replace with actual words spoken)
  person2: spoken words 
  (Continue for all characters)  

- All background details, descriptions, and text without a speaker must be assigned to the narrator.  
- Do not modify or paraphrase any words. Keep everything exactly as it is.
- Do not add any character which doesn't have any dialogue except the narrator.  
- Do not add scene headings or structure beyond the skit format.  
- Do not explain the speaker’s intent, audience, or actions within the dialogue.  
- Do not include gestures like 'thinking,' 'nodding,' or 'smiling' within character dialogues. Assign such descriptions to the narrator.  
- Do not introduce or summarize the task. Begin directly with the skit format.  
- Start a new line for each change in speaker.  

Strictly follow these constraints without deviation. Output should start immediately in the required format.
\n\n\n"""+clean_text}

        ],
        temperature=0.7,
        max_completion_tokens=100000,
        top_p=1,
        stream=False
    )
    print(f"Following characters have been passed to LLM prompt: {characters}")
    return completion.choices[0].message.content


def extract_and_save_text(input_text, filename="groq_output.txt"):
    match = re.search(r"</think>\s*", input_text)
    if match:
        extracted_text = input_text[match.end():].strip()
        '''with open(filename, "w", encoding="utf-8") as f:
             f.write(extracted_text)'''
        return extracted_text
    else:
        print(f"Could not extract text from input: {input_text}")
        return input_text

def process_voices(file_path, character2voice):
    """
    Processes the text and generates audio files
    Returns the path to the final merged audio file
    """
    print("Process voices utils filepath:", character2voice)
    return generate_audio_files(file_path, character2voice)
