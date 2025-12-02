"""
CSE Conflict Resolver Module
Detects contradictions and assigns penalties.
"""

from typing import Dict, List, Tuple
from cse.config import CONFLICT_DEFINITIONS
from cse.provenance import ProvenanceTracker

class ConflictResolver:
    """Detects and resolves signal contradictions"""
    
    def __init__(self, provenance: ProvenanceTracker):
        self.provenance = provenance
        self.conflicts = []
        
    def check_size_vs_pain(self, headcount: int, pain_type: str) -> Tuple[bool, float, str]:
        """Check for contradiction between company size and pain type"""
        is_startup = headcount < 50
        is_enterprise_pain = "enterprise" in pain_type.lower() or "scale" in pain_type.lower()
        
        if is_startup and is_enterprise_pain:
            conflict_def = CONFLICT_DEFINITIONS["size_vs_pain"]
            return True, conflict_def["penalty"], conflict_def["description"]
        return False, 0.0, ""
        
    def check_complexity_vs_personalization(self, complexity: float, personalization: float) -> Tuple[bool, float, str]:
        """Check for contradiction between complexity and personalization depth"""
        if complexity > 0.7 and personalization < 0.4:
            conflict_def = CONFLICT_DEFINITIONS["complexity_vs_personalization"]
            return True, conflict_def["penalty"], conflict_def["description"]
        return False, 0.0, ""
        
    def resolve_all(self, normalized_signals: Dict[str, float], raw_context: dict) -> Dict[str, any]:
        """
        Detect all conflicts and return conflict report.
        Returns: {
            "conflicts": [...],
            "total_penalty": float,
            "severity": "minor" | "moderate" | "severe"
        }
        """
        conflicts_found = []
        total_penalty = 0.0
        max_severity = "none"
        
        # Check size vs pain
        headcount = raw_context.get("brightdata", {}).get("raw_headcount", 100)
        pain_type = raw_context.get("pain", {}).get("primary_pain", "")
        
        has_conflict, penalty, description = self.check_size_vs_pain(headcount, pain_type)
        if has_conflict:
            conflicts_found.append({
                "type": "size_vs_pain",
                "description": description,
                "penalty": penalty,
                "severity": "moderate"
            })
            total_penalty += penalty
            max_severity = "moderate"
            
        # Check complexity vs personalization
        complexity = normalized_signals.get("domain_complexity", 0.5)
        personalization = normalized_signals.get("personalization_depth", 0.5)
        
        has_conflict, penalty, description = self.check_complexity_vs_personalization(complexity, personalization)
        if has_conflict:
            conflicts_found.append({
                "type": "complexity_vs_personalization",
                "description": description,
                "penalty": penalty,
                "severity": "minor"
            })
            total_penalty += penalty
            if max_severity == "none":
                max_severity = "minor"
                
        self.conflicts = conflicts_found
        
        return {
            "conflicts": conflicts_found,
            "total_penalty": total_penalty,
            "severity": max_severity,
            "count": len(conflicts_found)
        }
        
    def get_conflicts(self) -> List[Dict]:
        """Get all detected conflicts"""
        return self.conflicts
