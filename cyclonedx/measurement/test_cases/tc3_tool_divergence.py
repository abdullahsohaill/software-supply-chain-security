"""
TC3: Cross-Tool Divergence Test
===============================

Root Cause: Tools employ different methodologies for parsing metadata
Specification Section: 4.3.2(3)

Mitigation: None (specification provides no solution)
Problem: Measure divergence between SBOMs from same artifact using different tools
"""

from typing import Dict, Any, List, Set, Tuple
from . import BaseTestCase, extract_all_components


class TC3ToolDivergence(BaseTestCase):
    """Test case for cross-tool SBOM divergence."""
    
    def __init__(self):
        super().__init__("TC3", "Cross-Tool Divergence")
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """No mitigation exists in the specification."""
        return {
            "present": False,
            "reason": "Specification provides no solution for parsing methodology differences"
        }
    
    def measure_problem(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """
        Measure intrinsic qualities that affect cross-tool consistency.
        Note: Full divergence analysis requires comparing multiple SBOMs.
        This single-SBOM analysis measures factors contributing to divergence.
        """
        components = extract_all_components(sbom)
        
        # Count components with standardized identifiers
        with_purl = sum(1 for c in components if c.get("purl"))
        with_cpe = sum(1 for c in components if c.get("cpe"))
        with_hashes = sum(1 for c in components if c.get("hashes"))
        
        total = len(components)
        
        if total > 0:
            purl_rate = with_purl / total
            cpe_rate = with_cpe / total
            hash_rate = with_hashes / total
            
            # Standardization score (higher = more standardized = less divergence risk)
            standardization = (purl_rate + hash_rate) / 2
        else:
            purl_rate = cpe_rate = hash_rate = standardization = 0.0
        
        # Severity: lower standardization = higher divergence risk
        severity = 1.0 - standardization
        
        return {
            "severity": severity,
            "total_components": total,
            "with_purl": with_purl,
            "with_cpe": with_cpe,
            "with_hashes": with_hashes,
            "purl_rate": round(purl_rate * 100, 1),
            "cpe_rate": round(cpe_rate * 100, 1),
            "hash_rate": round(hash_rate * 100, 1),
            "standardization_score": round(standardization * 100, 1)
        }
    
    @staticmethod
    def compare_sboms(sbom1: Dict[str, Any], sbom2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare two SBOMs and calculate divergence metrics.
        Use this for comparing outputs from different tools on same artifact.
        """
        def extract_identifiers(sbom: Dict[str, Any]) -> Set[Tuple[str, str]]:
            """Extract (name, version) tuples from components."""
            components = sbom.get("components", [])
            identifiers = set()
            for c in components:
                name = c.get("name", "")
                version = c.get("version", "")
                if name:
                    identifiers.add((name, version))
            return identifiers
        
        def extract_purls(sbom: Dict[str, Any]) -> Set[str]:
            """Extract all PURLs from components."""
            components = sbom.get("components", [])
            return {c.get("purl") for c in components if c.get("purl")}
        
        ids1 = extract_identifiers(sbom1)
        ids2 = extract_identifiers(sbom2)
        
        purls1 = extract_purls(sbom1)
        purls2 = extract_purls(sbom2)
        
        # Jaccard similarity for name+version
        if ids1 or ids2:
            jaccard_ids = len(ids1 & ids2) / len(ids1 | ids2)
        else:
            jaccard_ids = 1.0
        
        # Jaccard similarity for PURLs
        if purls1 or purls2:
            jaccard_purls = len(purls1 & purls2) / len(purls1 | purls2)
        else:
            jaccard_purls = 1.0
        
        return {
            "sbom1_components": len(ids1),
            "sbom2_components": len(ids2),
            "common_components": len(ids1 & ids2),
            "unique_to_sbom1": len(ids1 - ids2),
            "unique_to_sbom2": len(ids2 - ids1),
            "jaccard_similarity_ids": round(jaccard_ids, 3),
            "jaccard_similarity_purls": round(jaccard_purls, 3),
            "divergence": round(1 - jaccard_ids, 3)
        }
