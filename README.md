[project_readme.md](https://github.com/user-attachments/files/33708646/project_readme.md)
# 🧪 Chemical Matrix

**Chemical Matrix** is a modern, responsive web application and AI agent designed for looking up chemical element data and exploring periodic table concepts. Built with Python, FastAPI, and Google's Gemini API, it features a glassmorphic dashboard styled with Tailwind CSS for seamless user interaction.

---

## ✨ Features

- **AI-Powered Element Lookup:** Ask complex questions about periodic table elements, chemical properties, electronic configurations, and real-world applications.
- **Clean Output Formatting:** Automatically strips raw LaTeX/Markdown math notation into clean, readable plain text.
- **Glassmorphic UI:** Modern dark-mode interface featuring glowing visual backdrops, real-time pulse indicators, and responsive message cards.
- **Quick-Prompt Suggestions:** Fast-action pill buttons to query popular topics instantly.
- **FastAPI Backend:** Lightweight and fast Python REST API backend.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, FastAPI, Uvicorn
- **AI Integration:** Google GenAI SDK (`google-genai`), Gemini Models
- **Frontend:** HTML5, JavaScript (Fetch API), Tailwind CSS
- **Environment Management:** `python-dotenv`

---

## 📁 Project Structure

```text
chemical-matrix/
│
├── app.py              # FastAPI application server & Gemini API handlers
├── index.html          # Single-page frontend chat dashboard
├── .env                # Local environment variables (API Key)
├── requirements.txt    # Python package dependencies
└── README.md           # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have Python installed on your system. You will also need an API key from **Google AI Studio**.

### 2. Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/chemical-matrix.git
   cd chemical-matrix
   ```

2. **Create and activate a virtual environment:**
   - **On Windows (Command Prompt):**
     ```cmd
     python -m venv venv
     venv\Scripts\activate.bat
     ```
   - **On Windows (PowerShell):**
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
     .\venv\Scripts\Activate.ps1
     ```
   - **On macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install required dependencies:**
   ```bash
   pip install fastapi uvicorn google-genai python-dotenv pydantic
   ```

---

## 🗝️ Environment Configuration

Create a `.env` file in the root directory of your project and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

---

## 🏃 Running the Application

1. Start the FastAPI development server:
   ```bash
   uvicorn app:app --reload
   ```

2. Open your web browser and go to:
   ```text
   http://127.0.0.1:8000
   ```

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
