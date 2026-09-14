import streamlit as st
from groq_client import get_groq_client
from agents import run_hse_agent, extract_text_from_pdf

st.set_page_config(
    page_title="Incident Commander AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Incident Commander AI")
st.markdown("Professional HSE Incident Investigation & Audit System")

# Mode Selection
app_mode = st.radio(
    "Select Application Mode:",
    ["MODE A: GENERATE INVESTIGATION REPORT", "MODE B: REVIEW & AUDIT EXISTING REPORT"],
    horizontal=True
)

st.divider()

col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.subheader("1. Incident Input & Documentation")
    
    input_text = ""
    if "MODE B" in app_mode:
        uploaded_pdf = st.file_uploader("Upload Investigation Report (PDF)", type=["pdf"])
        if uploaded_pdf:
            extracted_pdf_text = extract_text_from_pdf(uploaded_pdf)
            st.success("PDF text extracted successfully!")
            input_text = st.text_area(
                "Extracted Text (You can add additional comments/notes below):",
                value=extracted_pdf_text,
                height=450
            )
        else:
            input_text = st.text_area(
                "Paste Report Text Directly:",
                height=450,
                placeholder="Paste the report text or upload a PDF above..."
            )
    else:
        input_text = st.text_area(
            "Enter Raw Incident Details, Notes, and Statements:",
            height=500,
            placeholder="Describe what happened, timeline, equipment involved, personnel, site conditions, etc..."
        )

with col2:
    st.subheader("2. Investigation Parameters")
    
    c_act, c_pot = st.columns(2)
    with c_act:
        actual_sev = st.selectbox(
            "Actual Severity:",
            ["Minor", "Medical Treatment", "Restricted Work", "LTI", "Fatality"]
        )
    with c_pot:
        potential_sev = st.selectbox(
            "Potential Severity:",
            ["Low", "Medium", "High", "Major", "Fatality Risk"]
        )
        
    rca_method = st.selectbox(
        "Selected RCA Methodology:",
        [
            "5 Whys Analysis",
            "Fishbone (Ishikawa) Diagram",
            "Fault Tree Analysis (FTA)",
            "Event Tree Analysis (ETA)",
            "Bow-Tie Analysis",
            "Tripod Beta",
            "TOPSET Methodology"
        ]
    )
    
    required_docs = st.multiselect(
        "Required Attachments Checklist:",
        [
            "Witness Statements",
            "Competency & Training Records",
            "Pre-operational / Maintenance Logs",
            "Risk Assessment / JSA / PTW",
            "Medical / First Aid Reports",
            "Equipment Inspection Certificates",
            "Incident Scene Photos"
        ],
        default=[
            "Witness Statements",
            "Competency & Training Records",
            "Risk Assessment / JSA / PTW"
        ]
    )
    
    # Section options vary based on the mode
    if "MODE A" in app_mode:
        available_sections = [
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
        ]
    else:
        available_sections = [
            "Executive Review Summary",
            "Missing Investigation Details & Narrative Gaps",
            "RCA Execution Audit",
            "Evidence & Document Gap Analysis",
            "CAPA & Recommendation Improvements",
            "Specific Recommendations for Report Correction"
        ]
        
    selected_outputs = st.multiselect(
        "Required Report Output Sections:",
        options=available_sections,
        default=available_sections
    )
    
    image_gen = st.checkbox("Enable AI Image Scene Prompt", value=True if "MODE A" in app_mode else False)

st.divider()

if st.button("🚀 Process Request", type="primary", use_container_width=True):
    if not input_text.strip():
        st.error("Please provide input text or upload a valid PDF report.")
    elif not selected_outputs:
        st.error("Please select at least one output section to display.")
    else:
        with st.spinner("Processing request with Groq AI..."):
            try:
                client = get_groq_client()
                result = run_hse_agent(
                    client=client,
                    mode=app_mode,
                    raw_text=input_text,
                    actual_severity=actual_sev,
                    potential_severity=potential_sev,
                    rca_method=rca_method,
                    required_docs=required_docs,
                    selected_outputs=selected_outputs,
                    image_gen_enabled=image_gen
                )
                
                st.subheader("📋 Output Result")
                st.markdown(result)
                
                st.download_button(
                    label="📥 Download Output (.md)",
                    data=result,
                    file_name="hse_investigation_output.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Failed to process request: {str(e)}")
# --- ADD THIS AT THE VERY BOTTOM OF app.py ---

footer_html = """
<style>
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(6px);
        color: #ffffff;
        text-align: center;
        padding: 8px 16px;
        font-size: 14px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        z-index: 999999;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .footer-avatar {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #3B82F6;
    }

    .footer-link {
        color: #60A5FA;
        text-decoration: none;
        font-weight: 600;
    }

    .footer-link:hover {
        text-decoration: underline;
    }
</style>

<div class="custom-footer">
    <span>Created by</span>
    <a href="https://github.com/abbasraza5055" target="_blank" style="text-decoration: none; display: flex; align-items: center; gap: 8px;">
        <img src="https://github.com/abbasraza5055.png" class="footer-avatar" alt="abbasraza5055">
        <span class="footer-link">abbasraza5055</span>
    </a>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
