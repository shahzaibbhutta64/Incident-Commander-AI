import streamlit as st
import os
import time

from config import CUSTOM_CSS
from groq_client import get_groq_client
from state_manager import init_state, reset_state
import agents

# Page Configuration
st.set_page_config(
    page_title="Incident Commander AI",
    page_icon="🚨",
    layout="wide"
)

# Inject Custom CSS Theme
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize Session State
init_state()

# Header Section
st.title("🚨 INCIDENT COMMANDER AI")
st.caption("Automated Multi-Agent Incident Investigation & Root-Cause Analysis Platform")

# Sidebar Configuration and API Key Detection
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Retrieve API key across potential environments (Colab userdata, Streamlit Secrets, or manual input)
    api_key = None
    try:
        from google.colab import userdata
        api_key = userdata.get('GROK_API_KEY')
    except Exception:
        api_key = st.secrets.get("GROK_API_KEY", None)
        
    if not api_key:
        api_key = st.text_input("Enter Groq API Key:", type="password")
    else:
        st.success("API Key detected successfully!")
        
    st.divider()
    
    # Status Indicators
    st.subheader("Workflow Status")
    st.markdown(f"""
    * **Intake & Evidence**: {'✅' if st.session_state.evidence_analysis else '⏳'}
    * **Timeline Reconstruction**: {'✅' if st.session_state.timeline else '⏳'}
    * **Causal & Barrier Analysis**: {'✅' if st.session_state.causal_analysis else '⏳'}
    * **RCA Engine**: {'✅' if st.session_state.rca_results else '⏳'}
    * **CAPA & Safety Alert**: {'✅' if st.session_state.capa_plan else '⏳'}
    """)
    
    st.divider()
    if st.button("Reset Workflow", type="secondary"):
        reset_state()
        st.rerun()

if not api_key:
    st.warning("Please provide a valid Groq API Key to run the investigation workflow.")
    st.stop()

# Initialize API Client
client = get_groq_client(api_key)

# Main Intake Input Area
st.subheader("Incident Input & Initial Data")

default_text = """On 12-09-2026 at 10:30 AM during pipe lifting at Station 4, crane load swung unexpectedly. Permit PTW-402 was active. Operator states wind gust was severe. JSA was signed off at shift start. Inspection logs for crane sling show last inspection was 6 months ago (3 month requirement). No injuries reported, minor pipe coating damage."""

raw_input = st.text_area(
    "Enter unstructured incident details, statements, logs, or initial reports:", 
    value=st.session_state.raw_input or default_text, 
    height=150
)
st.session_state.raw_input = raw_input

if st.button("Run Multi-Agent Investigation", type="primary"):
    if not raw_input.strip():
        st.error("Please enter incident details to process.")
    else:
        with st.status("Executing Multi-Agent Investigation Pipeline...", expanded=True) as status:
            
            st.write("🔍 **Agent 1 & 2**: Analyzing evidence, facts, and missing data...")
            st.session_state.evidence_analysis = agents.agent_intake_and_evidence(client, raw_input)
            time.sleep(1)
            
            st.write("⏱️ **Agent 3**: Reconstructing chronological timeline...")
            st.session_state.timeline = agents.agent_timeline_reconstruction(
                client, raw_input, st.session_state.evidence_analysis
            )
            time.sleep(1)
            
            st.write("⚠️ **Agent 4**: Evaluating immediate/contributing causes and barriers...")
            st.session_state.causal_analysis = agents.agent_causal_analysis(
                client, st.session_state.timeline, st.session_state.evidence_analysis
            )
            time.sleep(1)
            
            st.write("🧬 **Agent 5**: Conducting 5-Why Root Cause Analysis and RCA Challenge...")
            st.session_state.rca_results = agents.agent_rca_engine(
                client, st.session_state.causal_analysis, st.session_state.evidence_analysis
            )
            time.sleep(1)
            
            st.write("🛡️ **Agent 6**: Generating CAPA Plan and Safety Alert...")
            st.session_state.capa_plan = agents.agent_capa_generation(
                client, st.session_state.rca_results, st.session_state.causal_analysis
            )
            
            status.update(label="Investigation Workflow Completed!", state="complete", expanded=False)

# Display Formatted Results in Tabbed View
if st.session_state.evidence_analysis:
    st.divider()
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. Evidence & Gaps", 
        "2. Timeline", 
        "3. Causes & Barriers", 
        "4. Root Cause Analysis", 
        "5. CAPA & Safety Alert"
    ])
    
    with tab1:
        st.markdown(st.session_state.evidence_analysis)
        
    with tab2:
        st.markdown(st.session_state.timeline)
        
    with tab3:
        st.markdown(st.session_state.causal_analysis)
        
    with tab4:
        st.markdown(st.session_state.rca_results)
        
    with tab5:
        st.markdown(st.session_state.capa_plan)
