# app.py - Latvian Laws Assistant - ChatGPT style layout

import streamlit as st
import importlib.util
import setup

# build DB on first startup
setup.setup()

# ── load generator ────────────────────────────────────────────
spec = importlib.util.spec_from_file_location(
    "generator",
    "code/generator.py"
)
generator_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator_module)
generate_answer = generator_module.generate_answer

# ── page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Latvian Laws Assistant",
    page_icon="⚖️",
    layout="centered"
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0f0f0f;
    color: #e8e3d9;
}
.stApp { background-color: #0f0f0f; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2rem;
    padding-bottom: 6rem;
    max-width: 720px;
}
.app-header { text-align: center; margin-bottom: 2rem; }
.app-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #e8e3d9;
    margin: 0;
}
.app-subtitle {
    font-size: 0.85rem;
    color: #3a3a3a;
    margin-top: 0.3rem;
    font-style: italic;
}
.custom-divider {
    border: none;
    border-top: 1px solid #1a1a1a;
    margin: 1.2rem 0;
}
.pills-label {
    font-size: 0.7rem;
    color: #3a3a3a;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    margin-bottom: 0.6rem;
}
.stButton > button:not([kind="primary"]) {
    background-color: #111 !important;
    color: #555 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 20px !important;
    padding: 0.3rem 0.9rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.8rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
    color: #c8a96e !important;
    border-color: #2e2a22 !important;
}
.user-bubble {
    display: flex;
    justify-content: flex-end;
    margin: 1rem 0 0.4rem 0;
}
.user-bubble-inner {
    background: #1e1e1e;
    color: #e8e3d9;
    border-radius: 18px 18px 4px 18px;
    padding: 0.8rem 1.2rem;
    max-width: 80%;
    font-size: 0.92rem;
    line-height: 1.6;
}
.bot-bubble {
    display: flex;
    justify-content: flex-start;
    margin: 0.4rem 0 1rem 0;
}
.bot-bubble-inner {
    background: #141414;
    border: 1px solid #1e1e1e;
    border-left: 3px solid #c8a96e;
    border-radius: 4px 18px 18px 18px;
    padding: 1rem 1.3rem;
    max-width: 90%;
    font-size: 0.92rem;
    line-height: 1.8;
    color: #ccc9c0;
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to   { opacity: 1; transform: translateY(0); }
}
.stTextInput > div > div > input {
    background-color: #111 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 14px !important;
    color: #e8e3d9 !important;
    padding: 0.9rem 1.2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
    transition: border-color 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2e2a22 !important;
    box-shadow: 0 0 0 4px rgba(200,169,110,0.05) !important;
}
.stTextInput > div > div > input::placeholder { color: #2e2e2e !important; }
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #c8a96e, #a8854a) !important;
    color: #0a0a0a !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(200,169,110,0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# ── init session state ────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── header ────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1 class="app-title">⚖️ Latvian Laws Assistant</h1>
    <p class="app-subtitle">Powered by local AI — no data leaves your machine</p>
</div>
<hr class="custom-divider">
""", unsafe_allow_html=True)

# ── example pills only when no history ───────────────────────
if not st.session_state.history:
    st.markdown('<p class="pills-label">Try asking</p>', unsafe_allow_html=True)
    examples = [
        "Fundamental rights of citizens?",
        "Employee rights in Latvia?",
        "Punishment for theft?",
        "How to join local government?",
    ]
    cols = st.columns(4)
    for i, example in enumerate(examples):
        with cols[i]:
            if st.button(example, key=f"ex_{i}"):
                with st.spinner("Searching Latvian law documents..."):
                    answer, _ = generate_answer(example)
                st.session_state.history.append({
                    "question": example,
                    "answer"  : answer
                })
                st.rerun()
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# ── chat history ──────────────────────────────────────────────
for chat in st.session_state.history:
    st.markdown(f"""
    <div class="user-bubble">
        <div class="user-bubble-inner">{chat['question']}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="bot-bubble">
        <div class="bot-bubble-inner">{chat['answer']}</div>
    </div>
    """, unsafe_allow_html=True)

# ── input ─────────────────────────────────────────────────────
question = st.text_input(
    label            = "Your question",
    placeholder      = "Ask anything about Latvian law...",
    value            = "",
    key              = f"input_{len(st.session_state.history)}",
    label_visibility = "collapsed"
)

ask = st.button("Ask", type="primary", key="ask_btn")

# ── generate ──────────────────────────────────────────────────
if ask and question.strip():
    with st.spinner("Searching Latvian law documents..."):
        answer, _ = generate_answer(question)

    st.session_state.history.append({
        "question": question,
        "answer"  : answer
    })
    st.rerun()