import streamlit as st
from config import CUSTOM_CSS
from groq_client import get_groq_client
from state_manager import init_state, reset_state
from pdf_utils import extract_text_from_pdf
from agents import generate_investigation_report

# Page Configuration
st.set_page_config(page_title="Incident Commander AI", page_icon="📋", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
init_state()

st.title("Incident Commander AI")
st.caption("Lead HSE Incident Investigation & Document Analysis Platform")

# Sidebar Configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.secrets.get("GROQ_API_KEY", None) or st.secrets.get("GROK_API_KEY", None) or st.text_input("Enter Groq API Key:", type="password")
    
    st.divider()
    if st.button("Reset Application"):
        reset_state()
        st.rerun()

if not api_key:
    st.warning("Please provide a valid Groq API key in sidebar or secrets.")
    st.stop()

try:
    client = get_groq_client(api_key)
except Exception as e:
    st.error(f"Error initializing client: {e}")
    st.stop()

# 1. Input Data & Context
st.subheader("1. Incident Input & Supporting Attachments")

col_text, col_files = st.columns(2)

with col_text:
    user_notes = st.text_area(
        "Enter unstructured incident details, statements, or initial reports:",
        height=180,
        placeholder="Enter incident context or leave blank if uploading full PDF report..."
    )

with col_files:
    uploaded_files = st.file_uploader(
        "Attach Investigation Documents (PDF format):",
        type=["pdf"],
        accept_multiple_files=True
    )

# Extract PDF contents
extracted_pdf_text = ""
if uploaded_files:
    pdf_chunks = []
    for file in uploaded_files:
        content = extract_text_from_pdf(file)
        pdf_chunks.append(f"=== ATTACHMENT: {file.name} ===\n{content}")
    extracted_pdf_text = "\n\n".join(pdf_chunks)

combined_input = f"{user_notes}\n\n{extracted_pdf_text}".strip()

st.divider()

# 2. Parameters & Scope Selection
st.subheader("2. Investigation Scope & Methodology")

col_a, col_b, col_c = st.columns(3)

with col_a:
    actual_severity = st.selectbox(
        "Actual Severity:",
        ["Minor / First Aid Case", "Medical Treatment Case", "Restricted Work Case", "Lost Time Injury", "Fatality"]
    )
    potential_severity = st.selectbox(
        "Potential Severity:",
        ["Low Potential", "Medium Potential", "High Potential / Major", "Fatality Risk"]
    )

with col_b:
    rca_method = st.selectbox(
        "Selected RCA Methodology:",
        ["5 Whys Analysis", "Fishbone (Ishikawa) Diagram", "TOPSET Methodology", "Tripod Beta"]
    )
    image_gen_enabled = st.checkbox("Generate AI Incident Scene Image Prompt", value=True)

with col_c:
    required_docs = st.multiselect(
        "Required Attachments Checklist:",
        options=[
            "Competency Certificates",
            "Witness Statements",
            "Injured Person Statement",
            "Pre-operational Logs",
            "HSE Induction Records",
            "Training Attendance Registry"
        ],
        default=["Competency Certificates", "Witness Statements", "Pre-operational Logs"]
    )

st.subheader("3. Required Report Output Sections")
selected_outputs = st.multiselect(
    "Select sections to include in the generated report:",
    options=[
        "Title",
        "Executive Summary",
        "Incident Description",
        "Immediate Actions Taken",
        "Incident Timeline",
        "Investigation Findings",
        "Root Cause Analysis",
        "Causes Breakdown",
        "Supporting Documents & Evidence Status",
        "Recommendations & CAPA Action Plan",
        "Conclusion",
        "AI Incident Image Prompt"
    ],
    default=[
        "Title",
        "Executive Summary",
        "Incident Description",
        "Immediate Actions Taken",
        "Incident Timeline",
        "Investigation Findings",
        "Root Cause Analysis",
        "Causes Breakdown",
        "Supporting Documents & Evidence Status",
        "Recommendations & CAPA Action Plan",
        "Conclusion"
    ]
)

st.divider()

# Execution Trigger
if st.button("Generate Investigation Report", type="primary"):
    if not combined_input:
        st.error("Please enter text details or upload at least one PDF file.")
    else:
        with st.spinner("Analyzing data and generating report according to compliance rules..."):
            st.session_state.generated_report = generate_investigation_report(
                client=client,
                raw_text=combined_input,
                actual_severity=actual_severity,
                potential_severity=potential_severity,
                rca_method=rca_method,
                required_docs=required_docs,
                selected_outputs=selected_outputs,
                image_gen_enabled=image_gen_enabled
            )

if st.session_state.generated_report:
    st.divider()
    st.markdown(st.session_state.generated_report)
