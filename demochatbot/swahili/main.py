"""
Swahili Chat Bot
"""
import streamlit as st

from response_functions import response_generator, translation_generator

st.title('Jambo! Nikusaidieje leo? 🙂')
st.caption('Hello! How can I help you today? 🙂')

# Clear chat history
if st.sidebar.button("New Chat"):
    st.session_state.messages = []

if 'previous_api_key' not in st.session_state:
    st.session_state.previous_api_key = None

current_api_key = st.sidebar.text_input(label='API Key',
                                        placeholder='your-openai-api-key',
                                        key='api_key')

# Check if the API key is being set or changed
if current_api_key and current_api_key != st.session_state.previous_api_key:
    st.toast("API Key saved successfully!", icon="✅")
    # Update the session state to the current API key
    st.session_state.previous_api_key = current_api_key


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

# Accept user input
if prompt := st.chat_input("Say something"):
    # Display user message in chat container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    api_key = st.session_state.api_key
    if not api_key:
        st.toast('Please provide an API key.', icon="🚨")
    else:
        # Generate response
        with st.chat_message("assistant"):
            tab1, tab2= st.tabs(["Swahili", "English"])
            with st.spinner('...'):
                with tab1:
                    # Generate response
                    response = st.write_stream(response_generator(
                        st.session_state.messages, api_key))
                with tab2:
                    st.write_stream(translation_generator(response))

        # Add response to chat history
        st.session_state.messages.append({'role': 'assistant', 'content': response})
