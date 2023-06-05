import openai

# from pydub import AudioSegment

# input_path = "C:/Users/Jacob/Desktop/Whisper Demo App/test.m4a"
# output_path = 'C:/Users/Jacob/Desktop/Whisper Demo App/afterConversion.mp3'
# audio = AudioSegment.from_file(input_path)
# print("here")
# .export(output_path, format="mp3")

API_KEY = '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'
# model_id = 'whisper-1'

audio_file= open("C:/Users/Jacob/Desktop/Whisper Demo App/test.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file, api_key=API_KEY)
print(transcript)

# transcript = 'foop fosby'

# Open the file with write 'w' permission.
file = open("C:/Users/Jacob/Desktop/Whisper Demo App/transcription.txt", 'w')

# Write some data to the file.
file.write(str(transcript))

# Close the file when you're done with it.
file.close()