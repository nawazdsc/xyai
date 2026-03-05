import asyncio
import os
import edge_tts
from config import EDGE_TTS_VOICE
from tts.utils import play_audio_file


async def _synthesize(text: str, output_path: str) -> None:
    communicate = edge_tts.Communicate(text, EDGE_TTS_VOICE)
    await communicate.save(output_path)


def speak(text: str) -> float:
    """Generate speech using Edge TTS and play it. Returns duration in seconds."""
    try:
        os.makedirs("audio", exist_ok=True)
        output_path = os.path.join("audio", "output.mp3")
        asyncio.run(_synthesize(text, output_path))
        return play_audio_file(output_path)
    except Exception as e:
        print("⚠️ Edge TTS error:", e)
        print("\n🗣️ SAI:", text)
        return 0
