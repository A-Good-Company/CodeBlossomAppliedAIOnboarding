import os
from dotenv import load_dotenv
import openai
import json

# Kwezani makonzedwe a chilengedwe kuchokera pa .env fayilo
load_dotenv()

# Pezani chitumbiko cha API kuchokera mu variable ya chilengedwe
openai.api_key = os.getenv("OPENAI_API_KEY")

def chatbot(prompt):
    """
    Kuyankhula kwapoyakwamba kupereka yankho la prompt pogwiritsa ntchito injini ya GPT-3 ya OpenAI.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", 
                 "content": "Ndinu wothandizira wa Chingerezi amene amayembekeza ma funso mu Chichewa ndipo akuyankha mu JSON. JSON iyenera kuchita bwino ndi zina ziwiri: 'chichewa' pamayankho a Chichewa ndipo 'translation' pamayankho mu Chingerezi. Ngati mukulandira mu Chingerezi kapena chinenero china, muyenera koyamba kudzifotokoza mu 'chichewa', kenako mumasulira mawanga tina mu 'translation'."},
                {"role": "user", "content": "Muli bwanji?"},
                {"role": "assistant", "content": '{"chichewa": "Ndili bwino kaya, inu muli bwanji?", "translation": "I am doing great, how are you doing?"}'},
                {"role": "user", "content": "Dzina lanu ndindani"},
                {"role": "assistant","content" : '{"chichewa": "Dzina langa ndi Assistant.", "translation": "My name is Assistant."}'},
                {"role": "user", "content": "Kodi mutha kulankhula zinenero ziti?"},
                {"role": "assistant","content" : '{"chichewa": "Ndingathe kulankhula Chichewa ndi Chingerezi.", "translation": "I can speak Chichewa and English."}'},
                {"role": "user", "content": "Kodi mutha kulankhula chichewa?"},
          
                {"role": "user", "content": prompt},
            ]
        )
        message = response.choices[0].message.content
        
        # Yesani kutanthauzira uthenga monga JSON
        try:
            parsed_message = json.loads(message)
            # Onetsetsani kuti zigawo zofunikira zilipo
            if 'chichewa' not in parsed_message or 'translation' not in parsed_message:
                raise ValueError("Zigawo zofunikira zasoweka mu JSON yanthawuzi")
            return parsed_message
        except json.JSONDecodeError:
            # Ngati kulephera kutanthauzira, pangani JSON ndi uthenga wa cholakwika
            return {
                "chichewa": f"Pepa, sindinathe kuwapeza mu kulepera kwabwino kwa JSON. Izi zamveka: {message}",
                "translation": f"Sorry, couldn't get a response in valid JSON format. Received: {message}"
            }
    except Exception as e:
        # Perekani JSON yokhala ndi uthenga wa cholakwika
        return {
            "chichewa": f"Cholakwika chachitika: {str(e)}",
            "translation": f"An error occurred: {str(e)}"
        }

def main():
    print("Robot: Lembani funso lanu pansipa. Lembani 'Siya', 'Tulani', kapena 'Kutha' kuti muyimbitse kuyankhula.\n[Translation] Type your question below. Type 'Bye', 'Quit', or 'Exit' to end the chat.")
    while True:
        user_input = input("Inu: ")
        if user_input.lower() in ['bye', 'quit', 'exit', 'siya', 'tulani']:
            print("Robot: Alamu!\n[Translation] Goodbye!")
            break
        response = chatbot(user_input)
        print(f"Response: {response}")


if __name__ == "__main__":
    main()