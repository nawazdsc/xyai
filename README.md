# Sai — Free Medical Voice Assistant

Sai is a medical intake voice assistant that follows the flow: **STT → LLM → TTS**. The entire pipeline is 100% free and runs locally.

```
Mic Input → Whisper STT → Ollama LLM (llama3.1:8b) → Edge TTS → Speaker
```

---

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) installed and running with the `llama3.1:8b` model:

```bash
ollama pull llama3.1:8b
ollama serve
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Running

### CLI (microphone-based intake)

```bash
python main.py
```

### Streamlit Web UI

```bash
streamlit run app.py
```

The web UI accepts an uploaded `.wav` file, transcribes it, generates a response, plays it back via the configured TTS engine, and displays a triage recommendation.

---

## Configuration (`config.py`)

| Setting | Default | Options |
|---|---|---|
| `TTS_ENGINE` | `"edge"` | `"edge"`, `"gtts"`, `"piper"`, `"disabled"` |
| `EDGE_TTS_VOICE` | `"hi-IN-SwaraNeural"` | Any Edge TTS voice |
| `MODEL_NAME` | `"llama3.1:8b"` | Any Ollama model |

---

## TTS Engines

| Engine | Free | Windows | Quality |
|---|---|---|---|
| **Edge TTS** (default) | ✅ | ✅ | High (neural) |
| **gTTS** | ✅ | ✅ | Medium |
| **Piper** | ✅ | ❌ | High (local) |
| **Disabled** | ✅ | ✅ | Print only |

> **Note:** Piper TTS is not supported on Windows. Use Edge TTS or gTTS instead.

---

## Architecture

```
main.py
├── stt/whisper_stt.py       — Local Whisper transcription
├── llm/ollama_client.py     — Local Ollama LLM
├── tts/edge_tts_engine.py   — Edge TTS (default, free, Hindi neural)
├── tts/gtts_tts.py          — gTTS fallback
├── tts/piper_tts.py         — Piper TTS (Linux/Mac only)
├── tts/disabled_tts.py      — Print-only fallback
├── rules/red_flag_rules.py  — Urgent symptom detection
├── rules/triage_engine.py   — Post-intake triage recommendation
├── memory/patient_store.py  — Save patient data as JSON
└── memory/pdf/pdf_generator.py — Generate PDF reports
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in values if using ElevenLabs (not required for default setup):

```bash
cp .env.example .env
```

---

## Everything is Free

- **STT**: OpenAI Whisper (local)
- **LLM**: Ollama with llama3.1:8b (local)
- **TTS**: Edge TTS / gTTS (free, no API key needed)
