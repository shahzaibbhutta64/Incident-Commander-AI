import pypdf
from groq import Groq
from groq_client import run_agent_prompt

def extract_text_from_pdf(pdf_file) -> str:
    """Extracts plain text content from an uploaded PDF file."""
    try:
        reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text if text.strip() else "PDF content empty or unreadable."
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"

def run_hse_agent(
    client: Groq,
    mode: str,
    raw_text: str,
    actual_severity: str,
    potential_severity: str,
    rca_method: str,
    required_docs: list,
    selected_outputs: list,
    image_gen_enabled: bool,
    model_name: str = "llama-3.3-70b-versatile"
) -> str:
    """Executes HSE Investigation Generation or Audit based on selected mode and options."""
    
    # Cap input text to ~15,000 characters (~3,500 tokens) to safely fit within Groq context windows
    MAX_CHAR_LIMIT = 15000
    if len(raw_text) > MAX_CHAR_LIMIT:
        safe_raw_text = raw_text[:MAX_CHAR_LIMIT] + "\n\n[...TEXT TRUNCATED DUE TO LENGTH LIMITS...]"
    else:
        safe_raw_text = raw_text

    system_prompt = f"""
SYSTEM ROLE:
You are an expert Lead HSE Incident Investigator and Senior Safety Auditor. Operate in the selected mode:
- {mode}

--------------------------------------------------------------------------------
1. INPUT CONTEXT
--------------------------------------------------------------------------------
- SEVERITY: Actual={actual_severity} | Potential={potential_severity}
- RCA METHODOLOGY: {rca_method}
- CHECKLIST: {", ".join(required_docs) if required_docs else "None"}
- MANDATORY OUTPUT SECTIONS: {", ".join(selected_outputs)}

- INCIDENT / REPORT TEXT:
{safe_raw_text}

--------------------------------------------------------------------------------
2. STRICT DIRECTIVES
--------------------------------------------------------------------------------
1. OUTPUT FILTERING: Output ONLY the exact sections specified in "MANDATORY OUTPUT SECTIONS". Do NOT include unselected sections, introductory remarks, or conversational filler.
2. FACTUAL INTEGRITY: Use ONLY facts from the provided text. Never fabricate missing witness statements, dates, or causes.
3. ITEM COUNTS: Where applicable, provide at least 3 Immediate Actions, 3 Immediate Causes, 3 Underlying Causes, 3 Root Causes, and 4 Investigation Findings (TPOE).

--------------------------------------------------------------------------------
3. OUTPUT FORMATTING GUIDELINES
--------------------------------------------------------------------------------

IF "MODE A: GENERATE INVESTIGATION REPORT":
Generate ONLY selected sections from:
# [Incident Title]
## Executive Summary
## Incident Description
## Immediate Actions Taken
## Incident Timeline
## Investigation Findings
## Root Cause Analysis ({rca_method})
## Causes Breakdown
## Supporting Documents & Evidence Status
## Recommendations & CAPA Action Plan
## Conclusion
## AI Incident Image Prompt

IF "MODE B: REVIEW & AUDIT EXISTING REPORT":
Audit the provided report and generate ONLY selected sections from:
# Investigation Audit & Review Report
## Executive Review Summary
## Missing Investigation Details & Narrative Gaps
## RCA Execution Audit
## Evidence & Document Gap Analysis
## CAPA & Recommendation Improvements
## Specific Recommendations for Report Correction
"""

    return run_agent_prompt(
        client=client,
        prompt=system_prompt,
        system_message="You are a precise Lead HSE Auditor.",
        model_name=model_name
    )
