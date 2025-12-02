"""
CSE Provenance Module
Tracks data lineage: Agent -> Raw -> Normalized -> Weighted -> Score
"""

from datetime import datetime
from typing import Dict, Any, List

class ProvenanceTracker:
    """Tracks the complete lineage of signals through the CSE pipeline"""
    
    def __init__(self):
        self.lineage = []
        
    def record_agent_output(self, agent_name: str, raw_data: Dict[str, Any], version: str = "1.0.0"):
        """Record raw output from an agent"""
        self.lineage.append({
            "stage": "agent_output",
            "agent": agent_name,
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "data": raw_data
        })
        
    def record_normalization(self, signal_name: str, raw_value: Any, normalized_value: float):
        """Record a normalization transformation"""
        self.lineage.append({
            "stage": "normalization",
            "signal": signal_name,
            "raw_value": raw_value,
            "normalized_value": normalized_value,
            "timestamp": datetime.now().isoformat()
        })
        
    def record_weighting(self, signal_name: str, normalized_value: float, weight: float, weighted_value: float):
        """Record a weighting transformation"""
        self.lineage.append({
            "stage": "weighting",
            "signal": signal_name,
            "normalized_value": normalized_value,
            "weight": weight,
            "weighted_value": weighted_value,
            "timestamp": datetime.now().isoformat()
        })
        
    def record_penalty(self, signal_name: str, original_value: float, penalty: float, adjusted_value: float, reason: str):
        """Record a penalty adjustment"""
        self.lineage.append({
            "stage": "penalty",
            "signal": signal_name,
            "original_value": original_value,
            "penalty": penalty,
            "adjusted_value": adjusted_value,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        
    def record_final_score(self, score: float, tier: str, confidence: float):
        """Record the final score and tier"""
        self.lineage.append({
            "stage": "final_score",
            "score": score,
            "tier": tier,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        })
        
    def get_lineage(self) -> List[Dict[str, Any]]:
        """Get the complete lineage"""
        return self.lineage
        
    def get_derivation_chain(self, signal_name: str) -> List[Dict[str, Any]]:
        """Get the derivation chain for a specific signal"""
        return [entry for entry in self.lineage if entry.get("signal") == signal_name]
