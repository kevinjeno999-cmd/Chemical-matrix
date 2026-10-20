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

# Custom Styling for Dark Theme, Glassmorphism & Minimalist Chat
st.markdown("""
    <style>
    .stApp {
        background-color: #030712;
        color: #f3f4f6;
    }
    .stChatMessage {
        background-color: rgba(31, 41, 55, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 1rem;
    }
    /* Hide avatar icons completely from chat messages */
    .stChatMessage [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🧪 Chemical Matrix")
st.caption("Powered by Gemini & Streamlit")

# Retrieve API Key securely (Streamlit Cloud secrets first, then local .env)
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
    st.error("⚠️ GEMINI_API_KEY is missing! Please configure it in Streamlit Secrets or your .env file.")
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
        {"role": "assistant", "content": "Hello! I am your advanced AI chemistry & periodic table assistant. Ask me anything about elements, properties, or compounds!"}
    ]

# Display Chat History (using avatar=None to enforce icon-less bubbles)
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=None):
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

# Handle User Input (via chat input or preset buttons)
user_input = st.chat_input("Ask about an element (e.g., Uranium, Copper, Oxygen)...")

if "pending_prompt" in st.session_state:
    user_input = st.session_state.pending_prompt
    del st.session_state.pending_prompt

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=None):
        st.markdown(user_input)

    # Generate Response with Streaming (Typing Effect)
    with st.chat_message("assistant", avatar=None):
        if not client:
            st.error("API client not initialized.")
        else:
            try:
                # Stream content chunk by chunk
                response_stream = client.models.generate_content_stream(
                    model="gemini-flash-latest",
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

                # st.write_stream renders the response dynamically as it types
                full_response = st.write_stream(stream_generator)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"Error getting response: {str(e)}")