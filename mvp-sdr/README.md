# SDR-MVP System Architecture (SRD-02)

## Overview
This repository contains the **SDR-MVP Pipeline**, an agentic system designed to generate highly personalized, persona-specific outreach emails. The system uses a deterministic "Enrichment -> Pain -> Angle" flow to ensure relevance and differentiation.

## Directory Structure

```
mvp-sdr/
  agents/                 # Core logic agents
    enrichment_agent.py   # Signals extraction (MockLLM)
    pain_profiler.py      # Signal -> Pain mapping
    angle_router.py       # Pain -> Angle mapping
    email_writer.py       # Content generation
    email_quality_agent.py # QA (Scaffolding)
    pipeline_manager.py   # Orchestrator (Scaffolding)
    monitor_agent.py      # Health checks (Scaffolding)
  config/                 # Configuration
    settings.py           # Central settings
  tools/                  # Shared utilities
    mock_llm_provider.py  # Deterministic enrichment mock
    csv_lead_input.py     # Input handling (Scaffolding)
    logger.py             # Unified logging (Scaffolding)
  debug/                  # Debugging scripts
    debug_enrichment.py
    debug_pain_profiler.py
    debug_router.py
  generated_emails.csv    # Output file
  verify_mvp.py           # Verification suite
  README.md               # This file
```

## Core Agents

1.  **EnrichmentAgent**: Extracts signals (team structure, noise level, etc.) from lead data.
2.  **PainProfiler**: Maps signals to a specific, high-priority pain point (e.g., "Firefighting Spiral").
3.  **AngleRouter**: Selects the marketing angle that best addresses the pain.
4.  **EmailWriter**: Generates the final email using "The Push" methodology.

## New Components (SRD-02 Scaffolding)

- **PipelineManager**: Will replace `main.py` as the central orchestrator.
- **MonitorAgent**: Will enforce data quality gates before export.
- **EmailQualityAgent**: Will score generated emails for compliance.
- **Logger**: Will provide structured metrics and logs.

## Usage

**Run the Pipeline:**
```bash
python main.py
```

**Verify System Health:**
```bash
python verify_mvp.py
```

**Debug Specific Agents:**
```bash
python debug/debug_enrichment.py
python debug/debug_router.py
```
