import os
from groq import Groq

def get_groq_client(api_key: str = None) -> Groq:
    """Initializes and returns the Groq client instance."""
    key = api_key or os.environ.get("GROQ_API_KEY") or os.environ.get("GROK_API_KEY")
    if not key:
        raise ValueError("Groq API key is missing.")
    return Groq(api_key=key)
