import openai
import os
from pydub import AudioSegment
import math

def transcribe_file(audio_path, api_key):
    # Set up model_id
    model_id = 'whisper-1'

    # Get the directory of the audio file
    audio_directory = os.path.dirname(audio_path)

    # Directory for transcriptions
    transcriptions_directory = os.path.join(audio_directory, 'Transcriptions')

    # Check if Transcriptions directory exists, if not create it
    if not os.path.exists(transcriptions_directory):
        os.makedirs(transcriptions_directory)

    # Load the audio file
    audio = AudioSegment.from_file(audio_path)

    # Convert the file to .mp3
    mp3_path = audio_path.rsplit(".", 1)[0] + ".mp3"
    audio.export(mp3_path, format="mp3")

    try:
        # Determine the number of chunks for the audio file
        audio_file_size = os.path.getsize(mp3_path)
        num_chunks = math.ceil(audio_file_size / (25 * 1024 * 1024))  # 25MB chunks

        # Split audio file into smaller chunks if it exceeds 25MB
        chunk_length = int(len(audio) / num_chunks)
        chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]

        # Transcribe each chunk
        transcripts = []
        for i, chunk in enumerate(chunks):
            chunk.export("chunk.mp3", format="mp3")
            with open("chunk.mp3", "rb") as chunk_file:
                transcript = openai.Audio.transcribe(model_id, chunk_file, api_key=api_key)
            transcripts.append(transcript)

        # Output filename
        output_filename = os.path.join(transcriptions_directory, os.path.basename(audio_path).rsplit(".", 1)[0] + ".txt")

        # Write the transcription to the output file
        with open(output_filename, 'w') as file:
            for transcript in transcripts:
                file.write(str(transcript) + '\n')

    except openai.error.APIConnectionError as e:
        raise e

    finally:
        # Remove temporary .mp3 files
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
        if os.path.exists("chunk.mp3"):
            os.remove("chunk.mp3")