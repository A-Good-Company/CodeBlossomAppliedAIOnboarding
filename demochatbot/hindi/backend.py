import os
from dotenv import load_dotenv
import openai
import json

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def chatbot(prompt):
    """
    OpenAI ke GPT-3 engine ka use karke prompt ka jawab deta hai.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", 
                 "content": "Aap ek helpful Hinglish assistant ho jo Hinglish mein prompt expect karta hai aur JSON format mein jawab deta hai. JSON mein do fields hone chahiye: 'hinglish' for Hinglish response, aur 'translation' for English translation. Agar aapko English ya koi aur language mein prompt milta hai jo Hinglish nahi hai, to aapko Hinglish mein jawab dena chahiye 'hinglish' field mein, aur us language mein translation 'translation' field mein add karna chahiye."},
               {"role": "user", "content": "Hello kya haal?"},
                {"role": "assistant", "content": '{"hinglish": "Hello! Main theek hoon, aap batao kya haal hai?", "translation": "Hello! I\'m fine, how are you?", "speaker_language": "Hinglish"}'},
               {"role": "user", "content": "What is your name"},
                {"role": "assistant","content" : '{"hinglish": "Mera naam Assistant hai.", "translation": "My name is Assistant.", "speaker_language": "English"}'},
                {"role": "user", "content": "What languages can you speak?"},
                {"role": "assistant","content" : '{"hinglish": "Main Hinglish aur English mein baat kar sakta hoon.", "translation": "I can speak in Hinglish and English.", "speaker_language": "English"}'},
                {"role": "user", "content": "Can you talk in Chichewa?"},
                {"role": "assistant","content" : '{"hinglish": "Haan main Chichewa mein baat kar sakti hoon.", "translation": "Yes, I can talk in Chichewa", "speaker_language": "English"}'},
                {"role": "user", "content": prompt},
            ]
        )
        message = response.choices[0].message.content
        
        # Try to parse the message as JSON
        try:
            parsed_message = json.loads(message)
            # Ensure the required fields are present
            if 'hinglish' not in parsed_message or 'translation' not in parsed_message:
                raise ValueError("Missing required fields in JSON response")
            return parsed_message
        except json.JSONDecodeError:
            # If parsing fails, create a JSON object with an error message
            return {
                "hinglish": f"Maaf kijiye, JSON format mein jawab nahi mil paya. Yeh mila: {message}",
                "translation": f"Sorry, couldn't get a response in JSON format. This was received: {message}"
            }
    except Exception as e:
        # Return a JSON object with an error message
        return {
            "hinglish": f"Error ho gaya: {str(e)}",
            "translation": f"An error occurred: {str(e)}"
        }

def main():
    print("Robot: Neeche apna sawal type karo. 'Alvida', 'Band karo', ya 'Bye' type karo chat khatam karne ke liye.\n[Translation] Type your question below. Type 'Bye', 'Quit', or 'Exit' to end the chat.")
    while True:
        user_input = input("Aap: ")
        if user_input.lower() in ['bye', 'quit', 'exit', 'alvida', 'band karo']:
            print("Robot: Alvida!\n[Translation] Goodbye!")
            break
        response = chatbot(user_input)
        print(f"Response: {response}")


if __name__ == "__main__":
    main()