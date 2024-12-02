import os

# Install openai package if not present
try:
    from openai import OpenAI
except ImportError:
    print("Installing openai package...")
    os.system('pip install openai')
    from openai import OpenAI

# OpenAI API key yahan daalein
api_key = ''
client = OpenAI(api_key=api_key)

def chatbot(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        message = response.choices[0].message.content.strip()
        return message
    except Exception as e:
        return f"Kuch ghalat ho gaya: {str(e)}"

def main():
    print("Chatbot se baat karein! Khattam karne ke liye 'bye' likhein.")
    while True:
        user_input = input("Aap: ")
        if user_input.lower() in ['bye', 'exit', 'quit']:
            print("Chatbot: Khuda Hafiz!")
            break
        response = chatbot(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()