"""
Chat Bot Functions
"""
import time
from typing import List
import openai
from translate import Translator

def response_generator(active_messages: List, api_key: str):
    """
    Replies to the prompt using OpenAI's GPT-3 engine.
    """
    try:
        # Initialize OpenAI API
        openai.api_key = api_key
        if not active_messages:
            raise ValueError("Please provide a prompt.")

        # Generate response
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a helpful Swahili assistant that expects a prompt in Swahili and answers in Swahili. If you get a prompt in English or any other language that is not Swahili, you should still respond in Swahili"},
                *active_messages,
            ],
            stream=True
        )
        for chunk in response:
            chunk_message = chunk.choices[0].delta.content
            if chunk_message:
                yield chunk_message
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

def translation_generator(message: str):
    """
    Translates a message from Swahili to English.
    """
    translator = Translator(from_lang="sw", to_lang="en")
    translation = translator.translate(message)
    for word in translation.split():
        yield word + " "
        time.sleep(0.05)
