from config import LLM_PROVIDER

_VALID_PROVIDERS = ("groq", "ollama")

if LLM_PROVIDER not in _VALID_PROVIDERS:
    raise ValueError(
        f"Invalid LLM_PROVIDER '{LLM_PROVIDER}'. "
        f"Must be one of: {', '.join(_VALID_PROVIDERS)}"
    )


def ask_llm(prompt):
    if LLM_PROVIDER == "groq":
        from llm.groq_client import ask_llm as groq_ask
        return groq_ask(prompt)
    else:
        from llm.ollama_client import ask_llm as ollama_ask
        return ollama_ask(prompt)
