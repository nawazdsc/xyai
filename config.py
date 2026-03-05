import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"

LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "groq")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

LANGUAGE = "hi"

RED_FLAGS = [
    "chest pain",
    "सीने में दर्द",
    "difficulty breathing",
    "सांस लेने में दिक्कत",
    "suicidal",
    "आत्महत्या",
    "loss of consciousness",
    "बेहोशी",
    "severe bleeding",
    "ज्यादा खून बहना"
]

PIPER_MODEL_PATH = "models/piper/hi_IN-priyamvada-medium.onnx"

# TTS engine selection: "edge" (default), "gtts", "piper", "disabled"
TTS_ENGINE = "edge"

# Edge TTS voice for Hindi
EDGE_TTS_VOICE = "hi-IN-SwaraNeural"
