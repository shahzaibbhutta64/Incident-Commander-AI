import os
import streamlit as st
from openai import OpenAI, APIStatusError, APIConnectionError
from config import GROQ_BASE_URL, MODEL_CANDIDATES

@st.cache_resource
def get_groq_client(api_key: str):
    """Initializes the OpenAI client configured for the Groq API endpoint."""
    if not api_key:
        raise ValueError("Groq API Key is missing. Provide a valid API key.")
    
    return OpenAI(
        base_url=GROQ_BASE_URL,
        api_key=api_key
    )

def get_active_model(client: OpenAI) -> str:
    """Dynamically fetches available models from Groq to avoid 404 errors."""
    try:
        available_models = [m.id for m in client.models.list().data]
        # Match candidate models against what's actually available on your account
        for candidate in MODEL_CANDIDATES:
            if candidate in available_models:
                return candidate
        
        # Fallback to the first available text model if candidates aren't listed
        if available_models:
            return available_models[0]
            
    except Exception as e:
        st.warning(f"Could not auto-detect model catalog: {str(e)}. Falling back to default.")
    
    return MODEL_CANDIDATES[0]

def run_agent_prompt(client: OpenAI, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    """Executes a chat completion call using an active Groq model."""
    selected_model = get_active_model(client)
    
    try:
        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
    except APIStatusError as e:
        st.error(f"⚠️ **Groq API Error [{e.status_code}] on model '{selected_model}'**: {e.message}")
        st.stop()
    except APIConnectionError:
        st.error("⚠️ **Connection Error**: Failed to connect to Groq API servers.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ **Unexpected Error**: {str(e)}")
        st.stop()
