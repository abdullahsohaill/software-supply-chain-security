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
        
        
        components_with_ref = [c for c in components if c.get("bom-ref")]
        
        
        refs_in_deps = set()
        refs_as_depender = set()
        refs_as_dependee = set()
        
        for dep in dependencies:
            if isinstance(dep, dict):
                ref = dep.get("ref", "")
                if ref:
                    refs_in_deps.add(ref)
                    refs_as_depender.add(ref)
                    
                for target in dep.get("dependsOn", []):
                    refs_in_deps.add(target)
                    refs_as_dependee.add(target)
        
        refs_in_deps.discard("")
        
        
        component_refs = {c.get("bom-ref") for c in components_with_ref}
        if "metadata" in sbom and "component" in sbom["metadata"]:
            root_ref = sbom["metadata"]["component"].get("bom-ref")
            if root_ref:
                component_refs.add(root_ref)
        component_refs.discard(None)
        
        
        dangling_refs = refs_in_deps - component_refs
        
        
        
        orphan_nodes = component_refs - refs_in_deps
        
        
        if len(components_with_ref) > 0:
            participating_components = component_refs.intersection(refs_in_deps)
            coverage = len(participating_components) / len(component_refs) if component_refs else 0.0
        else:
            coverage = 0.0
        
        
        
        severity = 1.0 - coverage
        
        return {
            "severity": max(0.0, min(1.0, severity)),
            "component_count": len(components),
            "components_with_ref": len(components_with_ref),
            "refs_in_deps": len(refs_in_deps),
            "dangling_refs": list(dangling_refs)[:10],
            "dangling_refs_count": len(dangling_refs),
            "orphan_nodes": list(orphan_nodes)[:10],
            "orphan_nodes_count": len(orphan_nodes),
            "coverage": round(coverage * 100, 1),
            "graph_present": len(dependencies) > 0
        }
