import os

# Groq OpenAI-compatible base URL
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Candidate models ordered by highest Tokens Per Minute (TPM) free limits
MODEL_CANDIDATES = [
    "llama-3.1-8b-instant",       # 30,000 TPM limit
    "llama-3.3-70b-versatile",    # High reasoning model
    "openai/gpt-oss-20b",
    "mixtral-8x7b-32768",
    "openai/gpt-oss-120b"
]

# High-contrast Dark HSE Industrial Theme CSS
CUSTOM_CSS = """
<style>
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    h1, h2, h3 {
        color: #00E5FF !important;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    .stStatusWidget {
        border-color: #00E5FF !important;
    }
    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00E5FF !important;
        border-bottom-color: #00E5FF !important;
    }
</style>
"""
