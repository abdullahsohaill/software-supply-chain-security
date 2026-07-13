"""
TC1: CISA Compliance Test
=========================

Root Cause: Failure to meet CISA minimum elements
Specification Section: 4.3.2(1)

Mitigation: Check for presence of metadata.supplier, metadata.timestamp, metadata.authors
Problem: Calculate percentage of CISA minimum elements present
"""

from typing import Dict, Any, List
from . import BaseTestCase, extract_all_components


class TC1CISACompliance(BaseTestCase):
    """Test case for CISA Minimum Elements compliance."""
    
    
    CISA_ELEMENTS = [
        "supplier_name",      
        "component_name",     
        "component_version",  
        "unique_identifier",  
        "dependency_rel",     
        "author",             
        "timestamp"           
    ]
    
    def __init__(self):
        super().__init__("TC1", "CISA Minimum Elements Compliance")
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check if SBOM has key CISA fields with robust validation."""
        metadata = sbom.get("metadata", {})
        
        
        has_supplier = False
        if "supplier" in metadata and isinstance(metadata["supplier"], dict):
            name = metadata["supplier"].get("name", "").strip()
            
            has_supplier = bool(name) and name.lower() != "organization"
            
        
        if not has_supplier and "component" in metadata:
            comp = metadata["component"]
            if isinstance(comp, dict) and "supplier" in comp:
                name = comp.get("supplier", {}).get("name", "").strip()
                has_supplier = bool(name)
        
        
        has_timestamp = bool(metadata.get("timestamp"))
        
        
        has_authors = bool(metadata.get("authors"))
        
        
        
        has_tools = bool(metadata.get("tools"))
        
        return {
            "present": has_supplier and has_timestamp and (has_authors or has_tools),
            "has_supplier": has_supplier,
            "has_timestamp": has_timestamp,
            "has_authors": has_authors,
            "has_tools": has_tools
        }
    
    def measure_problem(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate percentage of CISA elements present."""
        metadata = sbom.get("metadata", {})
        components = sbom.get("components", [])
        dependencies = sbom.get("dependencies", [])
        
        elements_present = 0
        element_status = {}
        
        
        has_supplier = False
        if "supplier" in metadata and isinstance(metadata["supplier"], dict):
             
            name = metadata["supplier"].get("name", "").strip()
            has_supplier = bool(name)
            
        if not has_supplier and "component" in metadata:
            comp = metadata.get("component", {})
            name = comp.get("supplier", {}).get("name", "").strip()
            has_supplier = bool(name)
            
        element_status["supplier_name"] = has_supplier
        if has_supplier:
            elements_present += 1
        
        
        
        
        
        total_comps = len(components)
        comps_with_name = sum(1 for c in components if isinstance(c, dict) and c.get("name"))
        has_comp_name = (comps_with_name / total_comps > 0.9) if total_comps > 0 else True
        
        element_status["component_name"] = has_comp_name
        if has_comp_name:
            elements_present += 1
        
        
        comps_with_ver = sum(1 for c in components if isinstance(c, dict) and c.get("version"))
        has_comp_version = (comps_with_ver / total_comps > 0.9) if total_comps > 0 else True
        
        element_status["component_version"] = has_comp_version
        if has_comp_version:
            elements_present += 1
        
        
        comps_with_id = sum(
            1 for c in components 
            if isinstance(c, dict) and (c.get("purl") or c.get("bom-ref"))
        )
        has_identifier = (comps_with_id / total_comps > 0.9) if total_comps > 0 else True
        
        element_status["unique_identifier"] = has_identifier
        if has_identifier:
            elements_present += 1
        
        
        has_deps = len(dependencies) > 0
        element_status["dependency_rel"] = has_deps
        if has_deps:
            elements_present += 1
        
        
        has_author = bool(metadata.get("authors")) or bool(metadata.get("manufacturer"))
        element_status["author"] = has_author
        if has_author:
            elements_present += 1
        
        
        has_timestamp = bool(metadata.get("timestamp"))
        element_status["timestamp"] = has_timestamp
        if has_timestamp:
            elements_present += 1
        
        total_elements = len(self.CISA_ELEMENTS)
        percentage = (elements_present / total_elements) * 100
        
        
        severity = 1.0 - (elements_present / total_elements)
        
        return {
            "severity": severity,
            "elements_present": elements_present,
            "total_elements": total_elements,
            "percentage": round(percentage, 1),
            "element_status": element_status,
            "components_stats": {
                "total": total_comps,
                "with_name": comps_with_name,
                "with_version": comps_with_ver,
                "with_id": comps_with_id
            }
        }
