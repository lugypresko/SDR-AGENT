Execution Instructions: BrightData Integration (No Code)

Goal:
Enhance lead enrichment with real-world company intelligence using BrightData’s datasets, while keeping the system deterministic, cost-controlled, and agent-compliant.

1. Purpose

Integrate BrightData as a Web Intelligence Layer that enriches each lead with externally validated signals.
This layer upgrades the accuracy of:

Normalization (Brain)

Routing (Soul)

Hooks (Writer)

Angle selection (Router)

Stress signals and complexity mapping

No changes to Writer or Router are needed initially — only enrichment.

2. Scope

BrightData integration will include two specific data sources only:

LinkedIn Company Search dataset
Used to extract:

Company description

Size confirmation

Industry/domain

Recent growth indicators

Job Postings dataset (Indeed / LinkedIn Jobs)
Used to extract:

Number of open engineering roles

Hiring trend signals

Team pressure / scaling indicators

No crawling. No scraping. No high-cost datasets.

3. Process Flow Integration
3.1. Pipeline placement

BrightData runs after CSV ingestion, before normalization:

CSV Lead
    ↓
BrightData Enrichment  ← New Layer
    ↓
Normalization Layer (Brain)
    ↓
Angle Router (Soul)
    ↓
Writer (Mouth)
    ↓
QA (Immune System)

This ensures the Router receives accurate real-world signals.

4. Responsibilities
4.1. BrightData Client Layer

A dedicated layer must:

Handle all requests to BrightData

Handle failures gracefully (empty response → fallback)

Expose two functions only:

search_company(name)

job_postings(domain)

4.2. WebEnrichmentAgent

This agent must:

Call the BrightData client once per lead

Extract insights into a structured dictionary

Provide the following normalized fields:

Field Source
company_size_verified LinkedIn Company dataset
domain_verified LinkedIn Company dataset
hiring_signals Jobs dataset
open_roles Jobs dataset
inferred_stress Computed based on job load
inferred_growth Computed based on hiring trend
inferred_complexity Computed from company metadata
4.3. Cache Layer

To prevent credit burn:

Must check local cache before making any BrightData request

Saves every response per-company

5. Data Requirements

The enrichment layer must extract the following:

Company Intelligence Signals

Verified size

Verified industry

Tech domain keywords

Growth or stagnation indicators

Location (optional)

Hiring Signals

Total open engineering roles

Seniority distribution (lead/principal roles amplify stress)

Rate of recent postings

Derived Signals

These must be computed after enrichment:

stress_signal (high hiring load → high internal pressure)

complexity_score (AI/Fintech → high complexity)

stage_signal (startup / scaleup / enterprise)

execution_noise_level (many open roles → high noise)

These fields feed directly into the existing Brain/Soul modules.

6. Cost Control Rules

To avoid burning the $50 BrightData credit:

Allowed Calls Per Lead

1× company search

1× job postings search

Forbidden

Repeated calls for the same company

Crawling

Real-time scraping

Dataset runs over 100 rows without batching

More than 2 queries per lead

Mandatory

Local cache for all prior responses

Dry-run mode to test pipeline without API usage

7. Test Procedure

Before using real credits, run:

Dry Run Mode

Simulate BrightData responses

Validate schema

Validate Router behavior

Single Lead Test

Run enrichment for 1 lead

Confirm extraction of all required signals

Confirm correct routing angle

Batch Test

Run 5–10 leads

Ensure caching prevents duplicate calls

Inspect logs for error handling

Verification Output

Save enriched_leads.csv

Confirm presence of:

verified company info

hiring trends

complexity/stress signals

8. Definition of Done (DoD)

BrightData integration is DONE when:

Pipeline runs without API errors

Each lead has:

company_size_verified

domain_verified

hiring_signals

open_roles

stress_signal

complexity

Cached requests prevent redundant API usage

Normalization layer uses enriched signals correctly

Router improves accuracy (visible in generated_emails.csv)

Total cost logged shows < $1 for 20 leads

Audit log shows deterministic enrichment per lead

9. Non-Goals

To keep costs and complexity low, Phase 1 does not include:

Real-time web scraping

Deep tech stack detection

Product reviews or sentiment scraping

Multi-dataset orchestration

Crawling company websites
