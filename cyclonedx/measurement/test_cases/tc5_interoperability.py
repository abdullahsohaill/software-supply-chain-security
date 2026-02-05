"""
TC5: Interoperability Test
==========================

Root Cause: Interoperability issues between formats
Specification Section: 4.3.2(5)

Mitigation: Check for formulation presence (enables round-trip fidelity)
Problem: Measure potential data loss indicators
"""

from typing import Dict, Any, List
from . import BaseTestCase


class TC5Interoperability(BaseTestCase):
    """Test case for format interoperability."""
    
    # Fields that are CycloneDX-specific and may be lost in conversion
    CDX_SPECIFIC_FIELDS = [
        "formulation",
        "declarations", 
        "definitions",
        "compositions",
        "annotations",
        "cryptoProperties",
        "modelCard",
        "data"
    ]
    
    def __init__(self):
        super().__init__("TC5", "Interoperability")
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check for features that improve interoperability."""
        # Formulation enables better round-trip
        has_formulation = bool(sbom.get("formulation"))
        
        # Check for annotations (can carry conversion notes)
        has_annotations = bool(sbom.get("annotations"))
        
        # Check for properties that might be for SPDX compat
        has_spdx_props = False
        components = sbom.get("components", [])
        for comp in components:
            props = comp.get("properties", [])
            for p in props:
                if "spdx" in p.get("name", "").lower():
                    has_spdx_props = True
                    break
        
        return {
            "present": has_formulation or has_annotations,
            "has_formulation": has_formulation,
            "has_annotations": has_annotations,
            "has_spdx_properties": has_spdx_props
        }
    
    def measure_problem(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Measure potential data loss in format conversion."""
        # Count CycloneDX-specific fields that would be lost in SPDX
        cdx_specific_count = 0
        cdx_specific_present = []
        
        for field in self.CDX_SPECIFIC_FIELDS:
            if field in sbom and sbom[field]:
                cdx_specific_count += 1
                cdx_specific_present.append(field)
        
        # Check components for CDX-specific features
        components = sbom.get("components", [])
        comp_with_modelcard = sum(1 for c in components if c.get("modelCard"))
        comp_with_crypto = sum(1 for c in components if c.get("cryptoProperties"))
        comp_with_data = sum(1 for c in components if c.get("data"))
        
        # Calculate interop risk (more CDX-specific = higher risk)
        if len(self.CDX_SPECIFIC_FIELDS) > 0:
            risk = cdx_specific_count / len(self.CDX_SPECIFIC_FIELDS)
        else:
            risk = 0.0
        
        # Add component-level risk
        if components:
            component_risk = (comp_with_modelcard + comp_with_crypto + comp_with_data) / len(components)
            risk = (risk + component_risk) / 2
        
        return {
            "severity": risk,
            "cdx_specific_fields": cdx_specific_count,
            "cdx_fields_present": cdx_specific_present,
            "components_with_modelcard": comp_with_modelcard,
            "components_with_crypto": comp_with_crypto,
            "components_with_data": comp_with_data,
            "potential_loss_risk": round(risk * 100, 1)
        }
