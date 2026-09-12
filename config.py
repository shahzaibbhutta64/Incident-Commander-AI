import os

# Model configuration matching Groq OpenAI-compatible endpoint
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "openai/gpt-oss-120b"

# High-contrast Dark HSE Industrial Theme CSS
CUSTOM_CSS = """
<style>
    /* Main Background and Text */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    
    /* Headers Accent Colors */
    h1, h2, h3 {
        color: #00E5FF !important;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Custom Styling for Streamlit Status / Expander Container */
    .stStatusWidget {
        border-color: #00E5FF !important;
    }
    
    /* Tab Headers */
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
