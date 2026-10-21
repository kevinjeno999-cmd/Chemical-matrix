import os
import re
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Chemical Matrix",
    page_icon="🧪",
    layout="centered"
)

# Custom High-End Styling & Aggressive Avatar Removal
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    .stApp {
        background-color: #030712;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }

    /* Glassmorphic Chat Messages */
    .stChatMessage {
        background: rgba(17, 24, 39, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 1rem;
        padding: 1.2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 1rem;
    }

    /* COMPLETELY HIDE ALL AVATARS & EMOJIS IN CHAT */
    [data-testid="stChatMessageAvatar"],
    [data-testid="stChatMessageAvatarContainer"],
    .stChatMessage > div:first-child:has(img),
    .stChatMessage > div:first-child:has(svg),
    .stChatMessage [data-testid="stMarkdownContainer"] p:first-child:has(span) {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
        height: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Sleek Input Field */
    [data-testid="stChatInput"] textarea {
        background-color: rgba(15, 23, 42, 0.9) !important;
        color: #f3f4f6 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 0.75rem !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2) !important;
    }

    /* Modern Buttons */
    .stButton>button {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        color: #e2e8f0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 0.75rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #38bdf8;
        color: #38bdf8;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🧪 Chemical Matrix")
st.caption("Powered by Gemini 2.5 Flash & Streamlit")

# Retrieve API Key securely
api_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client
if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing! Please configure it in Streamlit Secrets.")
    client = None
else:
    client = genai.Client(api_key=api_key)

def clean_latex(text: str) -> str:
    """Removes LaTeX symbols, dollar signs, and backslash formatting from AI responses."""
    if not text:
        return ""
    text = text.replace("$", "")
    text = re.sub(r'\\text\{([^}]*)\}', r'\1', text)
    text = text.replace(r'\circ', '°')
    return text

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "matrix_bot", "content": "Hello! I am your advanced AI chemistry & periodic table assistant. Ask me anything about elements, properties, or reactions!"}
    ]

# Sidebar Controls for Chat History Management
with st.sidebar:
    st.header("⚙️ Chat Options")
    st.markdown(f"**Total Messages:** {len(st.session_state.messages)}")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = [
            {"role": "matrix_bot", "content": "Chat history cleared! Ask a new question to start again."}
        ]
        st.rerun()

# Render Existing Chat History (custom role names prevent default robot emoji)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Quick Prompt Buttons
cols = st.columns(3)
with cols[0]:
    if st.button("🟡 Gold Properties"):
        st.session_state.pending_prompt = "Tell me about Gold (Au)"
with cols[1]:
    if st.button("⬛ Carbon Structure"):
        st.session_state.pending_prompt = "What is the atomic structure of Carbon?"
with cols[2]:
    if st.button("🎈 Noble Gases"):
        st.session_state.pending_prompt = "Explain noble gases"

# Handle User Input
user_input = st.chat_input("Ask about an element or reaction...")

if "pending_prompt" in st.session_state:
    user_input = st.session_state.pending_prompt
    del st.session_state.pending_prompt

if user_input:
    # Save & Display User Message
    st.session_state.messages.append({"role": "user_query", "content": user_input})
    with st.chat_message("user_query"):
        st.markdown(user_input)

    # Generate Response with Real-Time Streaming
    with st.chat_message("matrix_bot"):
        if not client:
            st.error("API client not initialized.")
        else:
            try:
                response_stream = client.models.generate_content_stream(
                    model="gemini-3.5-flash",
                    contents=user_input,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "You are a helpful AI chemistry assistant for Chemical Matrix. "
                            "CRITICAL RULE: Do NOT use any LaTeX syntax, backslashes, or dollar signs. "
                            "Write all numbers, units (like g/cm3), and temperatures (like °C) in plain text."
                        ),
                        temperature=0.7,
                    )
                )

                def stream_generator():
                    for chunk in response_stream:
                        if chunk.text:
                            yield clean_latex(chunk.text)

                full_response = st.write_stream(stream_generator())
                # Save Assistant Message to History
                st.session_state.messages.append({"role": "matrix_bot", "content": full_response})

            except Exception as e:
                st.error(f"Error getting response: {str(e)}")