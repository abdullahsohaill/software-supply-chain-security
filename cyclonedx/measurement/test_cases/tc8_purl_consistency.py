"""
TC8: Package URL (PURL) Consistency Test
========================================

Root Cause: Inconsistencies in the naming of packages
Specification Section: 4.3.2(8)

Mitigation: Check for valid PURL format
Problem: Measure divergence in package names across tools
"""

from typing import Dict, Any, List
import re
from collections import Counter
from . import BaseTestCase, validate_purl


class TC8PURLConsistency(BaseTestCase):
    """Test case for Package URL consistency."""
    
    # Official PURL types from https://github.com/package-url/purl-spec
    KNOWN_PURL_TYPES = [
        "npm", "maven", "pypi", "nuget", "gem", "cargo", "composer",
        "golang", "deb", "rpm", "docker", "oci", "github", "bitbucket",
        "generic", "hex", "cocoapods", "swift", "pub", "hackage"
    ]
    
    def __init__(self):
        super().__init__("TC8", "PURL Consistency")
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check if components have valid PURLs."""
        components = sbom.get("components", [])
        
        if not components:
            return {
                "present": True,  # No components = no problem
                "total_components": 0,
                "valid_purls": 0,
                "purl_rate": 100.0
            }
        
        valid_purls = 0
        invalid_purls = []
        
        for comp in components:
            purl = comp.get("purl", "")
            if purl:
                if validate_purl(purl):
                    valid_purls += 1
                else:
                    invalid_purls.append(purl[:50])  # Truncate for display
        
        total = len(components)
        purl_rate = (valid_purls / total) * 100 if total > 0 else 100.0
        
        return {
            "present": purl_rate >= 80.0,  # >80% valid = mitigation present
            "total_components": total,
            "valid_purls": valid_purls,
            "purl_rate": round(purl_rate, 1),
            "sample_invalid": invalid_purls[:3]
        }
    
    def measure_problem(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Measure package naming consistency issues."""
        components = sbom.get("components", [])
        
        if not components:
            return {
                "severity": 0.0,
                "total_components": 0,
                "with_purl": 0,
                "with_name_only": 0,
                "purl_types": {}
            }
        
        with_purl = 0
        with_name_only = 0
        purl_types = Counter()
        naming_issues = []
        
        for comp in components:
            purl = comp.get("purl", "")
            name = comp.get("name", "")
            
            if purl:
                with_purl += 1
                # Extract PURL type
                match = re.match(r'pkg:([a-zA-Z][a-zA-Z0-9+.-]*)', purl)
                if match:
                    purl_type = match.group(1)
                    purl_types[purl_type] += 1
                    
                    # Check for common naming issues
                    if "@" in name and "npm" not in purl_type:
                        naming_issues.append(f"Scoped name '{name}' with non-npm type")
            else:
                with_name_only += 1
        
        # Calculate severity based on PURL coverage
        total = len(components)
        purl_coverage = with_purl / total if total > 0 else 0.0
        
        # Lower coverage = higher severity
        severity = 1.0 - purl_coverage
        
        # Check for type consistency (many types = potential issues)
        type_diversity = len(purl_types) / len(self.KNOWN_PURL_TYPES) if purl_types else 0.0
        
        return {
            "severity": severity,
            "total_components": total,
            "with_purl": with_purl,
            "with_name_only": with_name_only,
            "purl_coverage": round(purl_coverage * 100, 1),
            "purl_types": dict(purl_types),
            "type_count": len(purl_types),
            "naming_issues": naming_issues[:5]
        }
    
    @staticmethod
    def compare_purl_naming(sbom1: Dict[str, Any], sbom2: Dict[str, Any]) -> Dict[str, Any]:
        """Compare PURL naming between two SBOMs of the same artifact."""
        def extract_purls_with_names(sbom):
            result = {}
            for comp in sbom.get("components", []):
                name = comp.get("name", "")
                version = comp.get("version", "")
                purl = comp.get("purl", "")
                key = f"{name}@{version}"
                result[key] = purl
            return result
        
        purls1 = extract_purls_with_names(sbom1)
        purls2 = extract_purls_with_names(sbom2)
        
        common_keys = set(purls1.keys()) & set(purls2.keys())
        purl_matches = 0
        purl_mismatches = []
        
        for key in common_keys:
            if purls1[key] == purls2[key]:
                purl_matches += 1
            else:
                purl_mismatches.append({
                    "component": key,
                    "purl1": purls1[key],
                    "purl2": purls2[key]
                })
        
        if common_keys:
            consistency_rate = purl_matches / len(common_keys)
        else:
            consistency_rate = 0.0
        
        return {
            "common_components": len(common_keys),
            "purl_matches": purl_matches,
            "purl_mismatches": len(purl_mismatches),
            "consistency_rate": round(consistency_rate * 100, 1),
            "sample_mismatches": purl_mismatches[:5]
        }
