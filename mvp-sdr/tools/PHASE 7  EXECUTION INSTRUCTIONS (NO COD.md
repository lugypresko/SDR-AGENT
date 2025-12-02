PHASE 7 — EXECUTION INSTRUCTIONS (NO CODE)
Centralized Signal Engine (CSE) Version
“Confidence Engine + Explainability + Lead Scoring — Unified Intelligence Layer”

1. Mission of Phase 7

Transform the SDR pipeline from a sequence of independent agents into a single coherent intelligence system by centralizing ALL reasoning, scoring, and explainability into one module:

CSE — Centralized Signal Engine.

This removes duplication, ensures deterministic behavior, simplifies debugging, and makes the system enterprise-ready.

2. What Changes in the Architecture
Before (Weak Version)

Each agent tried to compute confidence/explanations

Scattered logic

Hard to audit

Hard to debug

Hard to tune

Now (Strong Version)

Agents return raw facts only.

All intelligence logic happens at the end in a single module:

Signal normalization

Weighting

Confidence

Explainability

Lead score

Priority tier

Global trace

This is the cleanest and most scalable design.

3. Required Pipeline Behavior
A. Agents Produce Raw Data Only

Every agent must output only factual signals, not intelligence.

Examples:

Enrichment Agent

Hiring ratios

Headcount deltas

Tech stack tokens

Leadership churn

Pain Profiler

Identified pain points

Signal strength

Matched patterns

Angle Router

Candidate angles

Chosen angle

Rejected alternatives

Email Writer

Email metadata (tone, length, personalization depth)

Quality Agent

Clarity score

Coherence

Safety

Agents must not:

Emit confidence

Explain themselves

Produce scores

Apply weights

Do any prioritization

The only job of the agents is:
Produce the raw signals.

B. Orchestrator Aggregates Raw Data

The orchestrator should:

Collect all outputs in a unified structure

Do zero interpretation

Do zero scoring

Pass everything into the CSE unchanged

The orchestrator must remain “dumb” — it does not think, it only manages the flow.

C. Centralized Signal Engine (CSE) Performs ALL Reasoning
CSE Input:

All raw agent data

System configuration (weights, thresholds)

Domain rules

Normalization rules

CSE Processing Steps (no code, just logic):

1. Signal Normalization Layer

Transform all inputs to a consistent 0–1 scale:

Hiring stress normalized

Pain strength normalized

Domain complexity normalized

Personalization depth normalized

All signals must be comparable.

2. Weighted Signal Layer

Apply weighting once, in one place:

Pain signals (high weight)

Org health signals

Complexity

Personalization

Enrichment completeness

Weights must be defined in a single config file.

3. Conflict Resolution Layer

Resolve contradictions:

High complexity + weak personalization → adjust score

Strong pains + weak enrichment → apply penalty

High org health + negative churn signal → normalize

This ensures the score reflects real-world business logic.

4. Confidence Engine

Compute system certainty:

Global confidence

Minimum agent confidence

Variance

Penalties for missing data

Penalties for contradictory data

Confidence is derived from normalized signals — not from agent opinions.

5. Explainability Builder

Build a single, coherent reasoning tree:

Why each signal was weighted as it was

Why the angle matches the pain

Why certain alternatives were not selected

Why the final score is high or low

Why the lead was placed in a given tier

All explanations must be consistent and deterministic.

6. Lead Score Calculator

Produce the final business score:

Numeric lead_score (0–100)

score_breakdown by category

priority_tier (A / B / C)

Flags for low confidence or missing signals

Scoring must be deterministic, auditable, and reproducible.

4. Required Outputs of Phase 7
A. Updated CSV (per lead)

Each row must include:

lead_score

priority_tier

avg_confidence

min_confidence

score_breakdown

explanation_summary

B. Full Pipeline Trace

One additional artifact:

pipeline_trace.json

Contains:

All raw agent outputs

All normalized signals

Final weighted signals

Full reasoning tree

Confidence reasoning

Scoring details

Conflict resolution outcomes

5. Non-Functional Requirements
Determinism

Same input → same output

No randomness

No time-based decisions

Auditability

Every decision must be explainable

Every score must be reproducible

Every reasoning step must be transparent

Performance

CSE must add minimal overhead (< 50ms per lead)

Runs fully in Docker CPU mode

Isolation

Agents and CSE must not overlap in responsibility

6. Definition of Done

Phase 7 is considered DONE when:

Agents emit raw factual data ONLY

Orchestrator aggregates without interpretation

CSE produces:

Normalized signals

Weighted signals

Conflict resolutions

Full reasoning tree

Confidence profile

Lead score + tier

CSV includes all new fields

pipeline_trace.json is complete and consistent

Mock mode runs 5 times with identical output

CSE thresholds and weights can be tuned via config

Explainability is readable and meaningful

No scoring or confidence logic remains inside agents

7. One-Sentence Executive Summary

Phase 7 centralizes all intelligence into a single CSE module, making the SDR engine predictable, explainable, tunable, and enterprise-ready.
