Unified System Instructions

Phase 4: LLM Integration + Four Organs Architecture**

This document defines the operational rules, responsibilities, and LLM integration strategy for the Agentic SDR Engine.
It merges the four critical agent “organs” and the Phase 4 LLM infrastructure plan into one coherent set of instructions.

This should be placed in your repo as:

system_instructions.md

I. Purpose of This System

We are building an AI-driven SDR engine that:

understands the lead deeply

diagnoses their hidden pressures

routes them to the correct psychological angle

generates a high-authority email

does all of this deterministically

and scales cheaply with LLM tiering + caching

The system operates as four cooperating organs:

Normalization = The Brain

Router = The Soul

Writer = The Mouth

Quality = The Immune System

Phase 4 introduces the LLM nervous system:
LLMClient + Caching + Tiering.

II. The Four Organs (Functional Identity)

Each organ has ONE job and ONE responsibility.
Any overlap is considered a bug.

1. 🧠 Normalization Layer — “The Brain”

Mission:
Convert raw lead data into structured, predictable signals the system can reason with.

Responsibilities:

Clean messy CSV input

Normalize titles (CTO → executive, VP Eng → executive, Team Lead → manager)

Normalize company size → stage (startup / scaleup / enterprise)

Normalize industry category

Extract angle-relevant signals (pressure, chaos, attrition patterns)

Produce a NormalizedLead object

LLM Usage:
Optional. If needed, use Tier 2 (cheap model) through LLMAdapter.

Golden Rule:
The Brain never guesses emotions.
It only produces facts and signals.

2. 🫀 Angle Router — “The Soul”

Mission:
Decide why we are talking to this lead and which deep psychological angle we should approach.

Responsibilities:

Take NormalizedLead + AngleSignals

Apply deterministic priority rules

Select one of the defined angles:

Predictability Crisis

Execution Velocity

Silent Attrition

Firefighting Spiral

Leadership Drift

Cross-Team Flow

Team Health

Identity Breakdown

LLM Usage:
Never.
The Soul must be deterministic.

Golden Rule:
No guessing.
Only routing based on explicit signals.

3. 👄 Email Writer — “The Mouth”

Mission:
Generate a personalized, angle-aligned, high-authority email that sounds like Itay.

Responsibilities:

Select subject line based on angle

Generate a hook based on (role × stage × angle) with hierarchical fallback

Generate the email body using templates + LLM refinement

Include signature + credibility markers

LLM Usage:
Tier 1 (strong model) through LLMAdapter.

Golden Rule:
The Mouth speaks only after the Brain and Soul have done their jobs.

4. 🛡️ QA Layer — “The Immune System”

Mission:
Protect brand integrity and stop bad emails from reaching the world.

Responsibilities:

Enforce tone rules

Detect red flags (“hope you are well”, “checking in”, softeners)

Ensure the email references the correct angle + signal

Validate length

Fix minor issues; reject major ones

Produce either:

approved_email

rejected_email + reason

LLM Usage:
Optional. Prefer Tier 2 or deterministic checks.

Golden Rule:
If it doesn’t feel like leadership — kill it.

III. LLM Infrastructure (Phase 4)

This is the nervous system connecting all organs.

1. LLMAdapter (Mandatory)

A single entry point for all LLM usage.

Responsibilities:

Accepts prompt + schema

Selects correct tier (Tier 1 or Tier 2)

Pulls from cache (SQLite)

Calls provider

Logs request + response

Returns parsed output

Agents never call LLMs directly.

2. LLMClient

Handles the actual API logic.

API keys

Rate limiting

Error handling

Timeout retries

The Adapter wraps this.

3. Tiering Policy

Tier 1 (expensive):

EmailWriter

Any deep reasoning tasks

Tier 2 (cheap):

Normalization (if needed)

Tone validation

Minor enrichment

Tier 3 (free/local):

Token counting

Formatting

Sanity checks

4. SQLite Caching

Every LLM call must be cached by:

prompt hash

model

schema

Cache hit = no API cost.

Required for both speed & cost control.

5. Logging

All LLM behavior must be logged:

model used

token count

cache hit/miss

raw request + response

error cases

Logs stored in /debug/.

IV. Operational Rules

Orchestrator is immutable

Agents have strict boundaries

No state is shared between agents

Normalization → Router → Writer → QA

No backward flow

No dynamic iteration unless explicitly added in Phase 5

V. Definition of Done for Phase 4

The system is considered complete when:

LLMAdapter is implemented with caching

Tiering policy is fully active

EnrichmentAgent & EmailWriter use LLM tiering

Router & QA remain deterministic

A sample lead produces:

NormalizedLead

Angle

Hook

High-quality email

No contract violations

No drifting tone

No repetitive emails
Architecture Misalignment (Missing LLMAdapter)

Issue:
The architecture doc declares:

“LLMAdapter (Mandatory)… Agents never call LLMs directly.”

But your implementation plan only referenced LLMClient, and did not define the Adapter layer.

This is critical — without an Adapter, the agents will end up calling the LLM layer directly, violating:

tiering

caching

isolation

contract boundaries

Required Fix:
Update implementation_plan.md to explicitly include:

LLMAdapter (high-level API)

Handles prompt → cache → tier selection → LLMClient → parse → return

Visible to agents.

Only public interface allowed.

LLMClient (low-level API)

Performs the actual API call.

Relationship Diagram
Agents  →  LLMAdapter  →  (Cache / Tiering)  →  LLMClient  →  Provider


This maintains the Clean 4-Organ Architecture:

Brain: no LLM (or Tier 2 only via Adapter)

Soul: deterministic, no LLM

Mouth: Tier 1 LLM via Adapter

Immune System: Tier 2 LLM (optional) via Adapter