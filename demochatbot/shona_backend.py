import openai

# Replace with your actual OpenAI API key
openai.api_key = 'Api_Key'

def chat_with_openai(messages, language='Shona'):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("Shona Chatbot. Type your message and press enter. Type 'exit' to end the conversation.")
    conversation_context = [{"role": "system", "content": "You are a helpful assistant that converses in Shona."}]
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        
        conversation_context.append({"role": "user", "content": user_input})
        response = chat_with_openai(conversation_context)

        if response:
            print(f"Chatbot: {response}")
            conversation_context.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
