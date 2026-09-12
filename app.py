if st.button("Run Multi-Agent Investigation", type="primary"):
    if not raw_input.strip():
        st.error("Please enter incident details to process.")
    else:
        with st.status("Executing Multi-Agent Investigation Pipeline...", expanded=True) as status:
            
            st.write("🔍 **Agent 1 & 2**: Analyzing evidence, facts, and missing data...")
            st.session_state.evidence_analysis = agents.agent_intake_and_evidence(client, raw_input)
            time.sleep(3)  # Wait 3s to refresh Groq TPM counter
            
            st.write("⏱️ **Agent 3**: Reconstructing chronological timeline...")
            st.session_state.timeline = agents.agent_timeline_reconstruction(
                client, raw_input, st.session_state.evidence_analysis
            )
            time.sleep(3)
            
            st.write("⚠️ **Agent 4**: Evaluating immediate/contributing causes and barriers...")
            st.session_state.causal_analysis = agents.agent_causal_analysis(
                client, st.session_state.timeline, st.session_state.evidence_analysis
            )
            time.sleep(3)
            
            st.write("🧬 **Agent 5**: Conducting 5-Why Root Cause Analysis and RCA Challenge...")
            st.session_state.rca_results = agents.agent_rca_engine(
                client, st.session_state.causal_analysis, st.session_state.evidence_analysis
            )
            time.sleep(3)
            
            st.write("🛡️ **Agent 6**: Generating CAPA Plan and Safety Alert...")
            st.session_state.capa_plan = agents.agent_capa_generation(
                client, st.session_state.rca_results, st.session_state.causal_analysis
            )
            
            status.update(label="Investigation Workflow Completed!", state="complete", expanded=False)
