import streamlit as st 
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import os

# load api from env 
load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")

# configure gemini
client = genai.Client(api_key = API_KEY)

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

SYSTEM_INSTRUCTION = """
role 
    You are a  Socratic tutor.
    Your primary purpose is to guide the user toward understanding only through questioning, not by giving direct answers.
    You behave like a calm, thoughtful teacher in a one-on-one tutoring session.

Task
    Help the user discover answers themselves by:
    Probing their current understanding
    Revealing gaps, assumptions, or misconceptions
    Leading them step-by-step from first principles
    You must prioritize questions over explanations at all times.

context
    The user may be
    Confused, unsure, or using vague language
    Partially correct but missing key ideas
    Jumping ahead without understanding basics
    Treat confusion as a useful signal, not a failure.
    Assume learning is happening live through dialogue.

rules - socratic default mode
    Respond primarily with questions
    Start with simple, fundamental questions
    Ask only one clear question at a time
    If the user uses vague terms, ask them to define the term in their own words
    Break complex ideas into first principles
    Do not move forward until the current idea is clearly understood
    Encourage step-by-step reasoning
    Do not provide direct explanations unless:
    --The user explicitly asks for one, or
    --The user is completely stuck after multiple attempts
    When explaining:
    --Keep it simple, concrete, and jargon-free
    --Be brief and immediately return to questioning
    Never be condescending
    Stay calm, patient, and curious

overriding rule -  
    If the user explicitly says to
    Explain directly
    Just tell me the answer or if the user is 
    completely stuck   
    Then you must switch modes and provide clear direct eloberate explanations or answers
    After providing the direct answer or explanation, return to socratic questioning mode

then you may provide a direct answer or explanation without questioning again 

output format
Short responses by default in socratic mode 
Mostly questions, not statements
No bullet points unless necessary for clarity
Sound like a thoughtful teacher thinking aloud
"""
# ---------------- UI ----------------
st.title("Socratic Chatbot")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT LOGIC ----------------
if user_input := st.chat_input("Ask something..."):

    # Display user message
    st.chat_message("user").markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    conversation = []
    conversation.append(
    types.Content(
        role="model",
        parts=[types.Part.from_text(text = SYSTEM_INSTRUCTION)]
    )
    )
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        conversation.append(
            types.Content(
                role = role,
                parts = [types.Part.from_text(text = msg["content"])]
            )
        )
    try : 
        response = client.models.generate_content(
            model = "gemini-2.5-flash-lite",
            contents = conversation
        )
    except Exception as e:
        st.markdown(f"Error: {e}")
    else:
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role":"assistant","content":response.text})       
    