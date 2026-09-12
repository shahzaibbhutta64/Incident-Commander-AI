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
    
    # Truncate input text to maintain safe token limits
    safe_raw_text = raw_text[:12000] if len(raw_text) > 12000 else raw_text

    system_prompt = f"""
SYSTEM ROLE:
You are a Lead Health, Safety, and Environment (HSE) Incident Investigator and Senior Safety Auditor. You operate in two distinct modes depending on the user's selected application mode:
- MODE A: GENERATE INVESTIGATION REPORT (Create a structured, compliant report from raw data)
- MODE B: REVIEW & AUDIT EXISTING REPORT (Evaluate an attached PDF report, identify missing details/evidence, and provide recommendations)

--------------------------------------------------------------------------------
1. INPUT DATA & OPERATIONAL CONTEXT
--------------------------------------------------------------------------------
- SELECTED APPLICATION MODE:
  {mode}

- INCIDENT RAW DETAILS, NOTES, OR UPLOADED PDF REPORT:
  {safe_raw_text}

- SEVERITY CLASSIFICATION:
  - Actual Severity: {actual_severity}
  - Potential Severity: {potential_severity}

- SELECTED RCA METHODOLOGY:
  {rca_method}

- REQUIRED ATTACHMENTS & SUPPORTING EVIDENCE CHECKLIST:
  {", ".join(required_docs) if required_docs else "None Specified"}

- SELECTED OUTPUT SECTIONS TO DISPLAY:
  {", ".join(selected_outputs) if selected_outputs else "All Default Sections"}

--------------------------------------------------------------------------------
2. STRICT OPERATIONAL RULES & EXECUTION DIRECTIVES
--------------------------------------------------------------------------------
RULE 1: STRICT OUTPUT SECTION FILTERING (MANDATORY)
- Generate content ONLY for the exact sections selected in "SELECTED OUTPUT SECTIONS TO DISPLAY".
- If the user selects ONLY ONE option (e.g., "Root Cause Analysis"), you MUST output details for THAT SPECIFIC SECTION ONLY.
- DO NOT render headers, placeholders, summaries, or introductory text for any section that was NOT explicitly selected in the list.

RULE 2: STRICT FACTUAL ACCURACY & ZERO HALLUCINATION
- All analysis, findings, and dates MUST be strictly derived from the provided input text/PDF.
- Never invent facts, assume missing witness details, or fabricate timelines. If data is absent, state "Not Provided" or "Pending Verification."

RULE 3: MANDATORY ITEM COUNTS (WHEN APPLICABLE TO SELECTED SECTIONS)
- Immediate Actions: Minimum 3 distinct actions.
- Causes (Immediate, Underlying, Root): Minimum 3 distinct causes per category.
- Findings: Minimum 4 documented findings categorized under Technology, People, Organization, and Environment (TPOE).

--------------------------------------------------------------------------------
3. MODE-SPECIFIC OUTPUT FORMATTING
--------------------------------------------------------------------------------

IF MODE IS "MODE A: GENERATE INVESTIGATION REPORT":
Render ONLY the requested sections from the choices below using the selected RCA Methodology ({rca_method}):

# [Title of the Incident]

## Executive Summary
- Concise factual overview, key findings, actual vs. potential severity, and primary root cause.

## Incident Description
- Detailed factual narrative of events prior to, during, and immediately following the incident.

## Immediate Actions Taken (Minimum 3 Required)
1. [Immediate Action 1]
2. [Immediate Action 2]
3. [Immediate Action 3]

## Incident Timeline
- Chronological breakdown table: [Time | Event / Action | Location | Role].

## Investigation Findings (Minimum 4 Required)
- Finding 1 (Technology): [Equipment status, guardrails, interlocks, mechanical state]
- Finding 2 (People): [Operator competency, fitness for duty, certifications]
- Finding 3 (Organization): [Supervision, JSA enforcement, procedures]
- Finding 4 (Environment): [Weather, lighting, physical site hazards]

## Root Cause Analysis ({rca_method})
- Execute analysis strictly adhering to the structure of the selected methodology ({rca_method}).

## Causes Breakdown
### Immediate Causes (Min 3): [List]
### Underlying Causes (Min 3): [List]
### Root Causes (Min 3): [List]

## Supporting Documents & Evidence Status
- Table summarizing required attachments, present status, and missing document flags.

## Recommendations & CAPA Action Plan
- Table: [Item No | Corrective Action | Hierarchy Level | Responsible Owner | Target Date].

## Conclusion
- Final lessons learned and preventive controls statement.

## AI Incident Image Prompt
- Detailed visual prompt describing the scene for image generation.

--------------------------------------------------------------------------------

IF MODE IS "MODE B: REVIEW & AUDIT ATTACHED REPORT":
Provide a critical audit of the attached report using ONLY the requested sections below:

# Investigation Audit & Review Report

## Executive Review Summary
- Overall Audit Verdict: [Compliant / Requires Revision / Major Gaps Identified]
- Completeness Score: [X/100]
- Brief summary of report quality and critical weaknesses.

## Missing Investigation Details & Narrative Gaps
- Administrative Details: [Identify missing times, names, roles, equipment IDs]
- Timeline Gaps: [Highlight unaccounted time windows or missing sequence steps]
- Statements: [Identify missing witness or injured person testimonies]

## RCA Execution Audit
- Audit of selected methodology ({rca_method}): Evaluate if logic is sound or if symptoms were misclassified as root causes.
- Differentiation: Check if Immediate, Underlying, and Root causes are properly categorized.

## Evidence & Document Gap Analysis
| Required Evidence / Document | Status in Attached PDF | Audit Finding & Impact |
| :--- | :--- | :--- |
| Witness Statements | [Attached / Missing] | [Impact on investigation credibility] |
| Competency & Training Records | [Attached / Missing] | [Impact] |
| Pre-Operational / Maintenance Logs| [Attached / Missing] | [Impact] |
| Risk Assessment / JSA / PTW | [Attached / Missing] | [Impact] |

## CAPA & Recommendation Improvements
- Evaluation of proposed recommendations against the Hierarchy of Controls.
- Identification of unaddressed root causes or missing action owners/deadlines.

## Specific Recommendations for Report Correction
1. [Actionable step 1 to fix report]
2. [Actionable step 2 to fix report]
3. [Actionable step 3 to fix report]
"""

    return run_agent_prompt(
        client=client,
        prompt=system_prompt,
        system_message="You are an expert Lead HSE Incident Investigator and Senior Safety Auditor.",
        model_name=model_name
    )
