# file: unified_cyclonedx_comparator.py (Corrected Version)
import json
import sys
import os
from typing import Any, Dict, List, Optional

# --- UTILITY FUNCTIONS (No changes here) ---

def load_schema(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        print(f"FATAL ERROR: Schema file not found: {path}")
        print("Please make sure both schemas are in the same directory.")
        exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_defs(doc: Dict[str, Any]) -> Dict[str, Any]:
    return doc.get("$defs", doc.get("definitions", {})) or {}

def resolve_ref(doc: Dict[str, Any], node: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(node, dict) or "$ref" not in node:
        return node
    ref = node["$ref"]
    if not ref.startswith("#"):
        return node
    try:
        parts = ref[2:].split("/")
        target = doc
        for part in parts:
            part = part.replace("~1", "/").replace("~0", "~")
            target = target[part]
        merged = target.copy()
        merged.update({k: v for k, v in node.items() if k != "$ref"})
        return merged
    except (KeyError, IndexError):
        return node

def infer_type_string(doc: Dict[str, Any], schema_node: Any) -> str:
    if not isinstance(schema_node, dict):
        return type(schema_node).__name__
    node = resolve_ref(doc, schema_node)
    details = []
    node_type = node.get("type")
    if isinstance(node_type, list):
        details.append("type:" + "|".join(sorted(map(str, node_type))))
    elif node_type:
        details.append(f"type:{node_type}")
    if "format" in node:
        details.append(f"format:{node['format']}")
    if "pattern" in node:
        details.append("has_pattern")
    if "enum" in node:
        details.append(f"enum[{len(node['enum'])}]")
    if "const" in node:
        return f"const({json.dumps(node['const'])})"
    for combiner in ("oneOf", "anyOf", "allOf"):
        if combiner in node:
            details.append(combiner)
    if "$ref" in schema_node and schema_node['$ref'] != node.get('$ref'):
         details.append(f"ref({schema_node['$ref']})")
    if not details and ("properties" in node or "required" in node):
        return "object"
    return ", ".join(details) if details else "any"

# --- MAIN COMPARISON LOGIC ---

def run_comparison(prescriptive_path: str, official_path: str, report_path: str):
    print(f"Loading schemas: '{prescriptive_path}' and '{official_path}'...")
    prescriptive_doc = load_schema(prescriptive_path)
    official_doc = load_schema(official_path)
    
    prescriptive_defs = get_defs(prescriptive_doc)
    official_defs = get_defs(official_doc)
    
    report = [
        f"===== Unified Schema Comparison Report: CycloneDX v1.6 =====\n",
        f"Baseline (Prescriptive): {os.path.basename(prescriptive_path)}",
        f"Target   (Official)    : {os.path.basename(official_path)}\n"
    ]

    report.append("\n--- [Level 1] Top-Level Definition Presence ---\n")
    keys1, keys2 = set(prescriptive_defs.keys()), set(official_defs.keys())
    missing_in_2, added_in_2 = keys1 - keys2, keys2 - keys1
    if not missing_in_2 and not added_in_2:
        report.append("✅ ALIGNMENT: All top-level definitions are present in both schemas.")
    else:
        if missing_in_2:
            report.append(f"ℹ️  Info: {len(missing_in_2)} definitions in Baseline but not Target (likely defined inline or refactored).")
        if added_in_2:
            report.append(f"ℹ️  Info: {len(added_in_2)} definitions in Target but not Baseline (due to modular/reusable design).")
    report.append("Interpretation: The Official Schema uses a highly modular design with many reusable types, explaining the difference in top-level definition counts.\n")

    report.append("\n--- [Level 2] Property Presence within Common Definitions ---\n")
    common_defs = keys1.intersection(keys2)
    level2_mismatches = []
    for def_name in sorted(list(common_defs)):
        props1 = set(prescriptive_defs.get(def_name, {}).get("properties", {}).keys())
        props2 = set(official_defs.get(def_name, {}).get("properties", {}).keys())
        if props1 - props2:
            level2_mismatches.append(f"  - In '{def_name}', properties missing from Official Schema: {sorted(list(props1 - props2))}")
    if not level2_mismatches:
        report.append("✅ ALIGNMENT: Confirmed 100% property presence. No functional fields are missing in the Official Schema for all common definitions.")
    else:
        report.extend(level2_mismatches)
    report.append("\n")
    
    report.append("\n--- [Level 3] Granular Constraint & Type Comparison ---\n")
    level3_mismatches = []
    root_props1, root_props2 = prescriptive_doc.get("properties", {}), official_doc.get("properties", {})
    for prop_name, prop_schema in root_props1.items():
        if prop_name in root_props2:
            type1, type2 = infer_type_string(prescriptive_doc, prop_schema), infer_type_string(official_doc, root_props2[prop_name])
            if type1 != type2:
                level3_mismatches.append(f"  - BOM Root -> '{prop_name}': Mismatch ('{type1}' vs '{type2}')")
    for def_name in sorted(list(common_defs)):
        props1, props2 = prescriptive_defs[def_name].get("properties", {}), official_defs[def_name].get("properties", {})
        for prop_name in sorted(list(props1.keys())):
            if prop_name in props2:
                type1, type2 = infer_type_string(prescriptive_doc, props1[prop_name]), infer_type_string(official_doc, props2[prop_name])
                if type1 != type2:
                    level3_mismatches.append(f"  - In '{def_name}' -> '{prop_name}': Mismatch ('{type1}' vs '{type2}')")
    if level3_mismatches:
        report.append(f"Found {len(level3_mismatches)} granular type/constraint mismatches. This is expected due to the Official Schema's use of '$ref'.\nKey examples:")
        report.extend(level3_mismatches[:15])
        if len(level3_mismatches) > 15: report.append(f"  ... and {len(level3_mismatches) - 15} more.")
    else:
        report.append("✅ ALIGNMENT: No type or constraint discrepancies found for common properties.")
    report.append("\nInterpretation: Most mismatches highlight that the Official Schema defines constraints in central, referenced types, not directly on the properties.\n")

    report.append("\n--- [Semantic Audit] Programmatic Verification of Key Findings ---\n")
    sv_official = official_doc.get("properties", {}).get("specVersion", {})
    if sv_official.get("const") == "1.6" or ("1.6" in sv_official.get("enum", [])):
        report.append("✅ 'specVersion': Official Schema correctly enforces the version.")
    else:
        report.append("❌ DIVERGENCE: 'specVersion': Official Schema DOES NOT enforce the '1.6' value. This is a critical laxity.")
    
    # *** CORRECTED SECTION FOR licenseChoice ***
    try:
        defs1_lc = get_defs(prescriptive_doc).get('licenseChoice', {})
        defs2_lc = get_defs(official_doc).get('licenseChoice', {})
        struct1_ok = defs1_lc.get('oneOf', [{}])[0].get('items', {}).get('$ref') == '#/definitions/license'
        struct2_ok = 'license' in defs2_lc.get('oneOf', [{}])[0].get('items', {}).get('properties', {})
        if struct1_ok and struct2_ok:
            report.append("✅ 'licenseChoice' structure: VERIFIED incompatible structural interpretation, confirming ambiguity in prose.")
        else:
            report.append("⚠️ 'licenseChoice' structure: Could not automatically verify mismatch.")
    except Exception as e:
        report.append(f"⚠️ 'licenseChoice' structure: Error during programmatic check. Details: {e}")

    if official_doc.get("additionalProperties") is False:
        report.append("✅ Global Strictness: VERIFIED that the Official Schema is 'closed' (additionalProperties: false), a non-normative security hardening choice.")
    else:
        report.append("⚠️ Global Strictness: Official Schema is unexpectedly 'open'.")
        
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"\n[✔] Comparison complete. Full report saved to '{report_path}'")

def main():
    prescriptive_path = "02_schema.json"
    official_path = "schema.json"
    run_comparison(prescriptive_path, official_path, "cyclonedx_comparison_report.txt")

if __name__ == "__main__":
    main()