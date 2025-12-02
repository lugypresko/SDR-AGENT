"""
CSE Configuration Module
Stores Weight Profiles, Normalization Boundaries, Penalty Rules, and Versioning.
"""

# ===== VERSIONING =====
SCORING_VERSION = "1.0.0"
EXPLAINABILITY_VERSION = "1.0.0"
CONFIG_VERSION = "1.0.0"
CSE_ENGINE_VERSION = "1.0.0"

# ===== WEIGHT PROFILES =====
# Multiple profiles allow A/B testing and experimentation
WEIGHT_PROFILES = {
    "v1": {
        "enrichment_quality": 0.15,
        "stress_signals": 0.20,
        "pain_strength": 0.25,
        "angle_relevance": 0.15,
        "personalization_depth": 0.10,
        "domain_complexity": 0.05,
        "org_health": 0.05,
        "email_quality": 0.05,
    },
    "v2": {
        "enrichment_quality": 0.10,
        "stress_signals": 0.25,
        "pain_strength": 0.30,
        "angle_relevance": 0.15,
        "personalization_depth": 0.10,
        "domain_complexity": 0.05,
        "org_health": 0.03,
        "email_quality": 0.02,
    },
    "experimental": {
        "enrichment_quality": 0.20,
        "stress_signals": 0.15,
        "pain_strength": 0.20,
        "angle_relevance": 0.20,
        "personalization_depth": 0.15,
        "domain_complexity": 0.05,
        "org_health": 0.03,
        "email_quality": 0.02,
    }
}

# Active profile (can be switched for A/B testing)
ACTIVE_WEIGHT_PROFILE = "v1"

# ===== NORMALIZATION BOUNDARIES =====
NORMALIZATION_RULES = {
    "headcount": {"min": 0, "max": 10000, "expected": 100},
    "open_roles_ratio": {"min": 0.0, "max": 0.5, "expected": 0.1},
    "pain_strength": {"min": 0.0, "max": 1.0, "expected": 0.5},
    "personalization_depth": {"min": 0.0, "max": 1.0, "expected": 0.7},
    "domain_complexity": {"min": 0.0, "max": 1.0, "expected": 0.5},
}

# ===== CONFLICT RULES =====
CONFLICT_DEFINITIONS = {
    "size_vs_pain": {
        "description": "Startup size but Enterprise pain",
        "severity": "moderate",
        "penalty": 0.15,
    },
    "complexity_vs_personalization": {
        "description": "High complexity but weak personalization",
        "severity": "minor",
        "penalty": 0.10,
    },
    "churn_vs_org_health": {
        "description": "High churn but healthy org signal",
        "severity": "severe",
        "penalty": 0.25,
    },
}

# ===== PENALTY RULES =====
PENALTY_RULES = {
    "missing_enrichment": 0.10,
    "missing_pain": 0.20,
    "missing_angle": 0.15,
    "low_confidence": 0.10,
}

# ===== TIER THRESHOLDS =====
TIER_THRESHOLDS = {
    "A": 80,  # High-potential, immediate send
    "B": 55,  # Good leads, queue
    "C": 0,   # Optional or deprioritized
}

# ===== CONFIDENCE COMPOSITION WEIGHTS =====
CONFIDENCE_WEIGHTS = {
    "availability": 0.30,
    "agreement": 0.20,
    "consistency": 0.25,
    "quality": 0.15,
    "conflict_penalty": 0.10,
}

# ===== PERFORMANCE CONSTRAINTS =====
MAX_CSE_LATENCY_MS = 20  # CSE must add < 20ms per lead

# ===== FALLBACK RULES =====
# Define behavior when agents fail or return incomplete data
FALLBACK_RULES = {
    "missing_brightdata": {
        "penalty": 0.15,
        "default_headcount": 100,
        "default_open_roles": 0,
        "default_industry": "Unknown"
    },
    "missing_pain": {
        "penalty": 0.20,
        "default_pain": "execution friction",
        "default_candidates": ["execution friction"]
    },
    "missing_angle": {
        "penalty": 0.15,
        "default_angle": "Execution Velocity",
        "default_candidates": ["Execution Velocity"]
    },
    "missing_email": {
        "penalty": 0.10,
        "default_personalization": 0.3,
        "default_tone": "professional"
    }
}
