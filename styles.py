import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

            /* Base Typography */
            html, body, [class*="css"], .stMarkdown p {
                font-family: 'Inter', sans-serif !important;
                color: #ffffff;
            }

            /* 1. Animated Gradient Background */
            .stApp {
                background: linear-gradient(-45deg, #1A2980, #26D0CE, #ee7752, #e73c7e);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
            }

            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            /* Hide Streamlit Header/Footer for clean look */
            # header {visibility: hidden;}
            # footer {visibility: hidden;}

            /* 2. Login Card Container */
            /* Using a more resilient selector for the main card container */
            [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
                background: rgba(255, 255, 255, 0.05); 
                backdrop-filter: blur(25px);
                -webkit-backdrop-filter: blur(25px);
                padding: 3rem 2.5rem;
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            }

            /* 3. Typography inside Login Card */
            .login-header {
                font-size: 2.2rem !important;
                font-weight: 700 !important;
                text-align: center;
                color: #ffffff;
                text-shadow: 0 4px 10px rgba(0,0,0,0.3);
                margin-bottom: 0.5rem;
                letter-spacing: -0.5px;
            }
            
            .login-sub {
                text-align: center;
                color: rgba(255,255,255,0.7);
                font-size: 1.05rem;
                font-weight: 300;
                margin-bottom: 2rem;
            }

            /* 4. Tabs styling */
            .stTabs [data-baseweb="tab-list"] {
                background-color: transparent !important;
                gap: 24px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
                padding-bottom: 5px !important;
            }

            .stTabs [data-baseweb="tab"] {
                background-color: transparent !important;
                border: none !important;
                color: rgba(255, 255, 255, 0.5) !important;
                font-weight: 500;
                font-size: 1.1rem;
                padding: 10px 0 !important;
                transition: color 0.3s ease;
            }

            .stTabs [data-baseweb="tab"]:hover {
                color: rgba(255, 255, 255, 0.8) !important;
            }

            .stTabs [aria-selected="true"] {
                color: #ffffff !important;
                font-weight: 600;
                border-bottom: 2px solid #ffffff !important;
                background-color: transparent !important;
            }

            /* 5. Input Fields */
            .stTextInput label {
                color: rgba(255, 255, 255, 0.8) !important;
                font-weight: 500 !important;
                padding-bottom: 5px;
            }

            .stTextInput > div > div > input {
                background-color: rgba(0, 0, 0, 0.2) !important;
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 12px;
                padding: 14px 20px;
                font-size: 1rem;
                transition: all 0.3s ease;
            }
            
            .stTextInput > div > div > input:focus {
                background-color: rgba(0, 0, 0, 0.4) !important;
                border-color: rgba(255, 255, 255, 0.5) !important;
                box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
            }

            /* Placeholder text */
            input::placeholder {
                color: rgba(255, 255, 255, 0.3) !important;
            }

            /* 6. Buttons */
            .stButton > button {
                background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                color: #ffffff !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                font-size: 1.05rem !important;
                padding: 12px 24px !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                backdrop-filter: blur(10px);
            }

            .stButton > button:hover {
                background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%) !important;
                border-color: rgba(255, 255, 255, 0.4) !important;
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            }

            .stButton > button:active {
                transform: translateY(1px);
            }

            /* 7. Chat Interface */
            /* User Message Bubble */
            [data-testid="stChatMessage"][data-testid*="user"] {
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px 20px 0px 20px;
                padding: 1.2rem;
                margin: 1rem 0 1rem auto;
                max-width: 85%;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }

            /* AI Message Bubble */
            [data-testid="stChatMessage"][data-testid*="assistant"] {
                background: rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px 20px 20px 0px;
                padding: 1.2rem;
                margin: 1rem auto 1rem 0;
                max-width: 85%;
            }

            /* Chat Input Area */
            [data-testid="stChatInput"] {
                background-color: rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(15px);
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                padding: 5px;
            }
            
            [data-testid="stChatInput"] textarea {
                color: #ffffff !important;
                font-size: 1rem;
            }
            
            [data-testid="stChatInput"] button {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
            }

            /* 8. Sidebar */
            [data-testid="stSidebar"] {
                background-color: rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(25px);
                -webkit-backdrop-filter: blur(25px);
                border-right: 1px solid rgba(255, 255, 255, 0.05);
            }
            
            [data-testid="stSidebar"] .stMarkdown p {
                color: rgba(255, 255, 255, 0.8);
                font-size: 0.95rem;
                line-height: 1.5;
            }

            /* 9. Animations */
            /* Smooth Logo Float */
            img[src*="logo.png"] {
                animation: softFloat 6s ease-in-out infinite;
                filter: drop-shadow(0 10px 15px rgba(0,0,0,0.2));
            }

            @keyframes softFloat {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
                100% { transform: translateY(0px); }
            }
            
            /* Status Messages (Success/Error) */
            .stAlert {
                background-color: rgba(0, 0, 0, 0.4) !important;
                backdrop-filter: blur(10px);
                color: white !important;
                border: none !important;
                border-radius: 12px;
            }
        </style>
    """, unsafe_allow_html=True)