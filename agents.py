from groq import Groq
from groq_client import run_agent_prompt

def generate_investigation_report(
    client: Groq,
    raw_text: str,
    actual_severity: str,
    potential_severity: str,
    rca_method: str,
    required_docs: list,
    selected_outputs: list,
    image_gen_enabled: bool,
    model_name: str = "llama3-70b-8192"
) -> str:
    """Generates a complete, factual HSE incident investigation report using Groq."""
    
    # Truncate input to avoid context limit issues
    safe_raw_text = raw_text[:12000] if len(raw_text) > 12000 else raw_text

    system_prompt = f"""
SYSTEM ROLE:
You are an expert Lead Health, Safety, and Environment (HSE) Incident Investigator. Your task is to process raw incident notes, uploaded documents, user selections, and required evidence to generate a professional, regulatory-compliant Incident Investigation Report.

--------------------------------------------------------------------------------
1. INPUT DATA & CONTEXT
--------------------------------------------------------------------------------
- INCIDENT RAW DETAILS & NOTES:
{safe_raw_text}

- SEVERITY CLASSIFICATION:
  - Actual Severity: {actual_severity}
  - Potential Severity: {potential_severity}

- SELECTED RCA METHODOLOGY:
  {rca_method}

- REQUIRED ATTACHMENTS & SUPPORTING EVIDENCE CHECKLIST:
  {", ".join(required_docs) if required_docs else "None Specified"}

- SELECTED OUTPUT SECTIONS TO GENERATE:
  {", ".join(selected_outputs) if selected_outputs else "All Default Sections"}

- AI INCIDENT SCENE IMAGE GENERATION:
  {"Enabled" if image_gen_enabled else "Disabled"}

--------------------------------------------------------------------------------
2. STRICT INVESTIGATION & COMPLIANCE RULES
--------------------------------------------------------------------------------
1. STRICT FACTUAL ACCURACY (NO ASSUMPTIONS OR EXAGGERATION):
   - All details, events, roles, and dates MUST be strictly based on and relevant to the provided text and attached documents.
   - DO NOT assume, fabricate, or exaggerate facts. If a detail is missing or unverified, state "Not Provided" or "Pending Verification."

2. MINIMUM MANDATORY ITEM COUNTS:
   - Immediate Actions: Must contain AT LEAST 3 distinct, factual immediate actions taken following the event.
   - Immediate Causes: Must contain AT LEAST 3 distinct immediate causes.
   - Underlying Causes: Must contain AT LEAST 3 distinct underlying causes.
   - Root Causes: Must contain AT LEAST 3 distinct root causes.
   - Investigation Findings: Must contain AT LEAST 4 distinct, documented findings across the Technology, People, Organization, and Environment categories.

3. RCA EXECUTION:
   - Perform the root-cause analysis strictly using the SELECTED RCA METHODOLOGY ({rca_method}).
   - Differentiate clearly between Immediate Causes (symptomatic events/failures), Underlying Causes (procedural/inspection/supervisory failures), and Root Causes (systemic/management weaknesses).

--------------------------------------------------------------------------------
3. OUTPUT GENERATION FORMAT
--------------------------------------------------------------------------------
Generate the report using ONLY the selected sections from the user choices while adhering strictly to the minimum counts:

# [Title of the Incident]

## Executive Summary
- Concise factual overview of the incident, key findings, actual vs. potential severity, and primary root cause.

## Incident Description
- Detailed, factual narrative of events prior to, during, and immediately following the incident.

## Immediate Actions Taken (Minimum 3 Required)
1. [Immediate Action 1]
2. [Immediate Action 2]
3. [Immediate Action 3]

## Incident Timeline
- Chronological breakdown (Time | Event / Action | Location | Involved Person / Role).

## Investigation Findings (Minimum 4 Required)
- Finding 1 (Technology): [Equipment condition, maintenance, physical failures, safety devices]
- Finding 2 (People): [Operator competency, certifications, experience, human factors]
- Finding 3 (Organization): [Supervision effectiveness, procedural enforcement, inspection protocols]
- Finding 4 (Environment): [Worksite conditions, weather, physical hazards, visibility]

## Root Cause Analysis ({rca_method})
- Step-by-step breakdown using the requested methodology (e.g., 5-Why chain or Fishbone categories).

## Causes Breakdown

### Immediate Causes (Minimum 3 Required)
1. [Immediate Cause 1]
2. [Immediate Cause 2]
3. [Immediate Cause 3]

### Underlying Causes (Minimum 3 Required)
1. [Underlying Cause 1]
2. [Underlying Cause 2]
3. [Underlying Cause 3]

### Root Causes (Minimum 3 Required)
1. [Root Cause 1]
2. [Root Cause 3]
3. [Root Cause 3]

## Supporting Documents & Evidence Status
- Table summarizing required attachments, whether they were provided, and specific gaps/recommendations for missing documentation.

## Recommendations & CAPA Action Plan
- Tabular format: [Item No | Corrective/Preventive Action | Responsible Person | Target Completion Date].

## Conclusion
- Final concluding statement summarizing factual lessons learned and preventive controls.

## AI Incident Image Prompt (Generated if Enabled)
- [A detailed, highly accurate prompt describing the visual scene of the incident based strictly on the reported facts for generating a visual illustration.]
"""

    return run_agent_prompt(
        client=client,
        prompt=system_prompt,
        system_message="You are a precise, factual HSE Lead Investigator.",
        model_name=model_name
    )
