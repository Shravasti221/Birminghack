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



def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text.strip()

def call_groq_api(text):
    client = Groq(api_key = os.environ.get("GROQ_API_KEY"))    
    clean_text = text.replace("\n", "")
    completion = client.chat.completions.create(
        model="deepseek-r1-distill-llama-70b",
        messages=[
            {"role": "user", "content": "do as directed below and strictly follow the instructions. DO NOT SUMMARIZE. any text without a speaker must be assigned to the narrator."},
            {"role": "system", "content": """"I am giving you a text. Convert the entire text into a drama skit format with the following structure:  

- Assign spoken dialogue to characters in this format:  
  person1: spoken words (replace with actual words spoken)
  person2: spoken words 
  (Continue for all characters)  

- All background details, descriptions, and text without a speaker must be assigned to the narrator.  
- Do not modify or paraphrase any words. Keep everything exactly as it is.  
- Do not add scene headings or structure beyond the skit format.  
- Do not explain the speaker’s intent, audience, or actions within the dialogue.  
- Do not include gestures like 'thinking,' 'nodding,' or 'smiling' within character dialogues. Assign such descriptions to the narrator.  
- Do not introduce or summarize the task. Begin directly with the skit format.  
- Start a new line for each change in speaker.  

Strictly follow these constraints without deviation. Output should start immediately in the required format.
\n\n\n"""+clean_text}

        ],
        temperature=0.6,
        max_completion_tokens=100000,
        top_p=1,
        stream=False
    )
    return completion.choices[0].message.content


def extract_and_save_text(input_text, filename="groq_output.txt"):
    match = re.search(r"</think>\s*\(.*?\)\s*", input_text)
    if match:
        extracted_text = input_text[match.end():].strip()
        '''with open(filename, "w", encoding="utf-8") as f:
             f.write(extracted_text)'''
        return extracted_text
    else:
        print(f"Could not extract text from input: {input_text}")
        return input_text

def process_voices(text):
    """
    Processes the text and generates audio files
    Returns the path to the final merged audio file
    """
    file_path = os.path.join(os.getcwd(), "sample_story.txt")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

    return generate_audio_files(file_path)
