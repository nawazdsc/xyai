import os
import pygame
from pydub import AudioSegment


def play_audio_file(path: str) -> float:
    """Play an audio file using pygame and return its duration in seconds."""
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()

    ext = os.path.splitext(path)[1].lower()
    if ext == ".wav":
        audio = AudioSegment.from_wav(path)
    else:
        audio = AudioSegment.from_mp3(path)
    return len(audio) / 1000.0
