import streamlit as st
import openai

# OpenAI API key yahan daalein
openai.api_key = ''  # Replace with your OpenAI API key]\

def get_chatbot_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."}, # Optional system message for context
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Something went wrong: {str(e)}"

def main():
    st.title("Chatbot with OpenAI and Streamlit")
    
    # Input text box for user prompt
    user_input = st.text_input("User:", "")
    
    if st.button("Send"):
        if user_input.strip() != "":
            with st.spinner('Thinking...'):
                response = get_chatbot_response(user_input)
            st.write("Chatbot:", response)
        else:
            st.warning("Please enter a message!")

if __name__ == "__main__":
    main()
# openai.api_key = api_key

# def chatbot(prompt):
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=150,
#             n=1,
#             stop=None,
#             temperature=0.7
#         )
#         message = response.choices[0].message.content.strip()
#         return message
#     except Exception as e:
#         return f"Kuch ghalat ho gaya: {str(e)}"

# def main():
#     st.title("Chatbot with OpenAI and Streamlit")
    
#     # Input text box for user prompt
#     user_input = st.text_input("User:", "")
    
#     if st.button("Send"):
#         if user_input.strip() != "":
#             with st.spinner('Sooch raha hai...'):
#                 response = chatbot(user_input)
#             st.write("Chatbot:", response)
#         else:
#             st.warning("Kuch type karein user input mein!")

# if __name__ == "__main__":
#     main()