import whisper
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

print("🔧 Using device:", device)

model = whisper.load_model("medium", device=device)

def transcribe_audio(path="audio/input.wav"):
    result = model.transcribe(
        path,
        language="hi",
        task="transcribe",
        fp16=True
    )

    print("📝 Whisper raw:", result["text"])
    return result["text"].strip()
