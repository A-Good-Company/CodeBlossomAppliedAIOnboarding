import os
import sounddevice as sd
import numpy as np
import whisper
import openai
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load Whisper model
model = whisper.load_model('base') 

def record_audio(duration=5, samplerate=16000):
    print("Recording...")
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
    # Construct the full conversation prompt with a three-shot example
    full_prompt = (
        "You are a chatbot that understands Chichewa and English. Answer in JSON format "
        "with 'chichewa' for the response in Chichewa and 'translation' for the English translation.\n\n"
        "User: Muli bwanji?\n"
        "Assistant: {\"chichewa\": \"Ndili bwino kaya, inu muli bwanji?\", \"translation\": \"I am doing great, how are you doing?\"}\n\n"
        "User: Dzina lanu ndindani?\n"
        "Assistant: {\"chichewa\": \"Dzina langa ndi Assistant.\", \"translation\": \"My name is Assistant.\"}\n\n"
        "User: Kodi mutha kulankhula zinenero ziti?\n"
        "Assistant: {\"chichewa\": \"Ndingathe kulankhula Chichewa ndi Chingerezi.\", \"translation\": \"I can speak Chichewa and English.\"}\n\n"
        f"User: {prompt}\n"
        "Assistant:"
    )
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=150,
        n=1,
        stop=["User:"],
        temperature=0.7
    )
    
    # Try parsing the response to JSON
    try:
        message = response.choices[0].text.strip()
        parsed_message = json.loads(message)
        # Ensure required keys are present
        if 'chichewa' not in parsed_message or 'translation' not in parsed_message:
            raise ValueError("Missing required keys in JSON response")
        return parsed_message
    except (json.JSONDecodeError, ValueError) as e:
        # Handle errors in JSON parsing
        return {
            "chichewa": f"Cholakwika chachitika: {str(e)}",
            "translation": f"An error occurred: {str(e)}"
        }

def main():
    while True:
        print("Type 'record' to use voice input or 'type' to enter your question manually. Type 'exit' to quit.")
        method = input("Choose input method: ").lower()

        if method == 'exit':
            print("Goodbye!")
            break
        elif method == 'record':
            # Record and transcribe audio
            audio = record_audio()
            transcribed_text = transcribe_audio(audio)
        elif method == 'type':
            transcribed_text = input("Enter your question: ")

        # Skip to the next loop iteration if no valid transcribed text
        if not transcribed_text:
            continue

        # Print the transcribed text if recorded
        print(f"You said: {transcribed_text}")

        # Get response from chatbot
        response = chatbot(transcribed_text)
        print(f"Response: {response}\n")

if __name__ == "__main__":
    main()