import streamlit as st
import os

from stt.whisper_stt import transcribe_audio
from llm.ollama_client import ask_llm
from rules.triage_engine import run_triage
from tts.tts_factory import get_speak

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

    # ---------------- TTS ----------------
    tts_output = os.path.join("audio", "output.mp3")
    from config import TTS_ENGINE
    if TTS_ENGINE != "disabled":
        with st.spinner("Generating speech..."):
            try:
                speak = get_speak()
                speak(response)

                if os.path.exists(tts_output):
                    with open(tts_output, "rb") as audio_file:
                        st.audio(audio_file.read(), format="audio/mp3")
            except Exception as e:
                st.warning(f"TTS playback unavailable: {e}")

    # ---------------- Triage ----------------
    with st.spinner("Running triage analysis..."):
        triage_result = run_triage(response)

    st.subheader("🩺 Triage Recommendation")
    st.info(triage_result)