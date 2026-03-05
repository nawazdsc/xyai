from openai import OpenAI
from config import GROQ_API_KEY, GROQ_MODEL

_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def ask_llm(prompt):
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is not set. Get a free key at https://console.groq.com "
            "and set it in your .env file or environment."
        )
    response = _client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=4096,
    )
    return response.choices[0].message.content.strip()
