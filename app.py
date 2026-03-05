import streamlit as st
import os

from stt.whisper_stt import transcribe_audio
from llm.ollama_client import ask_llm

# Load intake prompt
SYSTEM_PROMPT = open("prompts/intake_prompt.txt", encoding="utf-8").read()

st.set_page_config(page_title="Sai Medical Assistant")

st.title("🩺 Sai Medical Voice Assistant")
st.markdown("Upload patient audio (.wav) to interact with the AI assistant.")

uploaded_file = st.file_uploader("Upload Audio File", type=["wav"])

if uploaded_file is not None:

    os.makedirs("audio", exist_ok=True)

    # Save uploaded file
    audio_path = "audio/input.wav"
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Audio uploaded successfully.")

    # ---------------- STT ----------------
    with st.spinner("Transcribing audio..."):
        user_text = transcribe_audio()

    st.subheader("📝 Transcribed Text")
    st.write(user_text)

    # ---------------- LLM ----------------
    conversation = SYSTEM_PROMPT + "\nUser: " + user_text

    with st.spinner("Generating response..."):
        response = ask_llm(conversation)

    st.subheader("🤖 Sai's Response")
    st.write(response)