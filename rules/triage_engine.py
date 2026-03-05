import os
from llm.ollama_client import ask_llm


def run_triage(patient_json_text: str) -> str:
    """Run triage analysis on completed patient intake data.

    Args:
        patient_json_text: The patient intake data as a JSON string or raw text.

    Returns:
        Triage recommendation text in Hindi.
    """
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "triage_prompt.txt")
    with open(prompt_path, encoding="utf-8") as f:
        triage_prompt = f.read()

    full_prompt = triage_prompt + "\n" + patient_json_text
    return ask_llm(full_prompt)
