"""
CSE Engine Module
Main coordinator that orchestrates all CSE layers.
"""

import time
from typing import Dict, Any
from cse.schema import RawContext
from cse.config import (
    SCORING_VERSION, EXPLAINABILITY_VERSION, CONFIG_VERSION, CSE_ENGINE_VERSION,
    TIER_THRESHOLDS
)
from cse.provenance import ProvenanceTracker
from cse.normalizer import SignalNormalizer
from cse.conflict_resolver import ConflictResolver
from cse.scorer import LeadScorer
from cse.confidence import ConfidenceCalculator
from cse.explainer import Explainer

class CSEEngine:
    """
    Centralized Signal Engine
    Coordinates all intelligence layers: normalization, conflict resolution,
    scoring, confidence, and explainability.
    """
    
    def __init__(self, weight_profile: str = None):
        self.weight_profile = weight_profile
        self.provenance = ProvenanceTracker()
        self.normalizer = SignalNormalizer(self.provenance)
        self.conflict_resolver = ConflictResolver(self.provenance)
        self.scorer = LeadScorer(self.provenance, weight_profile)
        self.confidence_calculator = ConfidenceCalculator()
        self.explainer = Explainer()
        
    def process(self, raw_context: RawContext) -> Dict[str, Any]:
        """
        Main processing pipeline.
        Takes raw context, returns scored and explained result.
        """
        start_time = time.time()
        
        # Track fallbacks applied
        fallbacks_applied = []
        
        # 1. Record agent outputs in provenance
        self._record_agent_outputs(raw_context)
        
        # 2. Apply fallbacks for missing data
        raw_context = self._apply_fallbacks(raw_context, fallbacks_applied)
        
        # 3. Normalize all signals
        normalized_signals = self._normalize_signals(raw_context)
        
        # 4. Detect conflicts
        conflict_report = self.conflict_resolver.resolve_all(
            normalized_signals,
            raw_context.dict()
        )
        
        # 5. Compute weighted score
        score_breakdown = self.scorer.compute_weighted_score(normalized_signals)
        
        # Apply conflict penalties to score
        final_score = score_breakdown["final_score"] - (conflict_report["total_penalty"] * 100)
        
        # Apply fallback penalties
        fallback_penalty = sum(f["penalty"] for f in fallbacks_applied)
        final_score = final_score - (fallback_penalty * 100)
        
        final_score = max(0, min(100, final_score))
        score_breakdown["final_score"] = final_score
        score_breakdown["fallback_penalty"] = fallback_penalty
        
        # 6. Compute confidence
        confidence = self.confidence_calculator.compute_confidence(
            normalized_signals,
            conflict_report
        )
        
        # Reduce confidence for fallbacks
        if fallbacks_applied:
            confidence["avg_confidence"] = confidence["avg_confidence"] * (1 - fallback_penalty)
            confidence["avg_confidence"] = max(0, confidence["avg_confidence"])
        
        # 7. Determine tier
        tier = self._determine_tier(final_score)
        
        # 8. Generate explanations
        primary_pain = raw_context.pain.primary_pain if raw_context.pain else "Unknown"
        selected_angle = raw_context.angle.selected_angle if raw_context.angle else "Unknown"
        rejected_angles = raw_context.angle.rejected_angles if raw_context.angle else []
        
        summary_explanation = self.explainer.generate_summary(
            final_score, tier, primary_pain, selected_angle, confidence
        )
        
        full_explanation = self.explainer.generate_full_explanation(
            normalized_signals,
            score_breakdown["weighted_signals"],
            conflict_report,
            confidence,
            score_breakdown,
            tier,
            rejected_angles
        )
        
        # 9. Record final score in provenance
        self.provenance.record_final_score(final_score, tier, confidence["avg_confidence"])
        
        # 10. Calculate metrics
        processing_time_ms = (time.time() - start_time) * 1000
        
        # 11. Assemble result
        result = {
            "lead_score": final_score,
            "priority_tier": tier,
            "avg_confidence": confidence["avg_confidence"],
            "min_confidence": confidence["min_confidence"],
            "explanation_summary": summary_explanation,
            "data_quality_flag": "OK" if confidence["avg_confidence"] > 0.6 else "LOW",
            
            # Full trace
            "trace": {
                "lineage": self.provenance.get_lineage(),
                "normalized_signals": normalized_signals,
                "weighted_signals": score_breakdown["weighted_signals"],
                "conflicts": conflict_report,
                "confidence": confidence,
                "score_breakdown": score_breakdown,
                "tier_justification": full_explanation["tier_justification"],
                "full_explanation": full_explanation,
                "fallbacks_applied": fallbacks_applied,
                "metrics": {
                    "processing_time_ms": processing_time_ms,
                    "missing_signals": sum(1 for v in normalized_signals.values() if v < 0.1),
                    "conflict_count": conflict_report["count"],
                    "conflict_severity": conflict_report["severity"],
                    "confidence_variance": confidence["confidence_variance"],
                    "fallback_count": len(fallbacks_applied)
                },
                "versions": {
                    "cse_engine": CSE_ENGINE_VERSION,
                    "scoring": SCORING_VERSION,
                    "explainability": EXPLAINABILITY_VERSION,
                    "config": CONFIG_VERSION
                }
            }
        }
        
        return result
    
    def _apply_fallbacks(self, raw_context: RawContext, fallbacks_applied: list) -> RawContext:
        """Apply fallback logic for missing data"""
        from cse.config import FALLBACK_RULES
        from cse.schema import BrightDataOutput, PainProfilerOutput, AngleRouterOutput, EmailWriterOutput
        
        # Fallback for missing BrightData
        if raw_context.brightdata is None:
            fallbacks_applied.append({
                "agent": "BrightDataEnrichmentAgent",
                "reason": "Agent failed or returned None",
                "penalty": FALLBACK_RULES["missing_brightdata"]["penalty"]
            })
            raw_context.brightdata = BrightDataOutput(
                raw_headcount=FALLBACK_RULES["missing_brightdata"]["default_headcount"],
                raw_open_roles=FALLBACK_RULES["missing_brightdata"]["default_open_roles"],
                raw_industry=FALLBACK_RULES["missing_brightdata"]["default_industry"]
            )
        
        # Fallback for missing Pain
        if raw_context.pain is None or not raw_context.pain.pain_candidates:
            fallbacks_applied.append({
                "agent": "PainProfiler",
                "reason": "No pain candidates identified",
                "penalty": FALLBACK_RULES["missing_pain"]["penalty"]
            })
            raw_context.pain = PainProfilerOutput(
                pain_candidates=FALLBACK_RULES["missing_pain"]["default_candidates"],
                primary_pain=FALLBACK_RULES["missing_pain"]["default_pain"],
                raw_fragments=[],
                pattern_matches={}
            )
        
        # Fallback for missing Angle
        if raw_context.angle is None or not raw_context.angle.selected_angle:
            fallbacks_applied.append({
                "agent": "AngleRouter",
                "reason": "No angle selected",
                "penalty": FALLBACK_RULES["missing_angle"]["penalty"]
            })
            raw_context.angle = AngleRouterOutput(
                candidate_angles=FALLBACK_RULES["missing_angle"]["default_candidates"],
                selected_angle=FALLBACK_RULES["missing_angle"]["default_angle"],
                rejected_angles=[],
                raw_patterns={}
            )
        
        return raw_context
        
    def _record_agent_outputs(self, raw_context: RawContext):
        """Record all agent outputs in provenance"""
        if raw_context.brightdata:
            self.provenance.record_agent_output("BrightDataEnrichmentAgent", 
                                               raw_context.brightdata.dict())
        if raw_context.enrichment:
            self.provenance.record_agent_output("EnrichmentAgent", 
                                               raw_context.enrichment.dict())
        if raw_context.pain:
            self.provenance.record_agent_output("PainProfiler", 
                                               raw_context.pain.dict())
        if raw_context.angle:
            self.provenance.record_agent_output("AngleRouter", 
                                               raw_context.angle.dict())
        if raw_context.email:
            self.provenance.record_agent_output("EmailWriter", 
                                               raw_context.email.dict())
            
    def _normalize_signals(self, raw_context: RawContext) -> Dict[str, float]:
        """Normalize all raw signals to 0-1 scale"""
        normalized = {}
        
        # BrightData signals
        if raw_context.brightdata:
            bd = raw_context.brightdata
            normalized["headcount"] = self.normalizer.normalize("headcount", bd.raw_headcount)
            normalized["stress_signals"] = self.normalizer.normalize_ratio(
                "open_roles_ratio", 
                bd.raw_open_roles, 
                bd.raw_headcount
            )
            
        # Enrichment signals
        if raw_context.enrichment:
            normalized["enrichment_quality"] = 0.7  # Placeholder
            
        # Pain signals
        if raw_context.pain and raw_context.pain.pain_candidates:
            normalized["pain_strength"] = len(raw_context.pain.pain_candidates) / 5.0
            normalized["pain_strength"] = min(1.0, normalized["pain_strength"])
        else:
            normalized["pain_strength"] = 0.0
            
        # Angle signals
        if raw_context.angle and raw_context.angle.selected_angle:
            normalized["angle_relevance"] = 0.8  # Placeholder
        else:
            normalized["angle_relevance"] = 0.0
            
        # Email signals
        if raw_context.email:
            normalized["personalization_depth"] = raw_context.email.personalization_depth or 0.5
            normalized["email_quality"] = 0.7  # Placeholder
        else:
            normalized["personalization_depth"] = 0.0
            normalized["email_quality"] = 0.0
            
        # Domain complexity (placeholder)
        normalized["domain_complexity"] = 0.5
        normalized["org_health"] = 0.7
        
        return normalized
        
    def _determine_tier(self, score: float) -> str:
        """Determine priority tier based on score"""
        if score >= TIER_THRESHOLDS["A"]:
            return "A"
        elif score >= TIER_THRESHOLDS["B"]:
            return "B"
        else:
            return "C"
