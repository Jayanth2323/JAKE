import streamlit as st
import google.generativeai as genai


# Show title and description.
st.title("💬JAKE")
st.write(
    "This is a simple chatbot that uses Google's Gemini 2.5 Flash model to generate responses. "
    "To use this app, you need to provide a Gemini API key, which you can get [here](https://makersuite.google.com/app/apikey). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their Gemini API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:

    # Configure the Gemini API
    genai.configure(api_key=gemini_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Convert messages to Gemini format
        gemini_messages = []
        for message in st.session_state.messages:
            if message["role"] == "user":
                gemini_messages.append({"role": "user", "parts": [{"text": message["content"]}]})
            elif message["role"] == "assistant":
                gemini_messages.append({"role": "model", "parts": [{"text": message["content"]}]})

        # Generate a response using the Gemini API.
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Generate response
                    response = model.generate_content(
                        gemini_messages,
                        generation_config={
                            "temperature": 0.7,
                            "top_p": 0.8,
                            "top_k": 40,
                        }
                    )
                    
                    # Display the response
                    response_text = response.text
                    st.markdown(response_text)
                    
                    # Store the response in session state
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
                    st.info("Please check your API key and try again.")
