import streamlit as st
import google.generativeai as genai


# Model fallback list - prioritized by availability based on user's rate limits
# gemini-2.5-flash-lite: 1/10 RPM (most available)
# gemini-3-flash: 0/5 RPM (completely available)  
# gemini-2.5-flash: 4/5 RPM (almost exhausted)
GEMINI_MODELS = [
    "gemini-2.5-flash-lite",  # Highest capacity
    "gemini-3-flash",          # Completely available
    "gemini-2.5-flash",        # Almost exhausted
    "gemini-2.0-flash-exp", 
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
]

# Get the primary model name for display
PRIMARY_MODEL = GEMINI_MODELS[0]
MODEL_DISPLAY_NAME = PRIMARY_MODEL.replace("-", " ").title().replace(" ", " ").replace("Flash", "Flash ").replace("Exp", "Exp").strip()

# Show title and description.
st.title("💬JAKE")
st.write(
    f"This is a simple chatbot that uses Google's {MODEL_DISPLAY_NAME} model to generate responses. "
    "To use this app, you need to provide a Gemini API key, which you can get [here](https://makersuite.google.com/app/apikey). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Access the Gemini API key from Streamlit secrets
try:
    gemini_api_key = st.secrets["JAKEAPI"]
    # Configure the Gemini API
    genai.configure(api_key=gemini_api_key)
except KeyError:
    st.error("JAKEAPI secret not found. Please ensure it's configured in your Streamlit secrets.")
    st.stop()

def is_rate_limit_error(exception):
    """Check if the exception is a rate limit error."""
    error_str = str(exception).lower()
    rate_limit_indicators = [
        "rate limit",
        "429",
        "resource exhausted",
        "quota exceeded",
        "too many requests"
    ]
    return any(indicator in error_str for indicator in rate_limit_indicators)

def generate_response_with_fallback(messages, generation_config):
    """Try to generate response with fallback models if rate limit is exceeded."""
    last_error = None
    
    for model_name in GEMINI_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                messages,
                generation_config=generation_config
            )
            
            # If we used a fallback model, show which one
            if model_name != GEMINI_MODELS[0]:
                st.toast(f"Switched to {model_name} due to rate limit", icon="⚠️")
            
            return response, model_name
            
        except Exception as e:
            last_error = e
            if is_rate_limit_error(e):
                continue  # Try next model
            else:
                # Other error, don't try fallback models
                raise e
    
    # All models failed
    raise last_error

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

    # Generation config
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40,
    }
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Generate response with automatic fallback
                response, model_used = generate_response_with_fallback(
                    gemini_messages, 
                    generation_config
                )
                
                # Display the response
                response_text = response.text
                st.markdown(response_text)
                
                # Store the response in session state
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
                st.info("Please check your API key and try again.")
