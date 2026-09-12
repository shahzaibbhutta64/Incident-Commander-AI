import os
from groq import Groq

def get_groq_client(api_key: str = None) -> Groq:
    """Initializes and returns the Groq client instance."""
    key = api_key or os.environ.get("GROQ_API_KEY") or os.environ.get("GROK_API_KEY")
    if not key:
        raise ValueError("Groq API key is missing.")
    return Groq(api_key=key)

def get_available_model(client: Groq, preferred_model: str = "llama-3.3-70b-versatile") -> str:
    """Queries the Groq API to retrieve active models accessible on the user's key."""
    try:
        models_response = client.models.list()
        active_ids = [m.id for m in models_response.data]
        
        # 1. Return preferred model if explicitly available
        if preferred_model in active_ids:
            return preferred_model
            
        # 2. Return high-capacity Llama 3 models if present
        for m_id in active_ids:
            if "llama-3.3" in m_id or "llama-3.1" in m_id:
                return m_id
                
        # 3. Fallback to any active text completion model available on the account
        for m_id in active_ids:
            if not m_id.startswith("whisper") and not m_id.startswith("canopylabs"):
                return m_id
                
        return preferred_model
    except Exception:
        return preferred_model

def run_agent_prompt(
    client: Groq, 
    prompt: str, 
    system_message: str = "You are a helpful assistant.", 
    model_name: str = "llama-3.3-70b-versatile"
) -> str:
    """Executes a prompt against active Groq models dynamically."""
    selected_model = get_available_model(client, model_name)
    
    response = client.chat.completions.create(
        model=selected_model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content
