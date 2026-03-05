import subprocess
import uuid
import os
from config import PIPER_MODEL_PATH

def speak(text):
    os.makedirs("audio", exist_ok=True)

    text_file = f"audio/input_{uuid.uuid4().hex}.txt"
    output_wav = "audio/output.wav"

    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text)

    cmd = [
        "piper",
        "--model", PIPER_MODEL_PATH,
        "--input_file", text_file,
        "--output_file", output_wav
    ]

    subprocess.run(cmd, check=True)
    os.startfile(output_wav)
    os.remove(text_file)
