import os
import streamlit as st
from openai import OpenAI, APIStatusError, APIConnectionError
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
    """Executes a chat completion call with explicit error handling."""
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
    except APIStatusError as e:
        st.error(f"⚠️ **Groq API Error [{e.status_code}]**: {e.message}")
        st.stop()
    except APIConnectionError:
        st.error("⚠️ **Connection Error**: Failed to connect to Groq API servers.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ **Unexpected Error**: {str(e)}")
        st.stop()
