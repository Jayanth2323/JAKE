import streamlit as st

def apply_custom_css():
    """
    Applies modern UI styles including:
    - Animated gradient background
    - Glassmorphism effects for chat and sidebar
    - Custom typography and animations
    """
    st.markdown("""
        <style>
            /* Import modern font */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
            }

            /* 1.2 Animated Gradient Background */
            .stApp {
                background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
            }

            @keyframes gradient {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* 1.3 Gradient Title */
            h1 {
                font-weight: 800 !important;
                background: linear-gradient(to right, #ffffff, #e0e0e0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
                animation: fadeInDown 0.8s ease-out;
            }

            @keyframes fadeInDown {
                from { opacity: 0; transform: translate3d(0, -20px, 0); }
                to { opacity: 1; transform: translate3d(0, 0, 0); }
            }

            /* 2.2 Glassmorphism for Chat Messages */
            [data-testid="stChatMessage"] {
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 1rem;
                margin-bottom: 1rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            [data-testid="stChatMessage"]:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
            }

            /* 3.1 Enhanced Chat Input */
            .stTextInput > div > div > input {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 25px;
                padding: 10px 20px;
                transition: all 0.3s ease;
            }

            .stTextInput > div > div > input:focus {
                background-color: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.5);
                box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
            }

            /* 4.1 Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(20px);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }

            /* 3.2 Animated Buttons */
            .stButton button {
                background: linear-gradient(45deg, #FF512F, #DD2476);
                color: white;
                border: none;
                border-radius: 25px;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
        </style>
    """, unsafe_allow_html=True)