"""
CSE Normalizer Module
Transforms raw signals to 0-1 scale with clipping, outlier handling, and missing value logic.
"""

from typing import Any, Optional
from cse.config import NORMALIZATION_RULES
from cse.provenance import ProvenanceTracker

class SignalNormalizer:
    """Normalizes raw signals to 0-1 scale"""
    
    def __init__(self, provenance: ProvenanceTracker):
        self.provenance = provenance
        
    def normalize(self, signal_name: str, raw_value: Any) -> float:
        """
        Normalize a raw value to 0-1 scale.
        Handles clipping, outliers, and missing values.
        """
        # Handle missing values
        if raw_value is None:
            normalized = 0.0
            self.provenance.record_normalization(signal_name, None, normalized)
            return normalized
            
        # Get normalization rules
        rules = NORMALIZATION_RULES.get(signal_name, {})
        min_val = rules.get("min", 0)
        max_val = rules.get("max", 1)
        
        # Convert to float if possible
        try:
            numeric_value = float(raw_value)
        except (ValueError, TypeError):
            # Non-numeric value, return 0
            normalized = 0.0
            self.provenance.record_normalization(signal_name, raw_value, normalized)
            return normalized
            
        # Clip to boundaries
        clipped_value = max(min_val, min(max_val, numeric_value))
        
        # Normalize to 0-1
        if max_val == min_val:
            normalized = 0.5  # Avoid division by zero
        else:
            normalized = (clipped_value - min_val) / (max_val - min_val)
            
        # Record the transformation
        self.provenance.record_normalization(signal_name, raw_value, normalized)
        
        return normalized
        
    def normalize_ratio(self, signal_name: str, numerator: Optional[int], denominator: Optional[int]) -> float:
        """Normalize a ratio (e.g., open_roles / headcount)"""
        if numerator is None or denominator is None or denominator == 0:
            normalized = 0.0
            self.provenance.record_normalization(signal_name, f"{numerator}/{denominator}", normalized)
            return normalized
            
        ratio = numerator / denominator
        return self.normalize(signal_name, ratio)
        
    def normalize_categorical(self, signal_name: str, raw_value: Optional[str], category_weights: dict) -> float:
        """Normalize a categorical value using predefined weights"""
        if raw_value is None:
            normalized = 0.0
        else:
            normalized = category_weights.get(raw_value.lower(), 0.5)
            
        self.provenance.record_normalization(signal_name, raw_value, normalized)
        return normalized
