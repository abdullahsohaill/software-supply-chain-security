"""
TC2: Dependency Graph Depth Test
================================

Root Cause: Transitive dependencies are missed
Specification Section: 4.3.2(2)

Mitigation: Check if dependency graph has depth > 1 (transitive deps captured)
Problem: Measure divergence between component count and expected count
"""

from typing import Dict, Any, List
from . import BaseTestCase, build_dependency_graph, calculate_graph_depth


class TC2DependencyDepth(BaseTestCase):
    """Test case for transitive dependency coverage."""
    
    def __init__(self):
        super().__init__("TC2", "Dependency Graph Depth")
    
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check if SBOM has transitive dependencies (depth > 1)."""
        graph = build_dependency_graph(sbom)
        max_depth = calculate_graph_depth(graph)
        
        # Count total dependency relationships
        total_deps = sum(len(deps) for deps in graph.values())
        
        return {
            "present": max_depth > 1,
            "max_depth": max_depth,
            "has_graph": len(graph) > 0,
            "total_refs": len(graph),
            "total_relationships": total_deps
        }
    
    def measure_problem(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Measure the completeness of the dependency graph."""
        components = sbom.get("components", [])
        dependencies = sbom.get("dependencies", [])
        
        # Count components with bom-ref
        components_with_ref = [c for c in components if c.get("bom-ref")]
        
        # Count refs mentioned in dependencies
        refs_in_deps = set()
        for dep in dependencies:
            if isinstance(dep, dict):
                refs_in_deps.add(dep.get("ref", ""))
                refs_in_deps.update(dep.get("dependsOn", []))
        refs_in_deps.discard("")
        
        # Check for dangling refs (refs in deps not in components)
        component_refs = {c.get("bom-ref") for c in components_with_ref}
        # Add metadata.component ref if exists
        if "metadata" in sbom and "component" in sbom["metadata"]:
            component_refs.add(sbom["metadata"]["component"].get("bom-ref"))
        component_refs.discard(None)
        
        dangling_refs = refs_in_deps - component_refs
        
        # Calculate coverage
        if len(components_with_ref) > 0:
            coverage = len(refs_in_deps.intersection(component_refs)) / len(components_with_ref)
        else:
            coverage = 0.0
        
        # Severity based on coverage (lower coverage = higher severity)
        severity = 1.0 - coverage if components_with_ref else 0.5
        
        return {
            "severity": max(0.0, min(1.0, severity)),
            "component_count": len(components),
            "components_with_ref": len(components_with_ref),
            "refs_in_deps": len(refs_in_deps),
            "dangling_refs": len(dangling_refs),
            "coverage": round(coverage * 100, 1),
            "graph_present": len(dependencies) > 0
        }
