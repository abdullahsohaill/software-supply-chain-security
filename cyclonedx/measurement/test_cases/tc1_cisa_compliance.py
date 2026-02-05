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
    
    # CISA Minimum Elements for CycloneDX
    CISA_ELEMENTS = [
        "supplier_name",      # metadata.supplier.name OR component.supplier.name
        "component_name",     # components[].name
        "component_version",  # components[].version
        "unique_identifier",  # components[].purl OR bom-ref
        "dependency_rel",     # dependencies[]
        "author",             # metadata.authors OR metadata.manufacturer
        "timestamp"           # metadata.timestamp
    ]
    
    def __init__(self):
        super().__init__("TC1", "CISA Minimum Elements Compliance")
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check if SBOM has key CISA fields."""
        metadata = sbom.get("metadata", {})
        
        # Check supplier
        has_supplier = False
        if "supplier" in metadata and isinstance(metadata["supplier"], dict):
            has_supplier = bool(metadata["supplier"].get("name"))
        # Also check in root component
        if not has_supplier and "component" in metadata:
            comp = metadata["component"]
            if isinstance(comp, dict) and "supplier" in comp:
                has_supplier = bool(comp.get("supplier", {}).get("name"))
        
        # Check timestamp
        has_timestamp = bool(metadata.get("timestamp"))
        
        # Check authors
        has_authors = bool(metadata.get("authors"))
        
        # Check tools (alternative to authors)
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
        
        # 1. Supplier Name
        has_supplier = False
        if "supplier" in metadata and isinstance(metadata["supplier"], dict):
            has_supplier = bool(metadata["supplier"].get("name"))
        if not has_supplier and "component" in metadata:
            comp = metadata.get("component", {})
            has_supplier = bool(comp.get("supplier", {}).get("name"))
        element_status["supplier_name"] = has_supplier
        if has_supplier:
            elements_present += 1
        
        # 2. Component Name
        has_comp_name = any(c.get("name") for c in components if isinstance(c, dict))
        element_status["component_name"] = has_comp_name
        if has_comp_name:
            elements_present += 1
        
        # 3. Component Version
        has_comp_version = any(c.get("version") for c in components if isinstance(c, dict))
        element_status["component_version"] = has_comp_version
        if has_comp_version:
            elements_present += 1
        
        # 4. Unique Identifier (purl or bom-ref)
        has_identifier = any(
            c.get("purl") or c.get("bom-ref") 
            for c in components if isinstance(c, dict)
        )
        element_status["unique_identifier"] = has_identifier
        if has_identifier:
            elements_present += 1
        
        # 5. Dependency Relationship
        has_deps = len(dependencies) > 0
        element_status["dependency_rel"] = has_deps
        if has_deps:
            elements_present += 1
        
        # 6. Author
        has_author = bool(metadata.get("authors")) or bool(metadata.get("manufacturer"))
        element_status["author"] = has_author
        if has_author:
            elements_present += 1
        
        # 7. Timestamp
        has_timestamp = bool(metadata.get("timestamp"))
        element_status["timestamp"] = has_timestamp
        if has_timestamp:
            elements_present += 1
        
        total_elements = len(self.CISA_ELEMENTS)
        percentage = (elements_present / total_elements) * 100
        
        # Severity: 1.0 = 0% compliance, 0.0 = 100% compliance
        severity = 1.0 - (elements_present / total_elements)
        
        return {
            "severity": severity,
            "elements_present": elements_present,
            "total_elements": total_elements,
            "percentage": round(percentage, 1),
            "element_status": element_status
        }
