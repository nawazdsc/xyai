import json
import os
from datetime import datetime

def save_patient_data(patient_json_text):
    os.makedirs("data/patients", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/patients/patient_{timestamp}.json"

    try:
        patient_data = json.loads(patient_json_text)
    except:
        print("⚠️ Invalid JSON from model. Saving raw text.")
        patient_data = {"raw_output": patient_json_text}

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(patient_data, f, indent=2, ensure_ascii=False)

    print("✅ Patient data saved:", file_path)
