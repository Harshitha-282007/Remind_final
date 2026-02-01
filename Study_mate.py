import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
from google.genai import types
# ---------------- SETUP ----------------
load_dotenv()

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

st.set_page_config(page_title="StudyMate AI", layout="centered")
st.title("📘 StudyMate AI")
st.caption("A smart study chatbot for explanation, revision & guided learning")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "Explain"

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Learning Mode")
st.session_state.mode = st.sidebar.radio(
    "Choose mode:",
    ["Explain", "Socratic", "Revision"]
)

# ---------------- SYSTEM PROMPTS ----------------
def system_prompt(mode):
    if mode == "Explain":
        return (
            "You are a friendly study assistant. "
            "Explain concepts in very simple, beginner-friendly language. "
            "Use short paragraphs and examples."
        )

    if mode == "Socratic":
        return (
            "You are a strict Socratic tutor. "
            "Do NOT give direct answers. "
            "Only ask guiding questions to lead the student."
        )

    if mode == "Revision":
        return (
            "You are a revision assistant. "
            "Give concise bullet-point summaries, key definitions, and formulas. "
            "Keep it exam-oriented."
        )

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
user_input = st.chat_input("Ask a topic or question...")

if user_input:
    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Build Gemini contents
    converstaion = []

    converstaion.append(
    types.Content(
        role="user",
        parts=[
            types.Part.from_text(
                text=system_prompt(st.session_state.mode)
            )
        ]
    )
    )
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        converstaion.append(
            types.Content(
                role = role,
                parts = [types.Part.from_text(text = msg["content"])]
            )
        )

    response = client.models.generate_content(
            model = "gemini-2.5-flash-lite",
            contents = converstaion
        )

    bot_reply = response.text

    # Store bot reply
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # Optional mini check
    if st.session_state.mode == "Explain":
        with st.chat_message("assistant"):
            st.markdown(
                "**Quick check:** Want a short question to test your understanding?"
            )
