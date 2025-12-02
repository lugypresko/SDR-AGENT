"""
CSE Scorer Module
Computes weighted scores with caps and penalties.
"""

from typing import Dict
from cse.config import WEIGHT_PROFILES, ACTIVE_WEIGHT_PROFILE, PENALTY_RULES
from cse.provenance import ProvenanceTracker

class LeadScorer:
    """Computes final lead score from weighted normalized signals"""
    
    def __init__(self, provenance: ProvenanceTracker, weight_profile: str = None):
        self.provenance = provenance
        self.weight_profile = weight_profile or ACTIVE_WEIGHT_PROFILE
        self.weights = WEIGHT_PROFILES[self.weight_profile]
        
    def compute_weighted_score(self, normalized_signals: Dict[str, float]) -> Dict[str, any]:
        """
        Compute weighted score from normalized signals.
        Returns: {
            "weighted_signals": {...},
            "raw_score": float,
            "penalties": {...},
            "final_score": float
        }
        """
        weighted_signals = {}
        raw_score = 0.0
        
        # Apply weights to each signal
        for signal_name, weight in self.weights.items():
            normalized_value = normalized_signals.get(signal_name, 0.0)
            weighted_value = normalized_value * weight
            weighted_signals[signal_name] = weighted_value
            raw_score += weighted_value
            
            # Record weighting in provenance
            self.provenance.record_weighting(
                signal_name, 
                normalized_value, 
                weight, 
                weighted_value
            )
            
        # Convert to 0-100 scale
        raw_score = raw_score * 100
        
        # Apply penalties
        penalties = self._compute_penalties(normalized_signals)
        total_penalty = sum(penalties.values())
        
        # Final score with penalties
        final_score = max(0, raw_score - (total_penalty * 100))
        
        return {
            "weighted_signals": weighted_signals,
            "raw_score": raw_score,
            "penalties": penalties,
            "total_penalty": total_penalty,
            "final_score": final_score
        }
        
    def _compute_penalties(self, normalized_signals: Dict[str, float]) -> Dict[str, float]:
        """Compute penalties for missing or weak signals"""
        penalties = {}
        
        # Missing enrichment penalty
        if normalized_signals.get("enrichment_quality", 0) < 0.3:
            penalties["missing_enrichment"] = PENALTY_RULES["missing_enrichment"]
            
        # Missing pain penalty
        if normalized_signals.get("pain_strength", 0) < 0.2:
            penalties["missing_pain"] = PENALTY_RULES["missing_pain"]
            
        # Missing angle penalty
        if normalized_signals.get("angle_relevance", 0) < 0.2:
            penalties["missing_angle"] = PENALTY_RULES["missing_angle"]
            
        return penalties
