import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Grab API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class QueryRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h3>index.html file not found in the project directory!</h3>"

import re

def clean_latex(text: str) -> str:
    """Removes LaTeX symbols, dollar signs, and backslash formatting from AI responses."""
    if not text:
        return ""
    # Remove math display dollar signs
    text = text.replace("$", "")
    # Clean common LaTeX commands like \text{...} or \circ
    text = re.sub(r'\\text\{([^}]*)\}', r'\1', text)
    text = text.replace(r'\circ', '°')
    text = text.replace(r'\$', '$')
    return text

@app.post("/api/chat")
def chat_with_agent(req: QueryRequest):
    if not client:
        raise HTTPException(
            status_code=500, 
            detail="GEMINI_API_KEY is missing or not set in the server environment."
        )

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=req.message,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a helpful AI chemistry assistant for Chemical Matrix. "
                    "CRITICAL RULE: Do NOT use any LaTeX syntax, backslashes, or dollar signs. "
                    "Write all numbers, units (like g/cm3), and temperatures (like °C) in plain text."
                ),
                temperature=0.7,
            )
        )
        
        # Clean any accidental LaTeX before sending to frontend
        cleaned_text = clean_latex(response.text)
        return {"response": cleaned_text}
        
    except Exception as e:
        print(f"\n--- CRITICAL API ERROR --- \n{str(e)}\n--------------------------")
        raise HTTPException(status_code=500, detail=str(e))