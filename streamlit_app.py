import streamlit as st
import google.generativeai as genai
import styles
from urllib.parse import quote
import json
import os
from PIL import Image
from rembg import remove

# Define the logo path
LOGO_PATH = "JAKE.png"

# Configure page settings (Favicon & Title)
st.set_page_config(page_title="JAKE Intelligence", page_icon=LOGO_PATH)

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

# Initialize session state for messages if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# Show title and description.
styles.apply_custom_css()

@st.cache_data
def get_logo_image():
    """Loads the logo and removes the background."""
    if os.path.exists(LOGO_PATH):
        try:
            image = Image.open(LOGO_PATH)
            return remove(image)
        except Exception:
            img = Image.open(LOGO_PATH)
            img.load()  # Ensure image data is loaded into memory
            return img
    return None

# --- Authentication Logic ---
if not st.session_state.authenticated:
    # Centered Layout for Login
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Logo on Login Screen
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            st.image(get_logo_image(), width=120)
        st.markdown('<div class="login-header">Welcome to JAKE Intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Please provide your name and mobile number to continue</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            l_mobile = st.text_input("Mobile Number", key="l_mobile", placeholder="Enter your mobile number")
            l_name = st.text_input("Name", key="l_name", placeholder="Enter your name")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Login", use_container_width=True):
                if os.path.exists('users.json'):
                    try:
                        with open('users.json', 'r') as f:
                            users = json.load(f)
                        # Check if mobile exists and name matches
                        if l_mobile in users and users[l_mobile] == l_name:
                            st.session_state.authenticated = True
                            st.session_state.user_name = l_name
                            st.rerun()
                        else:
                            st.error("Invalid credentials or user not found.")
                    except json.JSONDecodeError:
                        st.error("User database is corrupted.")
                else:
                    st.error("No users registered yet.")

        with tab2:
            s_name = st.text_input("Name", key="s_name", placeholder="Choose a display name")
            s_mobile = st.text_input("Mobile Number", key="s_mobile", placeholder="Enter your mobile number")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✨ Sign Up", use_container_width=True):
                if s_name and s_mobile:
                    users = {}
                    if os.path.exists('users.json'):
                        try:
                            with open('users.json', 'r') as f:
                                users = json.load(f)
                        except json.JSONDecodeError:
                            users = {}
                    
                    users[s_mobile] = s_name
                    with open('users.json', 'w') as f:
                        json.dump(users, f)
                    st.success("Account created! Please Login.")
                else:
                    st.warning("Please fill all fields.")
    st.stop()

# Dynamic Greeting Logic
greeting = f"Hello {st.session_state.user_name}" if len(st.session_state.messages) == 0 else f"Hey {st.session_state.user_name}"
st.title(f"{greeting} 👋 💬JAKE")

with st.sidebar:
    st.image(get_logo_image(), width=150)
    st.write(
        f"This is a simple chatbot that uses Google's {MODEL_DISPLAY_NAME} model to generate responses. "
        "To use this app, you need to provide a Gemini API key, which you can get [here](https://makersuite.google.com/app/apikey). "
        "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
    )

    if st.button("Logout", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.user_name = ""
        st.rerun()
    
    # --- Conversation Actions ---
    st.markdown("---")
    st.subheader("📂 Conversation Options")
    
    # Prepare chat text for export
    chat_text = "\n\n".join([f"[{m['role'].upper()}]: {m['content']}" for m in st.session_state.messages])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download Button
        st.download_button(
            label="📥 Download",
            data=chat_text,
            file_name="jake_chat_history.txt",
            mime="text/plain"
        )
    
    with col2:
        # Share Button (Mailto link)
        subject = quote("My Conversation with JAKE")
        body = quote(chat_text)
        st.link_button("📤 Share", f"mailto:?subject={subject}&body={body}")

    # Copy Option (Expandable code block)
    with st.expander("📋 View & Copy Transcript"):
        st.code(chat_text, language="text")
        st.caption("Click the copy icon in the top right of the box above.")

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
