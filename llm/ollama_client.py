import requests
from config import OLLAMA_URL, MODEL_NAME

def ask_llm(prompt):
    payload = {
    "model": MODEL_NAME,
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.1,   # 🔥 very important
        "top_p": 0.9,
        "num_ctx": 4096
    }
}


    r = requests.post(OLLAMA_URL, json=payload)
    return r.json()["response"].strip()
