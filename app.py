import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Page Config
st.set_page_config(
    page_title="Chemical Matrix",
    page_icon="🧪",
    layout="centered"
)

# Custom Styling for Dark Theme & Glassmorphism feel
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
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🧪 Chemical Matrix")
st.caption("Powered by Gemini & Streamlit")

# Initialize Gemini Client
if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing! Please set it in your environment or a .env file.")
    client = None
else:
    client = genai.Client(api_key=api_key)

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your advanced AI chemistry & periodic table assistant. Ask me anything about elements, properties, or compounds!"}
    ]

# Display Chat History
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

# Handle User Input (via chat box or preset buttons)
user_input = st.chat_input("Ask about an element (e.g., Uranium, Copper, Oxygen)...")

if "pending_prompt" in st.session_state:
    user_input = st.session_state.pending_prompt
    del st.session_state.pending_prompt

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate Response from Gemini
    with st.chat_message("assistant"):
        if not client:
            st.error("API client not initialized.")
        else:
            with st.spinner("Analyzing properties..."):
                try:
                    response = client.models.generate_content(
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
                    reply_text = response.text
                    st.markdown(reply_text)
                    st.session_state.messages.append({"role": "assistant", "content": reply_text})
                except Exception as e:
                    st.error(f"Error getting response: {str(e)}")