"""
CSE Confidence Module
Computes composite confidence from availability, agreement, consistency, and quality.
"""

from typing import Dict
from cse.config import CONFIDENCE_WEIGHTS

class ConfidenceCalculator:
    """Computes composite confidence score"""
    
    def __init__(self):
        self.weights = CONFIDENCE_WEIGHTS
        
    def compute_confidence(self, normalized_signals: Dict[str, float], conflict_report: Dict) -> Dict[str, any]:
        """
        Compute composite confidence.
        Returns: {
            "availability": float,
            "agreement": float,
            "consistency": float,
            "quality": float,
            "conflict_penalty": float,
            "avg_confidence": float,
            "min_confidence": float,
            "confidence_variance": float,
            "justification": str
        }
        """
        # 1. Availability: How many signals are present?
        total_signals = len(normalized_signals)
        present_signals = sum(1 for v in normalized_signals.values() if v > 0.1)
        availability = present_signals / total_signals if total_signals > 0 else 0.0
        
        # 2. Agreement: For now, assume single source (no disagreement)
        agreement = 1.0  # Will be enhanced when multiple sources exist
        
        # 3. Consistency: Are signals internally consistent?
        consistency = 1.0 - (conflict_report.get("total_penalty", 0.0))
        consistency = max(0.0, consistency)
        
        # 4. Quality: Average signal strength
        quality = sum(normalized_signals.values()) / len(normalized_signals) if normalized_signals else 0.0
        
        # 5. Conflict penalty
        conflict_penalty = conflict_report.get("total_penalty", 0.0)
        
        # Compute weighted average confidence
        avg_confidence = (
            availability * self.weights["availability"] +
            agreement * self.weights["agreement"] +
            consistency * self.weights["consistency"] +
            quality * self.weights["quality"] -
            conflict_penalty * self.weights["conflict_penalty"]
        )
        avg_confidence = max(0.0, min(1.0, avg_confidence))
        
        # Min confidence (most conservative)
        min_confidence = min(availability, agreement, consistency, quality)
        
        # Variance
        confidences = [availability, agreement, consistency, quality]
        mean = sum(confidences) / len(confidences)
        variance = sum((c - mean) ** 2 for c in confidences) / len(confidences)
        
        # Justification
        justification = self._build_justification(availability, consistency, quality, conflict_report)
        
        return {
            "availability": availability,
            "agreement": agreement,
            "consistency": consistency,
            "quality": quality,
            "conflict_penalty": conflict_penalty,
            "avg_confidence": avg_confidence,
            "min_confidence": min_confidence,
            "confidence_variance": variance,
            "justification": justification
        }
        
    def _build_justification(self, availability: float, consistency: float, quality: float, conflict_report: Dict) -> str:
        """Build human-readable confidence justification"""
        reasons = []
        
        if availability < 0.5:
            reasons.append("Low data availability")
        if consistency < 0.7:
            reasons.append(f"{conflict_report.get('count', 0)} conflicts detected")
        if quality < 0.5:
            reasons.append("Weak signal strength")
            
        if not reasons:
            return "High confidence: Complete data, no conflicts, strong signals"
        else:
            return "Reduced confidence: " + ", ".join(reasons)
