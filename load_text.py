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
    """
    Reads the story file and parses it into a list of tuples containing (index, speaker, speech).
    Returns the list of tuples and the unique speakers.
    """
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    text_list = []
    current_speaker = None
    current_speech_lines = []
    count = 0

    # Updated regex pattern to allow multi-word speakers
    speaker_pattern = re.compile(r'^([\w\s\'-]+):\s*(.*)')  

    for line in lines:
        stripped_line = line.strip()

        # Check if the line starts with a new speaker
        speaker_match = speaker_pattern.match(stripped_line)
        if speaker_match:
            # Save the previous speaker's speech if it exists
            if current_speaker is not None and current_speech_lines:
                speech = ' '.join(current_speech_lines).strip()
                text_list.append((count, current_speaker, speech))
                count += 1

            # Start a new speaker block
            current_speaker = speaker_match.group(1).strip()  # Extract speaker
            speech_text = speaker_match.group(2).strip()  # Extract speech if present

            # If there's speech on the same line, start collecting it
            current_speech_lines = [speech_text] if speech_text else []
        else:
            # Collect speech lines
            current_speech_lines.append(stripped_line)

    # Add the last speaker and their speech if any
    if current_speaker is not None and current_speech_lines:
        speech = ' '.join(current_speech_lines).strip()
        text_list.append((count, current_speaker.lower(), speech))

    # Get unique speakers
    unique_speakers = list(set(speaker for _, speaker, _ in text_list))

    parsed_text_path = os.path.join(cwd, "parsed_text.txt")
    with open(parsed_text_path, "w", encoding="utf-8") as f:
        for line in text_list:
            f.write(f"id_{line[0]}_{line[1]}: speech_start_{line[2]}_speech_end\n\n")
    
    return text_list, unique_speakers

    
