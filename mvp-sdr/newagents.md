AGENT: Antigravity  
TASK: Generate the following system components for the SDR-MVP pipeline.

OBJECTIVE: Build file structure and agent specifications (no implementation code) for the system restart with monitoring and modularity.

COMPONENTS:
1. Directory & file tree exactly as:
   mvp-sdr/
     agents/
       enrichment_agent.py
       pain_profiler.py
       angle_router.py
       email_writer.py
       email_quality_agent.py
       pipeline_manager.py
       monitor_agent.py
     config/
       settings.py
     tools/
       mock_llm_provider.py
       csv_lead_input.py
       logger.py
     debug/
       debug_enrichment.py
       debug_pain_profiler.py
       debug_router.py
     generated_emails.csv
     verify_mvp.py
     verify_phase5.py
     README.md

2. Specification (in comments or doc-blocks at top of each file):
   - Purpose of file/agent
   - Input contract
   - Output contract
   - Key responsibilities
   - No actual implementation code, only scaffolding and comments.

3. Configuration file settings.py:
   - Placeholders for thresholds (e.g., fallback_threshold, minimum_unique_pains)
   - Paths for CSV input/output
   - Logging level

4. Tools logger.py:
   - API definition (Logger.info, Logger.warn, Logger.error)
   - Metrics schema (run_id, timestamp, lead_count, fallback_count, signal_distribution)
   - Comments indicating persistent storage of metrics.

5. monitor_agent.py specification:
   - Describe checks for enrichment consistency, pain diversity, angle distribution.
   - Input: list of LeadResults (NormalizedLead + pain + angle)
   - Output: MonitoringReport (status, metrics, reasons)
   - Integration: called by PipelineManager before export.

CONSTRAINTS:
- Do not modify existing pipeline logic yet.
- Maintain determinism.
- Use only pre-existing contracts (NormalizedLead, AngleSignals) in comments.
- Prepare the system for future LLM integration but remain in mock mode now.

OUTPUT:
- A zipped or file-list output of the directory and file names with the specified content (scaffolding comments).
- No implementation logic beyond skeleton and comments.
- A succinct README.md summary of the system architecture and upcoming steps.

EXECUTION:
- When this directive is fed, Antigravity should create the file structure, generate file headers and docstrings, and indicate completion.

END TASK.
