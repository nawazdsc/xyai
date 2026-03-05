from config import TTS_ENGINE


def get_speak():
    """Return the speak() function for the configured TTS engine."""
    if TTS_ENGINE == "edge":
        from tts.edge_tts_engine import speak
    elif TTS_ENGINE == "gtts":
        from tts.gtts_tts import speak
    elif TTS_ENGINE == "piper":
        from tts.piper_tts import speak
    else:
        from tts.disabled_tts import speak
    return speak
