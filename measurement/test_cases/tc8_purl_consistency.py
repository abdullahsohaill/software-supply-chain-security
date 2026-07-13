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
from . import BaseTestCase, validate_purl, PackageURL


class TC8PURLConsistency(BaseTestCase):
    """Test case for Package URL consistency."""
    
    
    KNOWN_PURL_TYPES = [
        "npm", "maven", "pypi", "nuget", "gem", "cargo", "composer",
        "golang", "deb", "rpm", "docker", "oci", "github", "bitbucket",
        "generic", "hex", "cocoapods", "swift", "pub", "hackage"
    ]
    
    def __init__(self):
        super().__init__("TC8", "PURL Consistency")
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check if components have valid PURLs using strict validation."""
        components = sbom.get("components", [])
        
        if not components:
            return {
                "present": True,
                "total_components": 0,
                "valid_purls": 0,
                "purl_rate": 100.0,
                "parsing_errors": []
            }
        
        valid_purls = 0
        invalid_purls = []
        parsing_errors = []
        
        for comp in components:
            purl_str = comp.get("purl", "")
            if purl_str:
                is_valid = False
                
                if PackageURL:
                    try:
                        purl = PackageURL.from_string(purl_str)
                        is_valid = True
                        
                        if not purl.type or not purl.name:
                            is_valid = False
                            parsing_errors.append(f"Missing type/name: {purl_str}")
                    except ValueError as e:
                        is_valid = False
                        parsing_errors.append(f"Invalid format: {purl_str} ({str(e)})")
                else:
                    
                    is_valid = validate_purl(purl_str)
                
                if is_valid:
                    valid_purls += 1
                else:
                    invalid_purls.append(purl_str[:100])
        
        total = len(components)
        purl_rate = (valid_purls / total) * 100 if total > 0 else 100.0
        
        return {
            "present": purl_rate >= 95.0,  
            "total_components": total,
            "valid_purls": valid_purls,
            "purl_rate": round(purl_rate, 1),
            "sample_invalid": invalid_purls[:3],
            "parsing_errors_count": len(parsing_errors)
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
        namespace_mismatches = []
        
        for comp in components:
            purl_str = comp.get("purl", "")
            name = comp.get("name", "")
            group = comp.get("group", "")
            
            if purl_str:
                with_purl += 1
                
                purl_type = "unknown"
                purl_ns = ""
                purl_name = ""
                
                if PackageURL:
                    try:
                        purl_obj = PackageURL.from_string(purl_str)
                        purl_type = purl_obj.type
                        purl_ns = purl_obj.namespace
                        purl_name = purl_obj.name
                    except ValueError:
                        pass
                else:
                    
                    match = re.match(r'pkg:([^/]+)/(([^/]+)/)?([^@]+)', purl_str)
                    if match:
                        purl_type = match.group(1)
                        purl_ns = match.group(3) if match.group(3) else ""
                        purl_name = match.group(4)
                
                purl_types[purl_type] += 1
                
                
                if group and purl_ns:
                    if group != purl_ns:
                        
                        if group.replace('.', '/') != purl_ns.replace('.', '/'):
                            namespace_mismatches.append(f"{name}: group='{group}' != purl_ns='{purl_ns}'")
                
                
                if name and purl_name:
                    if name != purl_name:
                        naming_issues.append(f"Name mismatch: '{name}' != '{purl_name}'")
                        
                
                if "@" in name and "npm" not in purl_type and "go" not in purl_type:
                     naming_issues.append(f"Scoped name '{name}' with type '{purl_type}'")

            else:
                with_name_only += 1
        
        total = len(components)
        purl_coverage = with_purl / total if total > 0 else 0.0
        
        
        
        severity = (1.0 - purl_coverage) * 0.6
        
        
        inconsistency_count = len(naming_issues) + len(namespace_mismatches)
        inconsistency_ratio = inconsistency_count / total if total > 0 else 0
        severity += inconsistency_ratio * 0.4
        
        return {
            "severity": min(1.0, severity),
            "total_components": total,
            "with_purl": with_purl,
            "with_name_only": with_name_only,
            "purl_coverage": round(purl_coverage * 100, 1),
            "purl_types": dict(purl_types),
            "naming_issues": naming_issues[:5],
            "namespace_mismatches": namespace_mismatches[:5],
            "total_inconsistencies": inconsistency_count
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
