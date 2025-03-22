import os
import regex as re

cwd = os.getcwd()
file_path = os.path.join(cwd, "sample_story.txt")

def unique_speakers(text_list):
    speakers = set()
    for line in text_list:
        speakers.add(line[1])
    return list(speakers)

def parse_text(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    text = text.split('\n')
    text = list(filter(lambda x: x!= '', text))

    text_list = []
    pattern = r'(\w+):\s*(.*)'
    count = 0
    for line in text:
        matches = re.findall(pattern, line)
        if matches:
            for speaker, speech in matches:
                text_list.append((count, speaker, speech))
                count += 1
        else:
            continue

    
    return text_list, unique_speakers(text_list)

# xx = parse_text(file_path)
# print(xx[0])
