"""
TC6: Reproducibility Test
=========================

Root Cause: Lack of reproducibility in builds on which SBOMs are created
Specification Section: 4.3.2(6)

Mitigation: Check for formulation with environment, workflow, tasks
Problem: Measure presence of reproducibility artifacts
"""

from typing import Dict, Any, List
from . import BaseTestCase


class TC6Reproducibility(BaseTestCase):
    """Test case for build reproducibility information."""
    
    def __init__(self):
        super().__init__("TC6", "Reproducibility")
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check if SBOM contains formulation for reproducibility."""
        formulation = sbom.get("formulation", [])
        
        if not formulation:
            return {
                "present": False,
                "has_formulation": False,
                "has_workflow": False,
                "has_environment": False,
                "has_tasks": False
            }
        
        # Check for specific formulation elements
        has_workflow = False
        has_environment = False
        has_tasks = False
        
        for form in formulation:
            if isinstance(form, dict):
                if "workflow" in form or "workflows" in form:
                    has_workflow = True
                if "environment" in form:
                    has_environment = True
                if "tasks" in form:
                    has_tasks = True
                # Check for components that describe the build
                if "components" in form:
                    has_environment = True
        
        return {
            "present": has_workflow or has_environment or has_tasks,
            "has_formulation": True,
            "has_workflow": has_workflow,
            "has_environment": has_environment,
            "has_tasks": has_tasks,
            "formulation_count": len(formulation)
        }
    
    def measure_problem(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Measure presence of reproducibility indicators."""
        # Count hashes (enable verification)
        components = sbom.get("components", [])
        comp_with_hashes = sum(1 for c in components if c.get("hashes"))
        
        # Check external references for build artifacts
        ext_refs = sbom.get("externalReferences", [])
        build_refs = []
        for ref in ext_refs:
            ref_type = ref.get("type", "")
            if ref_type in ["build-meta", "build-system", "vcs", "source-distribution"]:
                build_refs.append(ref_type)
        
        # Check for lockfile hashes in components
        lockfile_components = [
            c for c in components 
            if any(kw in c.get("name", "").lower() 
                   for kw in ["lock", "package-lock", "yarn.lock", "poetry.lock", "gemfile.lock"])
        ]
        
        # Check metadata for tools with version
        metadata = sbom.get("metadata", {})
        tools = metadata.get("tools", {})
        versioned_tools = 0
        if isinstance(tools, dict):
            # New format
            tool_components = tools.get("components", [])
            versioned_tools = sum(1 for t in tool_components if t.get("version"))
        elif isinstance(tools, list):
            # Legacy format
            versioned_tools = sum(1 for t in tools if t.get("version"))
        
        # Calculate reproducibility score
        total = len(components)
        if total > 0:
            hash_coverage = comp_with_hashes / total
        else:
            hash_coverage = 0.0
        
        build_ref_score = min(len(build_refs) / 4, 1.0)  # Max 4 types
        lockfile_score = 1.0 if lockfile_components else 0.0
        tool_score = 1.0 if versioned_tools > 0 else 0.0
        
        reproducibility_score = (hash_coverage + build_ref_score + lockfile_score + tool_score) / 4
        
        # Severity: lower score = worse
        severity = 1.0 - reproducibility_score
        
        return {
            "severity": severity,
            "total_components": total,
            "components_with_hashes": comp_with_hashes,
            "hash_coverage": round(hash_coverage * 100, 1),
            "build_ref_types": build_refs,
            "lockfile_components": len(lockfile_components),
            "versioned_tools": versioned_tools,
            "reproducibility_score": round(reproducibility_score * 100, 1)
        }
