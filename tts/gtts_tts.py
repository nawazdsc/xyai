import os
from gtts import gTTS
from tts.utils import play_audio_file


def speak(text: str) -> float:
    """Generate speech using gTTS and play it. Returns duration in seconds."""
    try:
        os.makedirs("audio", exist_ok=True)
        output_path = os.path.join("audio", "output.mp3")
        tts = gTTS(text=text, lang="hi")
        tts.save(output_path)
        return play_audio_file(output_path)
    except Exception as e:
        print("⚠️ gTTS error:", e)
        print("\n🗣️ SAI:", text)
        return 0
