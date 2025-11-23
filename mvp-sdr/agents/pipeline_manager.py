"""
AGENT: pipeline_manager.py

PURPOSE:
Orchestrates the end-to-end SDR pipeline flow.

RESPONSIBILITIES:
- Initialize all agents (Enrichment, Pain, Router, Writer, Monitor)
- Load configuration
- Read input CSV
- Loop through leads:
    - Enrichment -> NormalizedLead
    - PainProfiler -> Pain
    - AngleRouter -> Angle
    - EmailWriter -> Email
- Collect results
- Run MonitorAgent
- Write output CSV if Monitor passes (or warns)

INPUT CONTRACT:
- None (uses settings)

OUTPUT CONTRACT:
- generated_emails.csv
- run_report.json
"""

class PipelineManager:
    pass
