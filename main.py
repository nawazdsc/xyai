import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time

from stt.whisper_stt import transcribe_audio
from llm.ollama_client import ask_llm
from tts.eleven_tts import speak
from memory.patient_store import save_patient_data
from rules.red_flag_rules import check_red_flags
from memory.pdf.pdf_generator import generate_patient_pdf

# Load prompts
SYSTEM_PROMPT = open("prompts/intake_prompt.txt", encoding="utf-8").read()
SUMMARY_PROMPT = open("prompts/summary_prompt.txt", encoding="utf-8").read()


def record_audio(seconds=8, fs=16000):
    print("🎙️ सुन रहा हूँ...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write("audio/input.wav", fs, audio)


conversation = SYSTEM_PROMPT

print("🟢 Sai Medical Intake Started")

# 🔊 Initial greeting
duration = speak("नमस्ते, मैं साई हूँ। आपकी उम्र क्या है?")
print(f"⏳ Waiting {duration:.2f} seconds before listening...")
time.sleep(duration + 1)


while True:
    # 🎙️ Record only AFTER TTS + wait
    record_audio()
    user_text = transcribe_audio()
    user_text = user_text.strip()

    # Remove repeated words
    words = user_text.split()
    cleaned_words = []
    for i in range(len(words)):
        if i == 0 or words[i] != words[i-1]:
            cleaned_words.append(words[i])
    user_text = " ".join(cleaned_words)


    print("USER:", user_text)

    # 🛑 Manual end trigger
    if "बस" in user_text or "हो गया" in user_text:
        print("🧾 Generating structured summary...")

        final_response = ask_llm(SUMMARY_PROMPT + "\n" + conversation)

        print("📄 Final JSON:", final_response)

        save_patient_data(final_response)
        # 🔥 Generate PDF
        pdf_path = generate_patient_pdf(final_response)

        duration = speak("धन्यवाद। आपकी जानकारी सुरक्षित रूप से दर्ज कर ली गई है।")
        time.sleep(duration + 1)

        break

    conversation += f"\nUser: {user_text}"

    response = ask_llm(conversation)

    print("SAI:", response)

    # 🚨 Escalation check
    if "ESCALATE_TO_DOCTOR" in response:
        duration = speak("यह स्थिति गंभीर हो सकती है। डॉक्टर को सूचित किया जा रहा है।")
        time.sleep(duration + 1)
        break

    # 🔊 Speak response
    duration = speak(response)

    print(f"⏳ Waiting {duration:.2f} seconds before listening...")

    # ⏳ Wait for speech to finish (+1 second buffer)
    time.sleep(duration + 1)

    conversation += f"\nSai: {response}"


print("✅ कॉल समाप्त, डेटा सेव हो गया")
