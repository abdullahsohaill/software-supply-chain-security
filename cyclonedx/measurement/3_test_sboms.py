#!/usr/bin/env python3
"""
CycloneDX Measurement Study - Main Test Runner
===============================================

This script runs all 8 test cases against CycloneDX 1.6 SBOMs and generates
a comprehensive measurement report matching the methodology in Section 3.4.

Usage:
    # Run on a single SBOM
    python 3_test_sboms.py --file path/to/sbom.json
    
    # Run on a directory of SBOMs
    python 3_test_sboms.py --dir wild_cyclonedx_1.6_sboms/
    
    # Run cross-tool comparison
    python 3_test_sboms.py --tool-compare tool_experiment/
    
    # Full measurement study
    python 3_test_sboms.py --dir wild_cyclonedx_1.6_sboms/ --output results.csv
"""

import argparse
import json
import os
import csv
import sys
from typing import Dict, Any, List
from datetime import datetime

# Import test cases
from test_cases import load_sbom, TestResult
from test_cases.tc1_cisa_compliance import TC1CISACompliance
from test_cases.tc2_dependency_depth import TC2DependencyDepth
from test_cases.tc3_tool_divergence import TC3ToolDivergence
from test_cases.tc4_property_taxonomy import TC4PropertyTaxonomy
from test_cases.tc5_interoperability import TC5Interoperability
from test_cases.tc5b_license_choice import TC5bLicenseChoice
from test_cases.tc6_reproducibility import TC6Reproducibility
from test_cases.tc7_composition import TC7Composition
from test_cases.tc8_purl_consistency import TC8PURLConsistency


class MeasurementStudy:
    """Orchestrates the full measurement study across all test cases."""
    
    def __init__(self):
        self.test_cases = [
            TC1CISACompliance(),
            TC2DependencyDepth(),
            TC3ToolDivergence(),
            TC4PropertyTaxonomy(),
            TC5Interoperability(),
            TC5bLicenseChoice(),
            TC6Reproducibility(),
            TC7Composition(),
            TC8PURLConsistency()
        ]
    
    def run_single(self, sbom_path: str) -> Dict[str, Any]:
        """Run all test cases on a single SBOM."""
        try:
            sbom = load_sbom(sbom_path)
        except Exception as e:
            return {"error": str(e), "file": os.path.basename(sbom_path)}
        
        results = {
            "file": os.path.basename(sbom_path),
            "timestamp": datetime.now().isoformat(),
            "spec_version": sbom.get("specVersion", "unknown"),
            "component_count": len(sbom.get("components", []))
        }
        
        for tc in self.test_cases:
            try:
                result = tc.run(sbom)
                results[f"{tc.test_id}_mitigation"] = "PASS" if result.mitigation_present else "FAIL"
                results[f"{tc.test_id}_severity"] = round(result.problem_severity, 3)
                results[f"{tc.test_id}_details"] = result.problem_details
            except Exception as e:
                results[f"{tc.test_id}_mitigation"] = "ERROR"
                results[f"{tc.test_id}_severity"] = 1.0
                results[f"{tc.test_id}_details"] = {"error": str(e)}
        
        return results
    
    def run_directory(self, dir_path: str, output_csv: str = None) -> List[Dict[str, Any]]:
        """Run all test cases on all SBOMs in a directory."""
        results = []
        json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]
        
        print(f"Found {len(json_files)} JSON files in {dir_path}")
        
        for i, filename in enumerate(json_files):
            filepath = os.path.join(dir_path, filename)
            print(f"[{i+1}/{len(json_files)}] Processing {filename}...")
            result = self.run_single(filepath)
            results.append(result)
        
        if output_csv:
            self._write_csv(results, output_csv)
            print(f"\nResults written to {output_csv}")
        
        return results
    
    def run_tool_comparison(self, dir_path: str) -> Dict[str, Any]:
        """Compare SBOMs from different tools in the tool_experiment directory."""
        sbom_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]
        sboms = {}
        
        for filename in sbom_files:
            filepath = os.path.join(dir_path, filename)
            try:
                sboms[filename] = load_sbom(filepath)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        
        if len(sboms) < 2:
            return {"error": "Need at least 2 SBOMs for comparison"}
        
        comparisons = []
        filenames = list(sboms.keys())
        
        for i in range(len(filenames)):
            for j in range(i + 1, len(filenames)):
                f1, f2 = filenames[i], filenames[j]
                
                # TC3 comparison
                tc3_comp = TC3ToolDivergence.compare_sboms(sboms[f1], sboms[f2])
                
                # TC8 comparison
                tc8_comp = TC8PURLConsistency.compare_purl_naming(sboms[f1], sboms[f2])
                
                comparisons.append({
                    "sbom1": f1,
                    "sbom2": f2,
                    "tc3_divergence": tc3_comp,
                    "tc8_purl_consistency": tc8_comp
                })
        
        return {"comparisons": comparisons}
    
    def _write_csv(self, results: List[Dict[str, Any]], output_path: str):
        """Write results to a CSV file."""
        if not results:
            return
        
        columns = [
            "file", "spec_version", "component_count",
            "TC1_mitigation", "TC1_severity",
            "TC2_mitigation", "TC2_severity",
            "TC3_mitigation", "TC3_severity",
            "TC4_mitigation", "TC4_severity",
            "TC5_mitigation", "TC5_severity",
            "TC5b_mitigation", "TC5b_severity",
            "TC6_mitigation", "TC6_severity",
            "TC7_mitigation", "TC7_severity",
            "TC8_mitigation", "TC8_severity"
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
            writer.writeheader()
            for result in results:
                row = {
                    "file": result.get("file", ""),
                    "spec_version": result.get("spec_version", ""),
                    "component_count": result.get("component_count", 0),
                }
                for tc_id in ["TC1", "TC2", "TC3", "TC4", "TC5", "TC5b", "TC6", "TC7", "TC8"]:
                    row[f"{tc_id}_mitigation"] = result.get(f"{tc_id}_mitigation", "N/A")
                    row[f"{tc_id}_severity"] = result.get(f"{tc_id}_severity", "N/A")
                writer.writerow(row)
    
    def print_summary(self, results: List[Dict[str, Any]]):
        """Print a summary of the measurement study."""
        if not results:
            print("No results to summarize")
            return
        
        total = len(results)
        print(f"\n{'='*60}")
        print(f"CYCLONEDX MEASUREMENT STUDY SUMMARY")
        print(f"{'='*60}")
        print(f"Total SBOMs analyzed: {total}")
        print(f"{'='*60}")
        
        for tc_id in ["TC1", "TC2", "TC3", "TC4", "TC5", "TC5b", "TC6", "TC7", "TC8"]:
            mitigation_key = f"{tc_id}_mitigation"
            severity_key = f"{tc_id}_severity"
            
            passes = sum(1 for r in results if r.get(mitigation_key) == "PASS")
            fails = sum(1 for r in results if r.get(mitigation_key) == "FAIL")
            errors = sum(1 for r in results if r.get(mitigation_key) == "ERROR")
            
            severities = [r.get(severity_key, 0) for r in results if isinstance(r.get(severity_key), (int, float))]
            avg_severity = sum(severities) / len(severities) if severities else 0
            
            tc_name = next((tc.test_name for tc in self.test_cases if tc.test_id == tc_id), tc_id)
            
            print(f"\n{tc_id}: {tc_name}")
            print(f"  Mitigation Present: {passes}/{total} ({passes/total*100:.1f}%)")
            print(f"  Average Severity: {avg_severity:.3f}")
            if errors > 0:
                print(f"  Errors: {errors}")


def main():
    parser = argparse.ArgumentParser(description="CycloneDX Measurement Study")
    parser.add_argument("--file", help="Path to a single SBOM file")
    parser.add_argument("--dir", help="Directory containing SBOM files")
    parser.add_argument("--tool-compare", help="Directory with tool-generated SBOMs to compare")
    parser.add_argument("--output", "-o", help="Output CSV file path")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    if not any([args.file, args.dir, args.tool_compare]):
        parser.print_help()
        sys.exit(1)
    
    study = MeasurementStudy()
    
    if args.file:
        result = study.run_single(args.file)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            for key, value in result.items():
                if not key.endswith("_details"):
                    print(f"{key}: {value}")
    
    elif args.dir:
        output_path = args.output or "cyclonedx_measurement_results.csv"
        results = study.run_directory(args.dir, output_path)
        if not args.json:
            study.print_summary(results)
        else:
            print(json.dumps(results, indent=2, default=str))
    
    elif args.tool_compare:
        result = study.run_tool_comparison(args.tool_compare)
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
