from pydub import AudioSegment
import os

def merge_audio_files():
    """
    Merges all the audio files in the output_audio folder into a single file
    Returns the path to the merged audio file
    """
    cwd = os.getcwd()

    # Directory containing the audio files
    audio_folder = os.path.join(cwd, "output_audio")

    # Output filename
    output_file = "final_merged_output.wav"

    # List all audio files in the folder (sorted if necessary)
    audio_files = sorted([f for f in os.listdir(audio_folder) if f.endswith('.wav')])

    # Start with an empty audio segment
    merged_audio = AudioSegment.empty()

    # Loop through files and append them
    for file_name in audio_files:
        file_path = os.path.join(audio_folder, file_name)
        # print(f"Adding {file_name} to merged audio")
        
        # Load the current audio file
        audio = AudioSegment.from_wav(file_path)
        
        # Append to the merged audio
        merged_audio += audio

    # Export the final merged audio
    output_audio_path = os.path.join(cwd, output_file)
    merged_audio.export(output_audio_path, format="wav")

    print(f"Successfully merged {len(audio_files)} files into {output_file}")
    return output_audio_path
