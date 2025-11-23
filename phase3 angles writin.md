Phase 3 Instructions: Multi-Angle Writer + Hook Engine

(No code. Implementation to be done by Antigravity.)

Objective

Upgrade the SDR Engine so that email generation becomes signal-driven, angle-aware, and clearly personalized based on the NormalizedLead and AngleSignals created in Phase 2.

The goal of Phase 3 is to move from 2 generic templates to 8 intelligence-driven email archetypes that feel uniquely written for each persona, company stage, and pain pattern.

1. Requirements Overview

Phase 3 introduces:

1. Multi-Angle Email Writer (8 angles)

The writer must support all 8 angles:

Predictability

Execution Velocity

Cross-Team Flow

Prioritization Clarity

Delivery Stability

Strategy-to-Execution Gap

Product Ops Replacement

Multi-Initiative Management

Each angle requires:

A unique voice

A unique problem framing

A unique “aha moment”

A unique CTA

A unique mental model (e.g., “flow debt”, “decision latency”)

The chosen angle comes from the routing signals built in Phase 2.

2. Hook Engine (Lead-Aware Personalization)

This module must generate opening hooks that reflect:

Role

Stage (startup / scaleup / breaking)

Decision-maker level

Complexity level

Identified angle signals

The hook must feel like:

“Someone who knows this world wrote this. Someone who understands my reality.”

Examples (conceptually, not code):

For a VP R&D at a breaking-stage company
→ “Teams move fast but the system doesn’t keep up. That’s when predictability breaks.”

For a CTO at a scale-up
→ “Your org hits the point where alignment becomes more expensive than the code.”

For a Head of Eng in a complex product org
→ “When surface area expands, decision-making slows down unless you constrain the work.”

Hooks must be generated, not templated.

3. Writer Architecture Requirements
3.1 Deterministic Input

EmailWriter must consume:

NormalizedLead

AngleSignals

Chosen Angle

HookSeed (optional)

3.2 Output Contract

EmailWriter must return:

{
  "subject": string,
  "body": string,
  "angle_used": string,
  "tokens": int
}

3.3 Angle-Specific Copy Logic

Each angle must have its own:

Problem articulation

Insight

Mini-story or metaphor

CTA

The copy must be short, sharp, senior-level, and sound like it was written by someone who has been in the room.

4. QA Layer Requirements

The EmailQualityAgent must evolve to:

Enforce minimum structure

Validate tone (senior, not junior)

Enforce clarity

Ensure no repetition

Confirm the email ties back to the selected angle

Verify personalization signals appear in the first 1–2 sentences

If any requirement fails, the email must be automatically rewritten with the same angle.

5. Routing Enhancements

AngleRouter must:

Use the new AngleSignals

Apply deterministic rules

Never fallback to random or LLM decision-making

Include a final catch-all fallback angle (Execution OS)

Routing logic must be fully explainable and logged for debugging.

6. Verification Requirements

The verification suite for Phase 3 must check:

6.1 Completeness

All 8 angles are reachable and produce valid output.

6.2 Determinism

Running the pipeline twice with the same inputs produces identical output.

6.3 Personalization

Emails must show at least:

A reference to stage

A reference to role

A reference to the chosen angle

6.4 Structure Compliance

Verify presence of:

Subject line

Hook

Insight

CTA

6.5 No Degradation from Phase 2

Normalization must remain stable and unchanged.

7. Out of Scope for Phase 3

Keep the plan narrow:

No caching

No tiering

No external LLM adapters

No refactoring of orchestrator

No multi-email sequences

No A/B testing

No HTML output

These belong to Phase 4 and beyond.

8. Final Deliverable for Phase 3

A fully functional pipeline where:

Every lead receives a highly personalized email

The angle is sharply aligned with signals

The hook feels “insider”

The body communicates a real insight

The CTA is senior-level and relevant

The result is deterministic and verifiable
Phase 3 – Open Issues & Mitigation Plan

This phase introduces 8 leadership/ops Angles based on Role × Stage × Complexity signals.
Below are the known risks and the required engineering mitigations.

1. Hook Combinatorics (96+ variants)
Issue

The system requires unique hooks for each combination:

3 roles (CTO / VP R&D / Head of Eng)

4 company stages (Startup / Scaleup / Late-scale / Enterprise)

8 angles

This produces 96 combinations.
We will never write all 96 manually.
Trying to do so will stall the system.

Mitigation: Hierarchical Fallback System

Implement a 3-level lookup:

Exact match: (Role + Stage + Angle)

Partial match: (Stage + Angle)

Default: (Angle)

This ensures:

High personalization when possible

No missing hooks

Deterministic fallback behavior

Zero runtime failures

Status: Mandatory for Phase 3.

2. Routing Conflicts Between Angles
Issue

Leads often match multiple Angles.
Example: A Head of Engineering in a 70-person company could trigger:

Predictability (scaleup stage)

Execution Velocity (delivery pressure)

Team Health (manager overload signals)

Without strict rules, the router becomes chaotic or random.

Mitigation: Strict Priority Hierarchy

Define a fixed priority list:

Predictability

Execution Velocity

Cross-Team Flow

Team Health

Strategic Clarity

Firefighting Spiral

Silent Attrition

Rebuild Trust

Router logic:

Evaluate each angle’s conditions

Select the highest-priority angle that matches

Never choose more than one

Log the match path (for debugging)

This enforces single-angle determinism.

3. Tone Validation Without LLMs
Issue

In Phase 3, QA must validate tone deterministically (LLM-free).
Detecting a “senior, Israeli-direct, technical” tone is not possible with regex alone.

Mitigation: Two-Tier Tone Guardrail System
A. Negative Keyword Filter (Disqualifies tone)

Reject if email contains:

“Hope you are well”

“Just checking in”

“I wanted to follow up”

“Best regards”

“Touching base”

“Circle back”

These phrases are banned in Hebrew/Israeli tech communication.

B. Positive Signal Filter (Requires tone)

Email must include at least two of:

“execution”

“alignment”

“delivery pressure”

“bottleneck”

“initiative load”

“cross-team”

“roadmap clarity”

“manager fatigue”

This guarantees the message feels:

senior

technical

operational

direct

Status: These two lists are sufficient for deterministic tone validation.

4. Missing Normalization Signals
Issue

If a lead has incomplete data (no size, no title match), routing breaks.

Mitigation: Safe Normalization Defaults

Missing role → default to senior lead

Missing size → default to scaleup

Missing industry → default to SaaS

Missing signals → NULL-safe fallback ("unknown")

This eliminates pipeline crashes.

5. Email Length Drift
Issue

Angle-based templates may produce emails that drift too long or too short.

Mitigation: Deterministic Length Balancer

Minimum: 90 words

Maximum: 140 words

If <90 → auto-append angle’s “context line”

If >140 → remove lowest-priority lines

This ensures consistent output without LLM involvement.

Summary: What This Achieves

With these mitigation rules, Phase 3 becomes:

Deterministic

Explainable

Extensible

Impossible to break

Free from LLM unpredictability

This is the bare minimum required to evolve into Phase 4 (LLM-enhanced personalization).