from groq_client import run_agent_prompt

# Core System Identity and Rules
SYSTEM_BASE = """
You are Incident Commander AI, an expert multi-agent incident investigation platform supporting HSE professionals in heavy industry.
Adhere strictly to the Principle: Do not invent facts. Distinguish between VERIFIED FACTS, REPORTED INFO, INFERENCES, and ASSUMPTIONS.
Ensure findings reference traceable Evidence IDs (E-001, E-002...). Focus on systemic and organizational failures rather than worker blame.
"""

def agent_intake_and_evidence(client, raw_input: str) -> str:
    system_prompt = SYSTEM_BASE + "\nROLE: Evidence Analysis Agent & Gap Analyzer."
    user_prompt = f"""
    Analyze the raw incident description below:
    ---
    {raw_input}
    ---
    Tasks:
    1. Assign Evidence IDs (E-001, E-002...) to all referenced facts, statements, or documents.
    2. Categorize data into VERIFIED FACT, REPORTED INFO, INFERENCE, and ASSUMPTION.
    3. Perform Evidence Gap Analysis: List missing evidence, explain why it is vital, and specify what the investigator must obtain.
    4. Highlight any detected contradictions or evidence conflicts.
    """
    return run_agent_prompt(client, system_prompt, user_prompt)

def agent_timeline_reconstruction(client, raw_input: str, evidence_output: str) -> str:
    system_prompt = SYSTEM_BASE + "\nROLE: Incident Reconstruction & Timeline Agent."
    user_prompt = f"""
    Reconstruct the chronological timeline using the available input and evidence:
    Raw Input: {raw_input}
    Evidence Analysis: {evidence_output}
    
    Tasks:
    1. Build a clear chronological sequence (Pre-Incident, During Incident, Post-Incident).
    2. Map each event explicitly to an Evidence ID (e.g., [E-001]).
    3. Identify timeline gaps, unverified times, critical decisions, and missed intervention points.
    """
    return run_agent_prompt(client, system_prompt, user_prompt)

def agent_causal_analysis(client, timeline_output: str, evidence_output: str) -> str:
    system_prompt = SYSTEM_BASE + "\nROLE: Causal Analysis & Barrier Agent."
    user_prompt = f"""
    Analyze the causes and control barriers based on the timeline and evidence:
    Timeline: {timeline_output}
    Evidence: {evidence_output}
    
    Tasks:
    1. Identify Immediate Causes (at least 3).
    2. Identify Contributing Causes across People, Task, Equipment, Environment, and Management (at least 3).
    3. Perform Barrier Analysis: List intended barriers, their status (Effective, Failed, Missing, Bypassed), and supporting evidence.
    """
    return run_agent_prompt(client, system_prompt, user_prompt)

def agent_rca_engine(client, causal_output: str, evidence_output: str) -> str:
    system_prompt = SYSTEM_BASE + "\nROLE: Root Cause Analysis Agent (5-Why & Swiss Cheese Model)."
    user_prompt = f"""
    Execute Root Cause Analysis based on the causal findings:
    {causal_output}
    
    Tasks:
    1. Perform a rigorous 5-Why Analysis targeting underlying management system failures.
    2. Identify Root Causes (at least 3) addressing systemic/organizational breakdowns.
    3. Run 'Challenge the RCA': Provide critical counter-questions examining if conclusions are solidly backed by evidence ({evidence_output}).
    """
    return run_agent_prompt(client, system_prompt, user_prompt)

def agent_capa_generation(client, rca_output: str, causal_output: str) -> str:
    system_prompt = SYSTEM_BASE + "\nROLE: CAPA & Safety Alert Agent."
    user_prompt = f"""
    Generate an actionable CAPA plan and Safety Alert based on the RCA:
    RCA: {rca_output}
    Causes: {causal_output}
    
    Tasks:
    1. Build a structured CAPA Plan (Immediate, Corrective, Preventive, Systemic).
    2. Specify for each action: Action ID, Priority (Critical/High/Medium/Low), Root Cause Addressed, Action Description, Verification Method, and Effectiveness KPI.
    3. Draft a concise, professional Safety Alert for field distribution.
    """
    return run_agent_prompt(client, system_prompt, user_prompt)
