import streamlit as st
from google import genai
from dotenv import load_dotenv
import json
import os
from datetime import datetime
import random
from google.genai import types

# ---------------- CONFIG ----------------
load_dotenv()

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

DATA_FILE = "chat_history.json"
SR_FILE = "memory.json"

REVIEW_INTERVALS = {
    0: 10 * 60,
    1: 60 * 60,
    2: 24 * 60 * 60,
    3: 4 * 24 * 60 * 60
}

# ---------------- AI HELPERS ----------------

def generate_text(text):
    response = client.models.generate_content(
        model= "gemini-2.5-flash-lite",
        contents=[
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=text)]
            )
        ]
    )
    return response.text.strip()

def phrase_review_question(raw_query):
    prompt = f"""
Rewrite the following user query into a clear review question.
Do NOT answer it.

User query:
{raw_query}
"""
    return generate_text(prompt)

def check_answer_with_ai(question, correct_answer, user_answer):
    prompt = f"""
Question:
{question}

Correct answer:
{correct_answer}

User answer:
{user_answer}

Is the user's answer essentially correct?
Reply with ONLY YES or NO.
"""
    return generate_text(prompt).upper() == "YES"

def check_with_ai(user_input):
    prompt = f"""
Decide if the following input is a learnable concept.
Reply with ONLY YES or NO.

Input:
{user_input}
"""
    return generate_text(prompt).upper() == "YES"

# ---------------- DATA HELPERS ----------------

def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_sr():
    return load_json(SR_FILE, {"items": []})

def save_sr(data):
    save_json(SR_FILE, data)

def load_chat():
    return load_json(DATA_FILE, {"interactions": []})

def save_chat(data):
    save_json(DATA_FILE, data)

def save_spaced_item(query, response):
    data = load_sr()
    data["items"].append({
        "query": query,
        "response": response,
        "level": 0,
        "last_reviewed": datetime.now().isoformat()
    })
    save_sr(data)

def get_due_items():
    data = load_sr()
    now = datetime.now()
    due = []

    for item in data["items"]:
        last = datetime.fromisoformat(item["last_reviewed"])
        interval = REVIEW_INTERVALS.get(item["level"], REVIEW_INTERVALS[3])
        if (now - last).total_seconds() >= interval:
            due.append(item)

    return due

def update_item(item, correct):
    if correct:
        item["level"] = min(item["level"] + 1, 3)
    else:
        item["level"] = 0
    item["last_reviewed"] = datetime.now().isoformat()

def basic_clean(text):
    ignore = {"hi","hello","hey","ok","okay","thanks","thank you","yo","hmm","huh","yes","no"}
    t = text.strip().lower()
    return len(t) >= 4 and t not in ignore

def is_valid_spaced_item(user_input):
    return basic_clean(user_input) and check_with_ai(user_input)

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "review_mode" not in st.session_state:
    st.session_state.review_mode = False

if "current_review_item" not in st.session_state:
    st.session_state.current_review_item = None

if "current_review_question" not in st.session_state:
    st.session_state.current_review_question = None

if "review_answer" not in st.session_state:
    st.session_state.review_answer = ""

# ---------------- UI ----------------

st.title("Spaced Repetition Chatbot")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT ----------------

if user_input := st.chat_input("Ask something..."):
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    context = ""
    for m in st.session_state.messages:
        role = "User" if m["role"] == "user" else "Assistant"
        context += f"{role}: {m['content']}\n"

    reply = generate_text(context)

    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

    chat_data = load_chat()
    chat_data["interactions"].append({
        "query": user_input,
        "response": reply,
        "time": datetime.now().isoformat()
    })
    save_chat(chat_data)

    if is_valid_spaced_item(user_input):
        save_spaced_item(user_input, reply)

# ---------------- REVIEW ----------------

st.divider()
st.header("📘 Review Due Questions")

due_items = get_due_items()

if not due_items:
    st.write("✅ No questions due for review.")
else:
    if not st.session_state.review_mode:
        st.session_state.current_review_item = random.choice(due_items)
        st.session_state.current_review_question = phrase_review_question(
            st.session_state.current_review_item["query"]
        )
        st.session_state.review_mode = True

    item = st.session_state.current_review_item

    st.write("### Question")
    st.write(st.session_state.current_review_question)

    st.text_input("Your answer:", key="review_answer")

    if st.button("Submit Answer"):
        correct = check_answer_with_ai(
            st.session_state.current_review_question,
            item["response"],
            st.session_state.review_answer
        )

        if correct:
            st.success("Correct!")
        else:
            st.error(f"Incorrect.\n\nCorrect answer:\n{item['response']}")

        sr_data = load_sr()
        for it in sr_data["items"]:
            if it is item:
                update_item(it, correct)
                break
        save_sr(sr_data)

        st.session_state.review_mode = False
        st.session_state.current_review_item = None
        st.session_state.current_review_question = None
