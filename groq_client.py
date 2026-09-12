import os
from openai import OpenAI
from config import GROQ_BASE_URL, DEFAULT_MODEL

def get_groq_client(api_key: str):
    """Initializes the OpenAI client configured for the Groq API endpoint."""
    if not api_key:
        raise ValueError("Groq API Key is missing. Provide a valid API key.")
    
    return OpenAI(
        base_url=GROQ_BASE_URL,
        api_key=api_key
    )

def run_agent_prompt(client: OpenAI, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    """Executes a chat completion call using the specified Groq model."""
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content
