# Sai — Free Medical Voice Assistant

Sai is a medical intake voice assistant that follows the flow: **STT → LLM → TTS**. The entire pipeline is 100% free.

```
Mic Input → Whisper STT → LLM (Groq or Ollama) → Edge TTS → Speaker
```

---

## Prerequisites

- Python 3.10+
- **Option A (default): Groq Cloud LLM** — Free API, no local GPU required. Get a free API key at [https://console.groq.com](https://console.groq.com).
- **Option B: Local Ollama** — [Ollama](https://ollama.ai/) installed and running with the `llama3.1:8b` model:

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

## LLM Configuration

Sai supports two LLM backends, selected via the `LLM_PROVIDER` environment variable (default: `groq`).

### Groq (default — recommended)

Groq provides a **free cloud API** giving access to powerful models like `llama-3.3-70b-versatile`.

1. Get a free API key at [https://console.groq.com](https://console.groq.com).
2. Copy `.env.example` to `.env` and set your key:

```bash
cp .env.example .env
# Edit .env and set GROQ_API_KEY=your_key_here
```

| Setting | Default |
|---|---|
| `LLM_PROVIDER` | `groq` |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` |
| `GROQ_API_KEY` | *(set via env or `.env`)* |

### Ollama (local fallback)

Set `LLM_PROVIDER=ollama` in your `.env` to use local Ollama instead.

| Setting | Default |
|---|---|
| `LLM_PROVIDER` | `ollama` |
| `MODEL_NAME` | `llama3.1:8b` |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` |

---

## Configuration (`config.py`)

| Setting | Default | Options |
|---|---|---|
| `LLM_PROVIDER` | `"groq"` | `"groq"`, `"ollama"` |
| `GROQ_MODEL` | `"llama-3.3-70b-versatile"` | Any Groq model |
| `MODEL_NAME` | `"llama3.1:8b"` | Any Ollama model |
| `TTS_ENGINE` | `"edge"` | `"edge"`, `"gtts"`, `"piper"`, `"disabled"` |
| `EDGE_TTS_VOICE` | `"hi-IN-SwaraNeural"` | Any Edge TTS voice |

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
├── llm/llm_router.py        — LLM router (Groq or Ollama)
├── llm/groq_client.py       — Groq Cloud LLM client
├── llm/ollama_client.py     — Local Ollama LLM client
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

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```

---

## Everything is Free

- **STT**: OpenAI Whisper (local)
- **LLM**: Groq Cloud with llama-3.3-70b-versatile (free API) or Ollama (local)
- **TTS**: Edge TTS / gTTS (free, no API key needed)
