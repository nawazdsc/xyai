import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import json

from stt.whisper_stt import transcribe_audio
from llm.llm_router import ask_llm
from memory.patient_store import save_patient_data
from rules.red_flag_rules import check_red_flags
from rules.triage_engine import run_triage
from memory.pdf.pdf_generator import generate_patient_pdf
from tts.tts_factory import get_speak

speak = get_speak()

# Load prompts
SYSTEM_PROMPT = open("prompts/intake_prompt.txt", encoding="utf-8").read()
SUMMARY_PROMPT = open("prompts/summary_prompt.txt", encoding="utf-8").read()


def record_audio(seconds=8, fs=16000):
    print("🎙️ सुन रहा हूँ...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write("audio/input.wav", fs, audio)


def complete_intake(patient_data_json):
    """Save patient data, generate PDF, speak confirmation, and run triage."""
    print("📄 Final JSON:", patient_data_json)
    save_patient_data(patient_data_json)
    generate_patient_pdf(patient_data_json)
    speak("धन्यवाद। आपकी जानकारी सुरक्षित रूप से दर्ज कर ली गई है।")
    print("🩺 Running triage analysis...")
    triage_result = run_triage(patient_data_json)
    print("🩺 Triage:", triage_result)
    speak(triage_result)


conversation = SYSTEM_PROMPT

print("🟢 Sai Medical Intake Started")

# 🔊 Initial greeting
speak("नमस्ते, मैं साई हूँ, एक मेडिकल सहायक। कृपया बताइए, आप कौन हैं और मरीज़ से आपका क्या रिश्ता है?")


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

        patient_data_json = ask_llm(SUMMARY_PROMPT + "\n" + conversation)

        complete_intake(patient_data_json)
        break

    conversation += f"\nUser: {user_text}"

    response = ask_llm(conversation)

    print("SAI:", response)

    # 🚨 Escalation check
    if "ESCALATE_TO_DOCTOR" in response:
        speak("यह स्थिति गंभीर हो सकती है। डॉक्टर को सूचित किया जा रहा है।")
        break

    # 🔍 Check if response is valid JSON (LLM signals intake is complete)
    try:
        json.loads(response)
        print("📋 LLM returned JSON — intake complete.")
        complete_intake(response)
        break
    except (json.JSONDecodeError, ValueError):
        pass

    # 🔊 Speak response
    speak(response)

    conversation += f"\nSai: {response}"


print("✅ कॉल समाप्त, डेटा सेव हो गया")
