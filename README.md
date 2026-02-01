
# 🤖 Generative AI Chatbot Systems using Streamlit

This repository contains **three independent chatbot projects**, each implementing a **different conversational and system-design strategy** using **Generative AI**.
All chatbots are built using **Python**, **Streamlit**, and the **Google Gemini API**, and are designed as **standalone applications**.

The work was carried out as part of an **open-ended chatbot development assignment**, with emphasis on:

* Prompt engineering
* Conversation state management
* AI-assisted reasoning
* Memory and review mechanisms

---

## 📁 Repository Structure

```
.
├── Study_mate.py          # Multi-mode study assistant (StudyMate)
├── spaced_rep.py          # Spaced repetition chatbot with memory
├── socratic.py            # Strict Socratic tutoring chatbot
├── chat_history.json      # Auto-generated chat logs
├── memory.json            # Auto-generated spaced repetition data
├── .env                   # API key configuration (not committed)
└── README.md
```

Each Python file represents a **separate chatbot application** and can be executed independently.

---

## 🧠 Common Architecture and Tools

All three projects share a common technical foundation:

### 🔧 Core Technologies

* **Programming Language**: Python
* **UI Framework**: Streamlit
* **LLM Backend**: Google Gemini (`gemini-2.5-flash-lite`)
* **Environment Management**: `python-dotenv`
* **Persistence**: JSON-based local storage

### 🔄 Conversation Handling

* Chat history is stored using `st.session_state`
* On every user input, the **entire conversation context** is reconstructed and sent to Gemini
* Responses are rendered using Streamlit’s chat interface (`st.chat_message`)

This approach ensures **context-aware responses** without external databases.

---

## 🔹 Project 1: StudyMate – Multi-Mode Study Assistant

### 📌 Project Overview

**StudyMate** is a flexible study assistant chatbot designed to adapt its response style based on the user’s learning requirement.
Instead of building separate bots for each teaching style, this project demonstrates **dynamic system prompting** within a single application.

---

### 🧩 Learning Modes

The chatbot supports **three distinct modes**, selectable from the Streamlit sidebar:

#### 1. Explain Mode

* Generates simple, beginner-friendly explanations
* Uses short paragraphs and examples
* Intended for first-time exposure to a concept

#### 2. Socratic Mode

* Avoids giving direct answers
* Responds only with guiding questions
* Encourages users to reason step-by-step

#### 3. Revision Mode

* Produces concise, exam-oriented summaries
* Focuses on definitions, formulas, and key points
* Suitable for quick revision before assessments

---

### 🛠️ Implementation Details

* Mode selection implemented using `st.sidebar.radio`
* A dedicated `system_prompt()` function returns a **mode-specific system instruction**
* System instructions are injected at the beginning of each conversation
* Messages are converted into `types.Content` objects required by Gemini
* Conversation state is maintained entirely within the session
* UI logic and AI logic are cleanly separated

---

### 📦 Libraries Used

* `streamlit`
* `google.genai`
* `dotenv`
* `os`

---

## 🔹 Project 2: Spaced Repetition Chatbot

### 📌 Project Overview

This project implements a chatbot that combines **free-form conversation** with an automated **spaced repetition system (SRS)**.
The chatbot continuously learns from user interactions and schedules reviews to reinforce memory over time.

---

### 🧠 Core Components

#### 1. AI Interaction Layer

A helper function wraps all Gemini API calls and is reused for:

* Normal chatbot replies
* Rephrasing user queries into review questions
* Semantic answer evaluation
* Learnability detection

---

#### 2. Learnable Concept Detection

* Filters out greetings and trivial inputs
* Uses Gemini to classify whether an input represents a meaningful concept
* Prevents unnecessary memory pollution

---

#### 3. Persistent Memory System

Two JSON files are used:

* `chat_history.json`: stores all user–assistant interactions
* `memory.json`: stores spaced repetition items

Each memory item contains:

* Original user query
* AI-generated answer
* Current review level
* Last reviewed timestamp

---

#### 4. Spaced Repetition Scheduling

| Level | Review Interval |
| ----- | --------------- |
| 0     | 10 minutes      |
| 1     | 1 hour          |
| 2     | 1 day           |
| 3     | 4 days          |

* Time comparisons are handled using `datetime`
* Correct answers advance the level
* Incorrect answers reset the level to zero

---

### 🛠️ Implementation Details

* Due review questions are computed dynamically
* One question is selected randomly per review session
* Review questions are AI-generated for clarity
* User answers are evaluated semantically using Gemini
* Session state tracks review progress to avoid repetition

---

### 📦 Libraries Used

* `streamlit`
* `google.genai`
* `json`
* `datetime`
* `random`
* `dotenv`

---

## 🔹 Project 3: Socratic Chatbot – Strict Question-Driven Tutor

### 📌 Project Overview

This chatbot is designed to **strictly follow the Socratic method** of instruction, where learning occurs through questioning rather than explanation.

---

### 🧩 System Instruction Design

A long, carefully structured system instruction defines:

* Tutor personality and role
* Allowed response styles
* Rules enforcing question-only behavior
* Conditions under which direct explanations are permitted

This instruction is injected as the **first model message**, ensuring consistent behavior throughout the conversation.

---

### 🛠️ Implementation Details

* Every user message triggers a full context rebuild
* Responses are intentionally short and probing
* Only one clear question is asked at a time
* Explicit checks exist for:

  * User confusion
  * Requests for direct explanation
* Error handling is added for API failures
* Minimal UI to prioritize dialogue quality

---

### 📦 Libraries Used

* `streamlit`
* `google.genai`
* `dotenv`
* `json`
* `os`

---

## ▶️ Running the Applications

### Install Dependencies

```bash
pip install streamlit google-generativeai python-dotenv
```

### Configure Environment Variables

Create a `.env` file:

```env
GENAI_API_KEY=your_google_gemini_api_key
```

### Run Any Project

```bash
streamlit run Study_mate.py
streamlit run spaced_rep.py
streamlit run socratic.py
```

---

## 📌 Notes for Evaluation

* Each chatbot is **independent and self-contained**
* No external databases or services are required
* All persistence is file-based for simplicity
* Emphasis is placed on:

  * Prompt engineering
  * Conversation design
  * State management
  * Explainable AI behavior
* Code is intentionally written for readability and evaluation clarity

---

## 👤 Author

**Ramagiri Harshitha**
