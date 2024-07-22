import openai
import os
from pydub import AudioSegment
import math

# Set up model_id
model_id = 'whisper-1'

# Directory where script is running
current_directory = os.getcwd()

# Directory for transcriptions
transcriptions_directory = os.path.join(current_directory, 'Transcriptions')

# Check if Transcriptions directory exists, if not create it
if not os.path.exists(transcriptions_directory):
    os.makedirs(transcriptions_directory)

# File to store the API key
api_key_file = 'api_key.txt'

# Check if the API key file exists
if os.path.exists(api_key_file):
    # Read the API key from the file
    with open(api_key_file, 'r') as file:
        API_KEY = file.read().strip()
else:
    # Prompt the user for the API key
    API_KEY = input("Please enter your OpenAI API key: ")
    
    # Save the API key to the file
    with open(api_key_file, 'w') as file:
        file.write(API_KEY)

# Look for all audio files in the directory the script is run from
for filename in os.listdir(current_directory):
    if filename.endswith(('.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a')):
        print("Importing " + str(filename))
        audio_path = os.path.join(current_directory, filename)
        
        # Load the audio file
        audio = AudioSegment.from_file(audio_path)
        
        # Convert the file to .mp3
        print("Converting current file to .mp3")
        mp3_path = audio_path.rsplit(".", 1)[0] + ".mp3"
        audio.export(mp3_path, format="mp3")
        
        # Determine the number of chunks for the audio file
        audio_file_size = os.path.getsize(mp3_path)
        num_chunks = math.ceil(audio_file_size / (25 * 1024 * 1024))  # 25MB chunks
        
        # Split audio file into smaller chunks if it exceeds 25MB
        print("splitting into smaller chunks now")
        chunk_length = int(len(audio) / num_chunks)
        # chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]

        chunk_starts = [i*chunk_length for i in range(num_chunks)]
        chunk_ends = chunk_starts[1:] + [len(audio)]  # Use the length of the audio as the end for the last chunk

        chunks = [audio[start:end] for start, end in zip(chunk_starts, chunk_ends)]


        # Transcribe each chunk
        print("transcribe each chunk")
        transcripts = []
        for i, chunk in enumerate(chunks):
            print("Transcribing chunk "+ str(i+1) + "/" + str(len(chunks)))
            chunk.export("chunk.mp3", format="mp3")
            with open("chunk.mp3", "rb") as chunk_file:
                transcript = openai.Audio.transcribe(model_id, chunk_file, api_key=API_KEY)
            transcripts.append(transcript)
        
        # Output filename
        output_filename = os.path.join(transcriptions_directory, filename.rsplit(".", 1)[0] + ".txt")
        
        # Write the transcription to the output file
        with open(output_filename, 'w') as file:
            for transcript in transcripts:
                file.write(str(transcript) + '\n')
        
        # Remove temporary .mp3 files
        os.remove(mp3_path)
        os.remove("chunk.mp3")
        print()

print("All Files Processed")
input("press enter to continue")