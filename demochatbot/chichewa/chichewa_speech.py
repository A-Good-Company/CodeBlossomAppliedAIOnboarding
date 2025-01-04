import os
import sounddevice as sd
import numpy as np
import whisper
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load Whisper model
model = whisper.load_model('base') 

def record_audio(duration=5, samplerate=16000):
    print("Recording...")
    print(sd.query_devices())
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    print("Recording complete.")
    return np.squeeze(audio_data)

def transcribe_audio(audio_data, samplerate=16000):
    print("Transcribing...")
    # Whisper model expects np.ndarray as input with shape (samples,)
    result = model.transcribe(audio_data, language='en')
    text = result['text']
    print("Transcription complete.")
    return text.strip()

def chatbot(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def main():
    while True:
        print("Press Enter to start recording or type 'exit' to quit:")
        command = input().lower()
        if command == 'exit':
            break

        # Record and transcribe audio
        audio = record_audio()
        transcribed_text = transcribe_audio(audio)

        # Print transcribed text
        print(f"You said: {transcribed_text}")

        # Get response from chatbot
        response = chatbot(transcribed_text)
        print(f"Robot: {response}\n")

if __name__ == "__main__":
    main()