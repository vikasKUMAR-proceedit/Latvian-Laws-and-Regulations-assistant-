# generator.py - Uses Groq API via direct HTTP requests (no groq library)

import sys
import os
import importlib.util
import requests
import streamlit as st

spec = importlib.util.spec_from_file_location(
    "retriever",
    os.path.join(os.path.dirname(__file__), "retriver.py")
)
retriever_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retriever_module)
retrieve = retriever_module.retrieve

# Try Streamlit secrets first, then environment variable
GROQ_API_KEY = ""
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found! "
        "Please set it in Streamlit Cloud secrets or as an environment variable."
    )

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"

GREETINGS = ["hi", "hello", "hey", "how are you", "what are you",
             "who are you", "what can you do", "help"]


def is_greeting(question):
    return any(word in question.lower().strip() for word in GREETINGS)


def call_groq(messages):
    """Direct API call to Groq - no groq library needed."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": messages
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def generate_answer(question):

    if is_greeting(question):
        messages = [
            {
                "role": "system",
                "content": "You are a helpful Latvian law assistant. "
                           "For greetings respond briefly and friendly. "
                           "Let the user know you can answer questions about Latvian laws."
            },
            {"role": "user", "content": question}
        ]
        return call_groq(messages), []

    chunks = retrieve(question)

    context = ""
    for chunk in chunks:
        context += f"\n[Source: {chunk['source']} | Page: {chunk['page']}]\n"
        context += chunk["text"] + "\n"

    prompt = f"""You are a helpful Latvian law assistant.
Use ONLY the context below to answer the question.
If the answer is not in the context, say "I could not find this in the provided documents."

Context:
{context}

Question: {question}

Answer clearly and simply:"""

    messages = [{"role": "user", "content": prompt}]
    return call_groq(messages), chunks
