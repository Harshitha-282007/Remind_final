# 📘 StudyMate AI – Learning Chatbots using Generative AI

This repository contains **three independent chatbot applications** built using **Streamlit** and **Google Gemini API**.
Each project explores a **different AI-assisted learning strategy**, focusing on explanation, guided reasoning, and long-term retention.

These projects were developed as part of an **open-ended chatbot assignment**.

---

## 📁 Project Structure

```
.
├── Study_mate.py        # Multi-mode study assistant
├── spaced_rep.py        # Spaced repetition chatbot
├── socratic.py          # Socratic tutoring chatbot
├── chat_history.json    # (auto-generated)
├── memory.json          # (auto-generated)
├── .env                 # API key (not committed)
```

---

## 🔹 1. StudyMate AI – Multi-Mode Study Assistant

### 📌 Description

StudyMate AI is an interactive study chatbot that allows users to choose between **three learning modes**, each with a different teaching style.

### 🎯 Learning Modes

* **Explain Mode**
  Simple, beginner-friendly explanations using examples.
* **Socratic Mode**
  Concept discovery through guided questions without direct answers.
* **Revision Mode**
  Concise, exam-oriented summaries, definitions, and formulas.

### ✨ Key Features

* Mode selection via sidebar
* Session-based chat history
* Dynamic system prompting based on learning mode
* Beginner-focused design

---

## 🔹 2. Spaced Repetition Chatbot

### 📌 Description

This chatbot implements a **Spaced Repetition System (SRS)** to improve long-term memory retention.
Concepts asked by the user are automatically stored and reviewed at increasing time intervals.

### ✨ Key Features

* Automatic detection of learnable concepts
* AI-generated review questions
* Intelligent answer checking using Gemini
* JSON-based persistent memory
* Review scheduling based on correctness

### ⏱️ Review Intervals

* 10 minutes
* 1 hour
* 1 day
* 4 days

Correct answers increase the interval, while incorrect answers reset it.

---

## 🔹 3. Socratic Chatbot – Question-Driven Tutor

### 📌 Description

This chatbot strictly follows the **Socratic method of teaching**, prioritizing questions over explanations.

### ✨ Key Features

* Asks only guiding questions by default
* Breaks concepts into first principles
* Detects vague or incomplete understanding
* Switches to direct explanation only when explicitly requested
* Maintains a calm, one-on-one tutoring style

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Google Gemini API (`google.genai`)
* dotenv
* JSON (for persistent storage)

---

## ▶️ How to Run the Projects

### 1️⃣ Install dependencies

```bash
pip install streamlit google-generativeai python-dotenv
```

### 2️⃣ Set up environment variables

Create a `.env` file:

```env
GENAI_API_KEY=your_google_gemini_api_key
```

### 3️⃣ Run any chatbot

```bash
streamlit run Study_mate.py
streamlit run spaced_rep.py
streamlit run socratic.py
```

---

## 🎓 Educational Objectives

* Explore different AI-based teaching methodologies
* Apply prompt engineering for educational use cases
* Understand conversational state management
* Implement spaced repetition algorithms
* Evaluate user responses using generative AI

---
