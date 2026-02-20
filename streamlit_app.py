import streamlit as st
from google import genai
from google.genai import types
import styles
import json
import os
from PIL import Image

try:
    from rembg import remove
except ImportError:
    remove = None

LOGO_PATH = "logo.png"

# Must be the very first Streamlit command
st.set_page_config(
    page_title="JAKE Intelligence",
    page_icon=LOGO_PATH,
    layout="centered",
    initial_sidebar_state="expanded",
)

GEMINI_MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-3-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
]

PRIMARY_MODEL = GEMINI_MODELS[0]
MODEL_DISPLAY_NAME = (
    PRIMARY_MODEL.replace("-", " ")
    .title()
    .replace(" ", " ")
    .replace("Flash", "Flash ")
    .replace("Exp", "Exp")
    .strip()
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# Apply CSS immediately
styles.apply_custom_css()


def load_users():
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r") as f:
                users = json.load(f)
                if not isinstance(users, dict):
                    return {}
                return users
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)


@st.cache_data(show_spinner=False)
def get_logo_image():
    if not os.path.exists(LOGO_PATH):
        return None
    try:
        original_image = Image.open(LOGO_PATH)
        original_image.load()
    except Exception:
        return None
    if not remove:
        return original_image
    try:
        image_no_bg = remove(original_image)
        bbox = image_no_bg.getbbox()
        if bbox:
            return image_no_bg.crop(bbox)
        return image_no_bg
    except Exception:
        return original_image


# --- Authentication Screen ---
if not st.session_state.authenticated:
    # Use empty containers for vertical centering
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        with st.container():
            # Header Section
            c1, c2, c3 = st.columns([1, 1, 1])
            with c2:
                logo = get_logo_image()
                if logo:
                    st.image(logo, use_container_width=True)

            st.markdown(
                '<div class="login-header">JAKE Intelligence</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="login-sub">Welcome back. Please sign in to continue.</div>',
                unsafe_allow_html=True,
            )

            tab1, tab2 = st.tabs(["Login", "Sign Up"])

            with tab1:
                st.markdown("<br>", unsafe_allow_html=True)
                l_mobile = st.text_input(
                    "Mobile Number",
                    key="l_mobile",
                    placeholder="Enter your registered number",
                ).strip()
                l_name = st.text_input(
                    "Name", key="l_name", placeholder="Enter your name"
                ).strip()
                st.markdown("<br>", unsafe_allow_html=True)

                if st.button("🚀 Log In", use_container_width=True, key="login_btn"):
                    users = load_users()
                    if not users:
                        st.error("No users registered yet. Please Sign Up first.")
                    elif (
                        l_mobile in users and users[l_mobile].lower() == l_name.lower()
                    ):
                        st.session_state.authenticated = True
                        st.session_state.user_name = users[l_mobile]
                        st.rerun()
                    else:
                        st.error(
                            "Invalid credentials. Please check your name and number."
                        )

            with tab2:
                st.markdown("<br>", unsafe_allow_html=True)
                s_name = st.text_input(
                    "Name", key="s_name", placeholder="Choose a display name"
                ).strip()
                s_mobile = st.text_input(
                    "Mobile Number",
                    key="s_mobile",
                    placeholder="Enter your mobile number",
                ).strip()
                st.markdown("<br>", unsafe_allow_html=True)

                if st.button(
                    "✨ Create Account", use_container_width=True, key="signup_btn"
                ):
                    if s_name and s_mobile:
                        users = load_users()
                        if s_mobile in users:
                            st.warning(
                                "This mobile number is already registered. Please switch to Login."
                            )
                        else:
                            users[s_mobile] = s_name
                            save_users(users)
                            st.success(
                                "Account created successfully! You can now log in."
                            )
                    else:
                        st.warning("Please fill in both fields to continue.")
    # Halt execution here if not logged in
    st.stop()

# --- Main Application Interface ---

# Sidebar Configuration
with st.sidebar:
    logo = get_logo_image()
    if logo:
        st.image(logo, width=120)

    st.markdown("### About JAKE")
    st.write(
        f"This intelligence interface runs on Google's advanced **{MODEL_DISPLAY_NAME}** model."
    )

    st.markdown("---")

    # Action buttons stacked neatly
    if st.button("🔄 Clear Cache", use_container_width=True):
        st.cache_data.clear()
        st.success("Memory cache cleared!")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True, type="primary"):
        st.session_state.authenticated = False
        st.session_state.user_name = ""
        st.rerun()

# Main Chat Header
greeting = "Hello" if len(st.session_state.messages) == 0 else "Welcome back,"
st.title(f"{greeting} {st.session_state.user_name} 👋")
st.markdown("*How can JAKE assist you today?*")
st.markdown("---")

# API Configuration
try:
    gemini_api_key = st.secrets["JAKEAPI"]
    client = genai.Client(api_key=gemini_api_key)
except KeyError:
    st.error("⚠️ API Setup Required: JAKEAPI secret not found in Streamlit settings.")
    st.stop()


def is_rate_limit_error(exception):
    error_str = str(exception).lower()
    return any(
        ind in error_str
        for ind in [
            "rate limit",
            "429",
            "resource exhausted",
            "quota exceeded",
            "too many requests",
            "404",
        ]
    )


def generate_response_with_fallback(client_instance, current_messages):
    last_error = None
    for model_name in GEMINI_MODELS:
        try:
            response_stream = client_instance.models.generate_content_stream(
                model=model_name,
                contents=current_messages,
                config=types.GenerateContentConfig(
                    system_instruction="You are Jake, a highly capable, articulate, and intelligent AI assistant.",
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                ),
            )
            if model_name != GEMINI_MODELS[0]:
                st.toast(f"Traffic high. Switched to {model_name}", icon="🔄")
            return response_stream, model_name
        except Exception as e:
            last_error = e
            if is_rate_limit_error(e):
                continue
            else:
                raise e
    raise last_error


# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input & Logic
if prompt := st.chat_input("Message JAKE..."):
    # Append and display user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert to Gemini format
    gemini_messages = []
    for message in st.session_state.messages:
        role = "user" if message["role"] == "user" else "model"
        gemini_messages.append(
            types.Content(
                role=role, parts=[types.Part.from_text(text=message["content"])]
            )
        )

    # Generate and stream response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            response_stream, model_used = generate_response_with_fallback(
                client, gemini_messages
            )
            for chunk in response_stream:
                try:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                except ValueError:
                    continue

            message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:
            st.error("Connection interrupted.")
            st.info(f"System details: {str(e)}")
