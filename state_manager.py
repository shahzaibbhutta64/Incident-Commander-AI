import streamlit as st

def init_state():
    """Initializes session state variables."""
    if "raw_input" not in st.session_state:
        st.session_state.raw_input = ""
    if "generated_report" not in st.session_state:
        st.session_state.generated_report = ""

def reset_state():
    """Resets all generated outputs."""
    st.session_state.raw_input = ""
    st.session_state.generated_report = ""
