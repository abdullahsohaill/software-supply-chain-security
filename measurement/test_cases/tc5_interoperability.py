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
    
    
    
    CDX_SPECIFIC_FIELDS = [
        "formulation",
        "declarations", 
        "definitions",
        "compositions",
        "annotations",
        "cryptoProperties",
        "modelCard",
        "data",
        "services",       
        "vulnerabilities", 
        "properties"      
    ]
    
    def __init__(self):
        super().__init__("TC5", "Interoperability")
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check for features that improve interoperability."""
        
        has_formulation = bool(sbom.get("formulation"))
        
        
        has_annotations = bool(sbom.get("annotations"))
        
        
        components = sbom.get("components", [])
        has_ext_refs = any(c.get("externalReferences") for c in components if isinstance(c, dict))
        
        
        has_spdx_props = False
        for comp in components:
            if isinstance(comp, dict):
                props = comp.get("properties", [])
                for p in props:
                    name = p.get("name", "").lower()
                    if "spdx" in name or "concluded" in name or "declared" in name:
                        has_spdx_props = True
                        break
            if has_spdx_props: break
        
        return {
            "present": has_formulation or has_annotations or has_ext_refs,
            "has_formulation": has_formulation,
            "has_annotations": has_annotations,
            "has_spdx_properties": has_spdx_props,
            "has_external_references": has_ext_refs
        }
    
    def measure_problem(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Measure potential data loss in format conversion."""
        
        cdx_specific_count = 0
        cdx_specific_present = []
        
        for field in self.CDX_SPECIFIC_FIELDS:
            if field in sbom and sbom[field]:
                cdx_specific_count += 1
                cdx_specific_present.append(field)
        
        
        components = sbom.get("components", [])
        total_comps = len(components)
        
        comp_with_modelcard = sum(1 for c in components if c.get("modelCard"))
        comp_with_crypto = sum(1 for c in components if c.get("cryptoProperties"))
        comp_with_data = sum(1 for c in components if c.get("data"))
        comp_with_evidence = sum(1 for c in components if c.get("evidence"))
        
        
        
        if len(self.CDX_SPECIFIC_FIELDS) > 0:
            risk = cdx_specific_count / len(self.CDX_SPECIFIC_FIELDS)
        else:
            risk = 0.0
        
        
        if total_comps > 0:
            
            component_risk = (comp_with_modelcard + comp_with_crypto + comp_with_data + comp_with_evidence) / (total_comps * 4)
            
            risk = (risk * 0.4) + (component_risk * 0.6)
        
        return {
            "severity": min(1.0, risk),
            "cdx_specific_fields": cdx_specific_count,
            "cdx_fields_present": cdx_specific_present,
            "components_with_modelcard": comp_with_modelcard,
            "components_with_crypto": comp_with_crypto,
            "components_with_data": comp_with_data,
            "components_with_evidence": comp_with_evidence,
            "potential_loss_risk": round(risk * 100, 1)
        }
