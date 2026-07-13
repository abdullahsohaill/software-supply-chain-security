"""
TC5b: License Choice Interoperability Test
==========================================

Root Cause: Interoperability issues due to licenseChoice flexibility
Specification Section: 4.3.2(3)

The licenseChoice element allows:
- SPDX license ID (e.g., "MIT", "Apache-2.0")
- SPDX license expression (e.g., "MIT OR Apache-2.0")
- Proprietary license name (e.g., "My Company License v1")
- Full license text attachment

This flexibility creates friction for consuming tools expecting standardized SPDX IDs.

Mitigation: Check if licenses use SPDX IDs (interoperable)
Problem: Measure rate of non-SPDX license formats
"""

from typing import Dict, Any, List, Set
from . import BaseTestCase, extract_all_components


SPDX_LICENSE_IDS: Set[str] = {
    "MIT", "Apache-2.0", "GPL-2.0-only", "GPL-2.0-or-later", "GPL-3.0-only", 
    "GPL-3.0-or-later", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0",
    "LGPL-2.1-only", "LGPL-2.1-or-later", "LGPL-3.0-only", "LGPL-3.0-or-later",
    "AGPL-3.0-only", "AGPL-3.0-or-later", "Unlicense", "CC0-1.0", "CC-BY-4.0",
    "CC-BY-SA-4.0", "Zlib", "BSL-1.0", "EPL-2.0", "CDDL-1.0", "Artistic-2.0",
    "PostgreSQL", "OFL-1.1", "WTFPL", "0BSD", "BlueOak-1.0.0", "UPL-1.0",
    
    "GPL-2.0", "GPL-3.0", "LGPL-2.1", "LGPL-3.0", "BSD-2-Clause-FreeBSD",
    
    "NOASSERTION", "NONE"
}


class TC5bLicenseChoice(BaseTestCase):
    """Test case for license format interoperability."""
    
    def __init__(self):
        super().__init__("TC5b", "License Choice Interoperability")
    
    def _extract_licenses(self, sbom: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract all license declarations from the SBOM."""
        licenses = []
        
        def process_license_choice(license_data):
            """Process a licenseChoice object."""
            if isinstance(license_data, dict):
                
                if "license" in license_data:
                    lic = license_data["license"]
                    if isinstance(lic, dict):
                        licenses.append(lic)
                    elif isinstance(lic, str):
                        licenses.append({"id": lic})
                
                if "expression" in license_data:
                    licenses.append({"expression": license_data["expression"]})
                
                if "id" in license_data or "name" in license_data:
                    licenses.append(license_data)
            elif isinstance(license_data, list):
                for item in license_data:
                    process_license_choice(item)
        
        
        metadata = sbom.get("metadata", {})
        if "licenses" in metadata:
            process_license_choice(metadata["licenses"])
        
        
        components = extract_all_components(sbom)
        for comp in components:
            if "licenses" in comp:
                process_license_choice(comp["licenses"])
        
        return licenses
    
    def _classify_license(self, license_obj: Dict[str, Any]) -> str:
        """
        Classify a license as:
        - 'spdx_id': Uses standard SPDX identifier
        - 'spdx_expression': Uses SPDX expression syntax
        - 'proprietary_name': Uses custom/proprietary name
        - 'text_only': Only has license text, no identifier
        - 'unknown': Cannot classify
        """
        
        if "id" in license_obj:
            lid = license_obj["id"]
            if lid in SPDX_LICENSE_IDS:
                return "spdx_id"
            
            if lid and "-" in lid and lid[0].isupper():
                return "spdx_id"  
            return "proprietary_name"
        
        
        if "expression" in license_obj:
            expr = license_obj["expression"]
            
            if any(op in expr for op in [" AND ", " OR ", " WITH "]):
                return "spdx_expression"
            
            if expr in SPDX_LICENSE_IDS:
                return "spdx_expression"
            return "proprietary_name"
        
        
        if "name" in license_obj:
            name = license_obj["name"]
            
            if name in SPDX_LICENSE_IDS:
                return "spdx_id"
            return "proprietary_name"
        
        
        if "text" in license_obj:
            return "text_only"
        
        return "unknown"
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check if licenses use SPDX-standardized formats."""
        licenses = self._extract_licenses(sbom)
        
        if not licenses:
            return {
                "present": True,  
                "total_licenses": 0,
                "spdx_rate": 100.0,
                "reason": "No license declarations found"
            }
        
        classifications = [self._classify_license(lic) for lic in licenses]
        
        spdx_count = sum(1 for c in classifications if c in ["spdx_id", "spdx_expression"])
        total = len(classifications)
        spdx_rate = (spdx_count / total) * 100 if total > 0 else 100.0
        
        return {
            "present": spdx_rate >= 80.0,  
            "total_licenses": total,
            "spdx_count": spdx_count,
            "spdx_rate": round(spdx_rate, 1)
        }
    
    def measure_problem(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Measure the severity of license format inconsistency."""
        licenses = self._extract_licenses(sbom)
        
        if not licenses:
            return {
                "severity": 0.0,
                "total_licenses": 0,
                "classification": {},
                "interoperability_score": 100.0,
                "sample_proprietary": []
            }
        
        classifications = [self._classify_license(lic) for lic in licenses]
        
        
        from collections import Counter
        class_counts = Counter(classifications)
        
        
        
        interoperable = class_counts.get("spdx_id", 0) + class_counts.get("spdx_expression", 0)
        total = len(classifications)
        
        interop_score = (interoperable / total) * 100 if total > 0 else 100.0
        
        
        severity = 1.0 - (interoperable / total) if total > 0 else 0.0
        
        
        proprietary_samples = []
        for i, lic in enumerate(licenses):
            if classifications[i] == "proprietary_name":
                name = lic.get("name") or lic.get("id") or lic.get("expression", "unknown")
                if name not in proprietary_samples and len(proprietary_samples) < 5:
                    proprietary_samples.append(name)
        
        return {
            "severity": severity,
            "total_licenses": total,
            "classification": dict(class_counts),
            "interoperability_score": round(interop_score, 1),
            "sample_proprietary": proprietary_samples
        }
