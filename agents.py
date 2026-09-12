from groq_client import run_agent_prompt

# Core System Identity
SYSTEM_BASE = """
You are Incident Commander AI, an expert HSE multi-agent investigator.
Do not invent facts. Focus on systemic failures over worker blame.
Keep responses concise, well-structured, and factual.
"""

def agent_intake_and_evidence(client, raw_input: str) -> str:
    system_prompt = SYSTEM_BASE + "\nROLE: Evidence Analysis Agent."
    user_prompt = f"""
    Analyze the raw incident description below:
    ---
    {raw_input}
    ---
    Tasks:
    1. Assign Evidence IDs (E-001, E-002...).
    2. Categorize data into VERIFIED FACT, REPORTED INFO, INFERENCE, and ASSUMPTION.
    3. List missing evidence gaps.
    """
    return run_agent_prompt(client, system_prompt, user_prompt)

def agent_timeline_reconstruction(client, raw_input: str, evidence_output: str) -> str:
    system_prompt = SYSTEM_BASE + "\nROLE: Incident Reconstruction Agent."
    user_prompt = f"""
    Reconstruct timeline:
    Raw Input: {raw_input[:1500]}
    Evidence Summary: {evidence_output[:1500]}
    
    Tasks:
    1. Chronological sequence with Evidence IDs.
    2. Critical intervention points and time gaps.
    """
    return run_agent_prompt(client, system_prompt, user_prompt)

def agent_causal_analysis(client, timeline_output: str, evidence_output: str) -> str:
    system_prompt = SYSTEM_BASE + "\nROLE: Causal Analysis Agent."
    user_prompt = f"""
    Analyze causes based on findings:
    Timeline Summary: {timeline_output[:1500]}
    Evidence Summary: {evidence_output[:1000]}
    
    Tasks:
    1. Immediate Causes (3+).
    2. Contributing Causes (People, Task, Equipment, Environment, Management).
    3. Barrier Analysis (Effective, Failed, Missing).
    """
    return run_agent_prompt(client, system_prompt, user_prompt)

def agent_rca_engine(client, causal_output: str, evidence_output: str) -> str:
    system_prompt = SYSTEM_BASE + "\nROLE: Root Cause Analysis Agent."
    user_prompt = f"""
    Perform Root Cause Analysis:
    Causes Summary: {causal_output[:1500]}
    
    Tasks:
    1. 5-Why Analysis for management system failures.
    2. Root Causes addressing systemic issues.
    """
    return run_agent_prompt(client, system_prompt, user_prompt)

def agent_capa_generation(client, rca_output: str, causal_output: str) -> str:
    system_prompt = SYSTEM_BASE + "\nROLE: CAPA & Safety Alert Agent."
    user_prompt = f"""
    Generate Action Plan:
    RCA Summary: {rca_output[:1500]}
    
    Tasks:
    1. Actionable CAPA Plan.
    2. Field Safety Alert bulletin.
    """
    return run_agent_prompt(client, system_prompt, user_prompt)
