import requests
import os
from pydub import AudioSegment

API_KEY = "sk_5f3f9910e221cc644dc9c8febaba9acd89ddb936e216864c"
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

def speak(text):
    base_dir = os.path.abspath(os.getcwd())
    audio_dir = os.path.join(base_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    output_path = os.path.join(audio_dir, "output.mp3")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Accept": "audio/mpeg",
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.ok and len(response.content) > 0:
        with open(output_path, "wb") as f:
            f.write(response.content)

        # 🔊 Calculate duration
        audio = AudioSegment.from_file(output_path)
        duration = len(audio) / 1000.0  # seconds

        os.startfile(output_path)

        return duration
    else:
        print("TTS failed:", response.text)
        return 0
