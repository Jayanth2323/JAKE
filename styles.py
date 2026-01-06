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

            /* Chat Input specific styling */
            [data-testid="stChatInput"] {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: all 0.3s ease;
            }

            [data-testid="stChatInput"] textarea {
                background-color: transparent !important;
                color: white !important;
                border: none !important;
            }

            /* 4.1 Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(20px);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }

            /* 4.2 Sidebar Action Buttons */
            .stDownloadButton button, .stLinkButton a, .stButton button {
                width: 100%;
                border-radius: 15px !important;
                background: linear-gradient(90deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
                border: 1px solid rgba(255,255,255,0.2);
                color: white !important;
                transition: all 0.3s ease;
            }
            
            .stDownloadButton button:hover, .stLinkButton a:hover {
                background: linear-gradient(90deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }

            /* 3.2 Animated Buttons */
            /* Specific override for primary buttons if needed, otherwise generic above works */
            div[data-testid="stChatInput"] + button {
                background: linear-gradient(45deg, #FF512F, #DD2476);
                color: white;
                border: none;
                border-radius: 25px;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            /* 5.1 Custom Tabs for Login */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: rgba(255, 255, 255, 0.05);
                padding: 10px 10px 0 10px;
                border-radius: 15px;
                border-bottom: none;
            }

            .stTabs [data-baseweb="tab"] {
                height: 50px;
                border-radius: 10px;
                color: rgba(255, 255, 255, 0.6);
                font-weight: 600;
                transition: all 0.3s ease;
                border: none !important;
                flex: 1;
            }

            .stTabs [aria-selected="true"] {
                background-color: rgba(255, 255, 255, 0.2) !important;
                color: white !important;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            /* 5.2 Login Screen Typography */
            .login-header {
                font-size: 2.5rem !important;
                font-weight: 800 !important;
                text-align: center;
                background: linear-gradient(120deg, #ffffff, #84fab0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
                padding-bottom: 10px;
            }
            
            .login-sub {
                text-align: center;
                color: rgba(255,255,255,0.8);
                font-size: 1.1rem;
                margin-bottom: 2rem;
                font-weight: 400;
            }
        </style>
    """, unsafe_allow_html=True)