"""
CycloneDX Measurement Study - Test Case Framework
================================================

This module provides the base infrastructure for running test cases
against CycloneDX 1.6 SBOMs, mirroring the SPDX test case methodology.

Each test case measures:
1. Mitigation: Does the SBOM contain the specification's proposed solution?
2. Problem: How severe is the root cause in practice?
"""

import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import re
from collections import defaultdict
try:
    from packageurl import PackageURL
except ImportError:
    PackageURL = None  


@dataclass
class TestResult:
    """Result from a single test case execution."""
    test_id: str
    test_name: str
    mitigation_present: bool
    mitigation_details: Dict[str, Any] = field(default_factory=dict)
    problem_severity: float = 0.0  
    problem_details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_id": self.test_id,
            "test_name": self.test_name,
            "mitigation_present": self.mitigation_present,
            "mitigation_details": self.mitigation_details,
            "problem_severity": self.problem_severity,
            "problem_details": self.problem_details
        }


class BaseTestCase(ABC):
    """Abstract base class for all CycloneDX test cases."""
    
    def __init__(self, test_id: str, test_name: str):
        self.test_id = test_id
        self.test_name = test_name
    
    @abstractmethod
    def check_mitigation(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Check if the SBOM contains the specification's mitigation."""
        pass
    
    @abstractmethod
    def measure_problem(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Measure the severity of the root cause problem."""
        pass
    
    def run(self, sbom: Dict[str, Any]) -> TestResult:
        """Execute both mitigation check and problem measurement."""
        mitigation = self.check_mitigation(sbom)
        problem = self.measure_problem(sbom)
        
        return TestResult(
            test_id=self.test_id,
            test_name=self.test_name,
            mitigation_present=mitigation.get("present", False),
            mitigation_details=mitigation,
            problem_severity=problem.get("severity", 0.0),
            problem_details=problem
        )


def load_sbom(filepath: str) -> Dict[str, Any]:
    """Load a CycloneDX SBOM from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_all_components(sbom: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract all components including nested ones."""
    components = []
    
    def recurse(comp_list):
        for comp in comp_list:
            components.append(comp)
            if "components" in comp:
                recurse(comp["components"])
    
    if "components" in sbom:
        recurse(sbom["components"])
    
    
    if "metadata" in sbom and "component" in sbom["metadata"]:
        components.append(sbom["metadata"]["component"])
    
    return components


def extract_all_properties(sbom: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract all properties from all objects in the SBOM."""
    properties = []
    
    def recurse(obj):
        if isinstance(obj, dict):
            if "properties" in obj and isinstance(obj["properties"], list):
                properties.extend(obj["properties"])
            for value in obj.values():
                recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)
    
    recurse(sbom)
    return properties


def build_dependency_graph(sbom: Dict[str, Any]) -> Dict[str, List[str]]:
    """Build a dependency graph from the dependencies array."""
    dependencies = sbom.get("dependencies", [])
    graph = {}
    for dep in dependencies:
        if isinstance(dep, dict):
            ref = dep.get("ref", "")
            depends_on = dep.get("dependsOn", [])
            graph[ref] = depends_on if isinstance(depends_on, list) else []
    return graph


def calculate_graph_depth(graph: Dict[str, List[str]]) -> int:
    """Calculate the maximum depth of the dependency graph."""
    if not graph:
        return 0
    
    visited = set()
    max_depth = 0
    
    def dfs(node: str, depth: int):
        nonlocal max_depth
        if node in visited or node not in graph:
            max_depth = max(max_depth, depth)
            return
        visited.add(node)
        if not graph[node]:
            max_depth = max(max_depth, depth)
        else:
            for child in graph[node]:
                dfs(child, depth + 1)
        visited.discard(node)  
    
    
    all_children = set()
    for deps in graph.values():
        all_children.update(deps)
    roots = [node for node in graph.keys() if node not in all_children]
    
    if not roots:
        roots = list(graph.keys())[:1]  
    
    for root in roots:
        visited.clear()
        dfs(root, 1)
    
    return max_depth


def validate_purl(purl: str) -> bool:
    """Validate if a PURL follows the correct format."""
    if not purl:
        return False
    
    pattern = r'^pkg:[a-zA-Z][a-zA-Z0-9+.-]*/.+'
    return bool(re.match(pattern, purl))
