import os

# Groq OpenAI-compatible base URL
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Active production free model string on Groq
DEFAULT_MODEL = "llama-3.1-8b-instant"

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
