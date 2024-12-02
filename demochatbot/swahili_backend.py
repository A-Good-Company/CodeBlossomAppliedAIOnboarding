import openai


def chatbot(prompt):
    """
    Replies to the prompt using OpenAI's GPT-3 engine.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", 
                 "content": "You are a helpful Swahili assistant that expects a prompt in Swahili and answers in Swahili and adds a translation in English a line below it. If you get a prompt in English or any other language that is not Swahili, you should respond in Swahili and add a translation in the prompted language a line below it in the format [Translation] ..."},
                {"role": "user", "content": prompt},
            ]
        )
        message = response.choices[0].message.content
        return message
    except Exception as e:
        return f"Error occurred: {str(e)}"

def main():
    print("Roboti: Uliza swali lako hapo chini. Andika 'Kwaheri', 'Mwisho' ili kutimiza mazungumzo.\n[Translation] Type your question below. Type 'Bye', 'Quit', or 'Exit' to end the chat.")
    while True:
        user_input = input("Wewe: ")
        if user_input.lower() in ['bye', 'quit', 'exit', 'kwaheri']:
            print("Roboti: Kwaheri!\n[Translation] Goodbye!")
            break
        response = chatbot(user_input)
        print(f"Roboti: {response}", flush=True)

main()
