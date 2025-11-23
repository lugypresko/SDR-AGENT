"""
AGENT: monitor_agent.py

PURPOSE:
Monitors pipeline health and data quality before final export.

INPUT CONTRACT:
- list of LeadResults (NormalizedLead + pain + angle)

OUTPUT CONTRACT:
- MonitoringReport object:
    - status: "PASS" | "WARN" | "FAIL"
    - metrics: dict of calculated stats
    - reasons: list of failure reasons

RESPONSIBILITIES:
- Check Enrichment Consistency: Are signals populated?
- Check Pain Diversity: Are we seeing > X unique pains?
- Check Angle Distribution: Is any angle > 50% of total?
- Alert on high fallback rates.

INTEGRATION:
- Called by PipelineManager after processing all leads, before writing CSV.
"""

class MonitorAgent:
    pass
