"""
CSE Explainer Module
Generates deterministic, human-readable explanations.
"""

from typing import Dict, List
from cse.config import TIER_THRESHOLDS

class Explainer:
    """Generates summary and full reasoning explanations"""
    
    def __init__(self):
        pass
        
    def generate_summary(self, 
                        score: float, 
                        tier: str, 
                        primary_pain: str, 
                        selected_angle: str, 
                        confidence: Dict) -> str:
        """
        Generate compact explanation for CSV.
        Format: "Main pain: X. Angle: Y. Evidence: Z. Tier: A (Score: 85)"
        """
        evidence = "Strong signals" if confidence["avg_confidence"] > 0.7 else "Moderate signals"
        
        summary = (
            f"Main pain: {primary_pain}. "
            f"Angle: {selected_angle}. "
            f"Evidence: {evidence}. "
            f"Tier: {tier} (Score: {score:.0f})"
        )
        
        return summary
        
    def generate_full_explanation(self,
                                  normalized_signals: Dict[str, float],
                                  weighted_signals: Dict[str, float],
                                  conflict_report: Dict,
                                  confidence: Dict,
                                  score_breakdown: Dict,
                                  tier: str,
                                  rejected_angles: List[str]) -> Dict:
        """
        Generate complete reasoning tree for trace.
        Returns structured explanation with all reasoning steps.
        """
        explanation = {
            "summary": {
                "final_score": score_breakdown["final_score"],
                "tier": tier,
                "confidence": confidence["avg_confidence"],
                "main_reasoning": self._build_main_reasoning(weighted_signals, confidence)
            },
            "signal_explanations": self._explain_signals(normalized_signals, weighted_signals),
            "conflict_explanations": self._explain_conflicts(conflict_report),
            "penalty_explanations": self._explain_penalties(score_breakdown.get("penalties", {})),
            "confidence_explanations": self._explain_confidence(confidence),
            "tier_justification": self._justify_tier(score_breakdown["final_score"], tier),
            "rejected_alternatives": self._explain_rejected_angles(rejected_angles)
        }
        
        return explanation
        
    def _build_main_reasoning(self, weighted_signals: Dict[str, float], confidence: Dict) -> str:
        """Build main reasoning sentence"""
        top_signal = max(weighted_signals.items(), key=lambda x: x[1])
        conf_level = "high" if confidence["avg_confidence"] > 0.7 else "moderate"
        
        return f"Lead prioritized based on {top_signal[0]} ({conf_level} confidence)"
        
    def _explain_signals(self, normalized: Dict, weighted: Dict) -> List[Dict]:
        """Explain each signal's contribution"""
        explanations = []
        for signal_name, weighted_value in weighted.items():
            explanations.append({
                "signal": signal_name,
                "normalized_value": normalized.get(signal_name, 0.0),
                "weighted_value": weighted_value,
                "contribution": f"{weighted_value * 100:.1f} points"
            })
        return sorted(explanations, key=lambda x: x["weighted_value"], reverse=True)
        
    def _explain_conflicts(self, conflict_report: Dict) -> List[str]:
        """Explain detected conflicts"""
        explanations = []
        for conflict in conflict_report.get("conflicts", []):
            explanations.append(
                f"{conflict['description']} (Penalty: {conflict['penalty'] * 100:.0f} points)"
            )
        return explanations
        
    def _explain_penalties(self, penalties: Dict) -> List[str]:
        """Explain applied penalties"""
        return [f"{reason}: {penalty * 100:.0f} points" for reason, penalty in penalties.items()]
        
    def _explain_confidence(self, confidence: Dict) -> Dict:
        """Explain confidence breakdown"""
        return {
            "availability": f"{confidence['availability'] * 100:.0f}% data completeness",
            "consistency": f"{confidence['consistency'] * 100:.0f}% signal consistency",
            "quality": f"{confidence['quality'] * 100:.0f}% signal strength",
            "justification": confidence["justification"]
        }
        
    def _justify_tier(self, score: float, tier: str) -> str:
        """Justify tier assignment"""
        if tier == "A":
            return f"Score {score:.0f} >= {TIER_THRESHOLDS['A']} (High-potential, immediate send)"
        elif tier == "B":
            return f"Score {score:.0f} >= {TIER_THRESHOLDS['B']} (Good lead, queue)"
        else:
            return f"Score {score:.0f} < {TIER_THRESHOLDS['B']} (Optional or deprioritized)"
            
    def _explain_rejected_angles(self, rejected: List[str]) -> List[str]:
        """Explain why alternatives were rejected"""
        if not rejected:
            return ["No alternative angles considered"]
        return [f"Rejected: {angle} (lower relevance)" for angle in rejected]
