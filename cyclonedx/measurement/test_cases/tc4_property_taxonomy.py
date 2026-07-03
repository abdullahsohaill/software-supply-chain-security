"""
TC4: Property Taxonomy Adherence Test
=====================================

Root Cause: Lack of standardized metadata formats
Specification Section: 4.3.2(4)

Mitigation: Check if properties use registered taxonomy (cdx: prefix)
Problem: Count ad-hoc vs registered property names
"""

from typing import Dict, Any, List
from collections import Counter
from . import BaseTestCase, extract_all_properties


class TC4PropertyTaxonomy(BaseTestCase):
    """Test case for property taxonomy adherence."""
    
    
    REGISTERED_PREFIXES = [
        "cdx:",           
        "cyclonedx:",     
        "spdx:",          
        "aquasecurity:",  
        "syft:",          
        "snyk:",          
    ]
    
    def __init__(self):
        super().__init__("TC4", "Property Taxonomy Adherence")
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check if SBOM uses registered property namespaces."""
        properties = extract_all_properties(sbom)
        
        if not properties:
            return {
                "present": True,  
                "total_properties": 0,
                "registered_count": 0,
                "registration_rate": 100.0
            }
        
        registered = 0
        for prop in properties:
            name = prop.get("name", "")
            if any(name.startswith(prefix) for prefix in self.REGISTERED_PREFIXES):
                registered += 1
        
        rate = (registered / len(properties)) * 100 if properties else 100.0
        
        return {
            "present": rate >= 50.0,  
            "total_properties": len(properties),
            "registered_count": registered,
            "registration_rate": round(rate, 1)
        }
    
    def measure_problem(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Measure property fragmentation and ad-hoc usage."""
        properties = extract_all_properties(sbom)
        
        if not properties:
            return {
                "severity": 0.0,
                "total_properties": 0,
                "unique_names": 0,
                "adhoc_properties": 0,
                "fragmentation_score": 0.0
            }
        
        
        name_counts = Counter(p.get("name", "") for p in properties)
        unique_names = len(name_counts)
        
        
        registered = []
        adhoc = []
        
        for prop in properties:
            name = prop.get("name", "")
            if any(name.startswith(prefix) for prefix in self.REGISTERED_PREFIXES):
                registered.append(name)
            else:
                adhoc.append(name)
        
        
        adhoc_unique = len(set(adhoc))
        
        
        fragmentation = len(adhoc) / len(properties) if properties else 0.0
        
        
        severity = fragmentation
        
        return {
            "severity": severity,
            "total_properties": len(properties),
            "unique_names": unique_names,
            "registered_properties": len(registered),
            "adhoc_properties": len(adhoc),
            "adhoc_unique_patterns": adhoc_unique,
            "fragmentation_score": round(fragmentation * 100, 1),
            "sample_adhoc": list(set(adhoc))[:5]  
        }
