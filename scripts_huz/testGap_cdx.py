#!/usr/bin/env python3
"""
testGap_cdx.py

Tests a CycloneDX SBOM (JSON) against a set of rules that are
often unenforced by the JSON schema but are MUST/SHOULD in the specification 
or CISA guidelines.

Usage:
    python3 testGap_cdx.py <path to sbom>
"""

import sys
import json
import re
from collections import namedtuple, defaultdict

PASS = "PASS"
FAIL = "FAIL"
INFO = "INFO"
NA = "N/A"

TestResult = namedtuple("TestResult", ["gap", "section", "title", "status", "details"])

def load_sbom(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# --------------------------------------------------------------------------
# Gap tests
# --------------------------------------------------------------------------

def test_empty_dependencies(data):
    gap, section, title = 1, "Dependencies", "Components with no dependencies MUST be empty graph entries"
    deps = data.get("dependencies", [])
    if not deps:
        return TestResult(gap, section, title, NA, "Dependency graph is not present.")
    dep_refs = {d.get("ref") for d in deps}
    comp_refs = []
    if "component" in data.get("metadata", {}):
        meta_ref = data["metadata"]["component"].get("bom-ref")
        if meta_ref:
            comp_refs.append(meta_ref)
    for comp in data.get("components", []):
        c_ref = comp.get("bom-ref")
        if c_ref:
            comp_refs.append(c_ref)
    if not comp_refs:
        return TestResult(gap, section, title, NA, "No components with bom-refs found.")
    missing = [ref for ref in comp_refs if ref not in dep_refs]
    if missing:
        return TestResult(gap, section, title, FAIL, f"{len(missing)} component(s) are missing from the dependency graph entirely.")
    return TestResult(gap, section, title, PASS, "All components are represented in the dependency graph.")

def test_purl_validity(data):
    gap, section, title = 2, "Identity", "PURLs MUST be structurally valid"
    components = data.get("components", [])
    if not components:
        return TestResult(gap, section, title, NA, "No components found.")
    purl_pattern = r"^pkg:[A-Za-z\.\-\+]+/[^@?#]+(@[^?#]+)?(\?[^#]+)?(#.+)?$"
    purls_found = 0
    invalid = []
    for comp in components:
        purl = comp.get("purl")
        if purl:
            purls_found += 1
            if not re.match(purl_pattern, purl) or " " in purl:
                invalid.append(purl)
    if purls_found == 0:
        return TestResult(gap, section, title, NA, "No PURLs found in components.")
    if invalid:
        return TestResult(gap, section, title, FAIL, f"{len(invalid)} PURL(s) are structurally invalid.")
    return TestResult(gap, section, title, PASS, f"All {purls_found} PURL(s) are structurally valid.")

def test_cisa_supplier(data):
    gap, section, title = 3, "Provenance", "Metadata supplier SHOULD be provided (CISA)"
    metadata = data.get("metadata", {})
    if not metadata or "supplier" not in metadata:
        return TestResult(gap, section, title, FAIL, "Supplier is missing from metadata.")
    return TestResult(gap, section, title, PASS, "Supplier is present in metadata.")

def test_cisa_timestamp(data):
    gap, section, title = 4, "Provenance", "Metadata timestamp SHOULD be provided (CISA)"
    metadata = data.get("metadata", {})
    if not metadata or "timestamp" not in metadata:
        return TestResult(gap, section, title, FAIL, "Timestamp is missing from metadata.")
    return TestResult(gap, section, title, PASS, "Timestamp is present in metadata.")

def test_cisa_tools(data):
    gap, section, title = 5, "Provenance", "Metadata tools SHOULD be provided (CISA)"
    metadata = data.get("metadata", {})
    if not metadata or "tools" not in metadata or not metadata["tools"]:
        return TestResult(gap, section, title, FAIL, "Tools are missing from metadata.")
    return TestResult(gap, section, title, PASS, "Tools are present in metadata.")

def test_component_names(data):
    gap, section, title = 6, "Inventory", "All components MUST have a name (CISA)"
    components = data.get("components", [])
    if not components:
        return TestResult(gap, section, title, NA, "No components found.")
    missing = [c for c in components if not c.get("name")]
    if missing:
        return TestResult(gap, section, title, FAIL, f"{len(missing)} component(s) are missing a name.")
    return TestResult(gap, section, title, PASS, "All components have a name.")

def test_component_versions(data):
    gap, section, title = 7, "Inventory", "All components SHOULD have a version (CISA)"
    components = data.get("components", [])
    if not components:
        return TestResult(gap, section, title, NA, "No components found.")
    missing = [c for c in components if not c.get("version")]
    if missing:
        return TestResult(gap, section, title, FAIL, f"{len(missing)} component(s) are missing a version.")
    return TestResult(gap, section, title, PASS, "All components have a version.")

def test_component_bomrefs(data):
    gap, section, title = 8, "Inventory", "All components SHOULD have a bom-ref"
    components = data.get("components", [])
    if not components:
        return TestResult(gap, section, title, NA, "No components found.")
    missing = [c for c in components if not c.get("bom-ref")]
    if missing:
        return TestResult(gap, section, title, FAIL, f"{len(missing)} component(s) are missing a bom-ref.")
    return TestResult(gap, section, title, PASS, "All components have a bom-ref.")

def test_vex_analysis(data):
    gap, section, title = 9, "Vulnerabilities", "Vulnerability analysis SHOULD be present if vulns exist"
    vulns = data.get("vulnerabilities", [])
    if not vulns:
        return TestResult(gap, section, title, NA, "No vulnerabilities listed.")
    missing_analysis = sum(1 for v in vulns if "analysis" not in v)
    if missing_analysis > 0:
        return TestResult(gap, section, title, FAIL, f"{missing_analysis}/{len(vulns)} vulnerabilities missing VEX analysis.")
    return TestResult(gap, section, title, PASS, "All vulnerabilities have associated analysis.")

def test_completeness_claims(data):
    gap, section, title = 10, "Completeness", "Compositions SHOULD be used to assert completeness"
    if "compositions" in data and data["compositions"]:
        return TestResult(gap, section, title, PASS, "Compositions block is present.")
    return TestResult(gap, section, title, FAIL, "Compositions block is missing.")

ALL_TESTS = [
    test_empty_dependencies,
    test_purl_validity,
    test_cisa_supplier,
    test_cisa_timestamp,
    test_cisa_tools,
    test_component_names,
    test_component_versions,
    test_component_bomrefs,
    test_vex_analysis,
    test_completeness_claims
]

def print_report(results, sbom_path):
    for r in results:
        status_label = f"\033[92mPASS\033[0m" if r.status == PASS else \
                       f"\033[91mFAIL\033[0m" if r.status == FAIL else \
                       f"\033[90mN/A \033[0m" if r.status == NA else \
                       f"\033[93mINFO\033[0m"
        print(f"Gap #{r.gap:<2} | {status_label:<13} | {r.section}: {r.title}")

    counts = defaultdict(int)
    for r in results: counts[r.status] += 1
    print(f"==> PASS: {counts[PASS]}, FAIL: {counts[FAIL]}, N/A: {counts[NA]}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 testGap_cdx.py <path to sbom>")
        sys.exit(1)
    sbom_path = sys.argv[1]
    data = load_sbom(sbom_path)
    results = [test_fn(data) for test_fn in ALL_TESTS]
    print(f"\n--- Results for {sbom_path} ---")
    print_report(results, sbom_path)

if __name__ == "__main__":
    main()
