import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load .env file if it exists (for local development)
load_dotenv()

# Try to get API key from Streamlit secrets (Cloud) or fallback to local environment
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if API key exists
if not GROQ_API_KEY:
    st.error("API Key not found. Please set GROQ_API_KEY in .env (for local) or in Streamlit secrets (for deployment).")
    st.stop()

# Streamlit page setup
st.set_page_config(page_title="MentalMend Chatbot", layout="centered", page_icon="🤖")

st.markdown(
    "<h1 style='text-align: center; color: #3b82f6;'>🤖 MentalMend</h1>", 
    unsafe_allow_html=True
)
st.markdown("<p style='text-align: center;'>I'm here for you &lt;3</p>", unsafe_allow_html=True)

# ------------------------------
# Fetch available models from Groq
# ------------------------------
headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
models_url = "https://api.groq.com/openai/v1/models"

available_models = []
try:
    res = requests.get(models_url, headers=headers)
    res.raise_for_status()
    available_models = [m["id"] for m in res.json().get("data", [])]
except Exception as e:
    st.error(f"Could not fetch models: {e}")

# Preferred order of models
preferred_models = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "mixtral-8x7b-32768",
    "gemma-7b-it"
]

# Pick first available model
MODEL_NAME = None
for m in preferred_models:
    if m in available_models:
        MODEL_NAME = m
        break

if not MODEL_NAME:
    st.error("❌ No valid Groq models available right now.")
    st.stop()

st.info(f"Using model: {MODEL_NAME}")

# ------------------------------
# Chatbot logic
# ------------------------------
# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Get user input
user_input = st.chat_input("How are you feeling?")
if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare API request to Groq
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": st.session_state.messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        with st.spinner("Thinking... 💭"):
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"]

        # Show bot reply
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err} - {response.text}")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
