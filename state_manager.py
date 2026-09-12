import streamlit as st

def init_state():
    """Initializes persistent investigation state variables in Streamlit session state."""
    keys = [
        "raw_input",
        "evidence_analysis",
        "timeline",
        "causal_analysis",
        "rca_results",
        "capa_plan"
    ]
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = ""

def reset_state():
    """Resets all investigation data from session state."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
