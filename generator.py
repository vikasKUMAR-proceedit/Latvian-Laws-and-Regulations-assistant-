# generator.py - Uses Groq API for deployment

import sys
import os
import importlib.util

spec = importlib.util.spec_from_file_location(
    "retriever",
    os.path.join(os.path.dirname(__file__), "retriver.py")
)
retriever_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retriever_module)
retrieve = retriever_module.retrieve

from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)

GREETINGS = ["hi", "hello", "hey", "how are you", "what are you",
             "who are you", "what can you do", "help"]

def is_greeting(question):
    return any(word in question.lower().strip() for word in GREETINGS)


def generate_answer(question):

    if is_greeting(question):
        response = client.chat.completions.create(
            model    = "llama-3.3-70b-versatile",
            messages = [
                {
                    "role"   : "system",
                    "content": "You are a helpful Latvian law assistant. "
                               "For greetings respond briefly and friendly. "
                               "Let the user know you can answer questions about Latvian laws."
                },
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content, []

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

    response = client.chat.completions.create(
        model    = "llama-3.3-70b-versatile",
        messages = [{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content, chunks