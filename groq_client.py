import os
from groq import Groq

def get_groq_client(api_key: str = None) -> Groq:
    """Initializes and returns the Groq client instance."""
    key = api_key or os.environ.get("GROQ_API_KEY") or os.environ.get("GROK_API_KEY")
    if not key:
        raise ValueError("Groq API key is missing.")
    return Groq(api_key=key)

def run_agent_prompt(client: Groq, prompt: str, system_message: str = "You are a helpful assistant.", model_name: str = "llama-3.3-70b-versatile") -> str:
    """Helper function to execute a prompt against the Groq API."""
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content
