import subprocess
import uuid
import os
from config import PIPER_MODEL_PATH
from tts.utils import play_audio_file

def speak(text):
    try:
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
        os.remove(text_file)
        return play_audio_file(output_wav)
    except Exception as e:
        print("⚠️ Piper TTS error:", e)
        print("\n🗣️ SAI:", text)
        return 0
