"""
TC7: Composition Completeness Test
==================================

Root Cause: View of SBOMs as unnecessary and merely a compliance checkbox
Specification Section: 4.3.2(7)

Mitigation: Check for compositions with aggregate completeness assertion
Problem: Measure percentage of unknown/incomplete composition types
"""

from typing import Dict, Any, List
from collections import Counter
from . import BaseTestCase


class TC7Composition(BaseTestCase):
    """Test case for composition completeness assertions."""
    
    
    COMPLETE_TYPES = ["complete", "first_party_only", "third_party_only"]
    INCOMPLETE_TYPES = ["incomplete", "incomplete_first_party_only", 
                        "incomplete_third_party_only", "unknown", "not_specified"]
    
    def __init__(self):
        super().__init__("TC7", "Composition Completeness")
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check if SBOM declares its completeness."""
        compositions = sbom.get("compositions", [])
        
        if not compositions:
            return {
                "present": False,
                "has_compositions": False,
                "aggregate_types": [],
                "declares_complete": False
            }
        
        aggregate_types = []
        declares_complete = False
        
        for comp in compositions:
            if isinstance(comp, dict):
                agg = comp.get("aggregate", "unknown")
                aggregate_types.append(agg)
                if agg in self.COMPLETE_TYPES:
                    declares_complete = True
        
        return {
            "present": len(compositions) > 0,
            "has_compositions": True,
            "aggregate_types": aggregate_types,
            "declares_complete": declares_complete
        }
    
    def measure_problem(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Measure the level of 'checkbox compliance'."""
        compositions = sbom.get("compositions", [])
        
        if not compositions:
            
            return {
                "severity": 1.0,
                "total_compositions": 0,
                "complete_count": 0,
                "incomplete_count": 0,
                "unknown_count": 0,
                "completeness_rate": 0.0,
                "checkbox_compliance": True
            }
        
        aggregate_counts = Counter()
        for comp in compositions:
            if isinstance(comp, dict):
                agg = comp.get("aggregate", "unknown")
                aggregate_counts[agg] += 1
        
        complete_count = sum(aggregate_counts.get(t, 0) for t in self.COMPLETE_TYPES)
        incomplete_count = sum(aggregate_counts.get(t, 0) for t in self.INCOMPLETE_TYPES)
        total = len(compositions)
        
        
        if total > 0:
            completeness_rate = complete_count / total
        else:
            completeness_rate = 0.0
        
        
        checkbox_compliance = completeness_rate < 0.5
        
        
        severity = 1.0 - completeness_rate
        
        return {
            "severity": severity,
            "total_compositions": total,
            "complete_count": complete_count,
            "incomplete_count": incomplete_count,
            "aggregate_distribution": dict(aggregate_counts),
            "completeness_rate": round(completeness_rate * 100, 1),
            "checkbox_compliance": checkbox_compliance
        }
