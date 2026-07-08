#!/usr/bin/env python3
"""
Comprehensive EDA for CycloneDX Thematic Analysis
Produces counts, distributions, cross-tabulations, and key insights.
"""

import csv
import os
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "cyclonedx_thematic.csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "eda_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {k.strip(): v.strip() for k, v in row.items()}
            rows.append(cleaned)
    return rows

def normalize_keyword(kw):
    kw = kw.upper().strip()
    mapping = {
        "MUST": "REQUIRED",
        "MUST NOT": "REQUIRED",
        "REQUIRED": "REQUIRED",
        "SHOULD": "RECOMMENDED",
        "SHOULD NOT": "RECOMMENDED",
        "RECOMMENDED": "RECOMMENDED",
        "MAY": "OPTIONAL",
        "OPTIONAL": "OPTIONAL",
    }
    return mapping.get(kw, kw)

def main():
    rows = load_data(CSV_PATH)
    total = len(rows)
    
    print(f"=" * 70)
    print(f"CYCLONEDX 1.6 THEMATIC ANALYSIS EDA")
    print(f"=" * 70)
    print(f"Total requirements extracted: {total}")
    print()

    # ─── 1. Subtheme Distribution (these are the primary tags) ───────
    subtheme_counts = Counter(r["Subtheme"] for r in rows)
    print("1. SUBTHEME DISTRIBUTION (top 25)")
    print("-" * 60)
    for sub, count in subtheme_counts.most_common(25):
        pct = count / total * 100
        print(f"  {sub:50s}  {count:4d}  ({pct:5.1f}%)")
    print(f"  ... total unique subthemes: {len(subtheme_counts)}")
    print()

    # ─── 2. Group subthemes into higher-level themes ─────────────────
    # We can derive themes by grouping related subthemes
    theme_mapping = {
        # Foundational BOM Structure
        "BOM Format and Versioning": "Foundational BOM Structure",
        "BOM Identification": "Foundational BOM Structure",
        "Root Object Model": "Foundational BOM Structure",
        "Internal Referencing (bom-ref)": "Foundational BOM Structure",
        "Specification Conformance": "Foundational BOM Structure",
        # Core Inventory & Attributes
        "Component and Service Typing": "Core Inventory & Attributes",
        "Component and Service Identification": "Core Inventory & Attributes",
        "Component Scope": "Core Inventory & Attributes",
        "Descriptive Metadata": "Core Inventory & Attributes",
        "Component Assemblies (Nesting)": "Core Inventory & Attributes",
        # Metadata & Provenance
        "BOM Metadata": "Metadata & Provenance",
        "Organizational Entity Definition": "Metadata & Provenance",
        "Contact Information": "Metadata & Provenance",
        "Component Pedigree and Provenance": "Metadata & Provenance",
        "Timestamping": "Metadata & Provenance",
        "Lifecycle Information": "Metadata & Provenance",
        "Tooling Information": "Metadata & Provenance",
        "Evidence and Substantiation": "Metadata & Provenance",
        # Trust, Integrity, and Security
        "Cryptographic Hashes": "Trust, Integrity & Security",
        "Standardized External Identifiers": "Trust, Integrity & Security",
        "Licensing and Copyright": "Trust, Integrity & Security",
        "Vulnerability Information": "Trust, Integrity & Security",
        "Signature and Trust": "Trust, Integrity & Security",
        # Relationships & Composition
        "Dependency Graph Representation": "Relationships & Composition",
        "External References": "Relationships & Composition",
        "Composition and Completeness": "Relationships & Composition",
        # Extensibility
        "Extensibility via Properties": "Extensibility & Customization",
        "Property Taxonomies": "Extensibility & Customization",
        # Advanced & Specialized
        "Cryptographic Asset Mgmt (CBOM)": "Advanced & Specialized Data Models",
        "Formulation and Reproducibility": "Advanced & Specialized Data Models",
        "ML Model Card": "Advanced & Specialized Data Models",
        "Data Governance": "Advanced & Specialized Data Models",
        "Service Definition": "Advanced & Specialized Data Models",
        "Annotation": "Advanced & Specialized Data Models",
        "Declaration and Attestation": "Advanced & Specialized Data Models",
    }

    # Auto-assign remaining subthemes
    derived_theme = {}
    for r in rows:
        sub = r["Subtheme"]
        if sub in theme_mapping:
            derived_theme[sub] = theme_mapping[sub]
        else:
            derived_theme[sub] = "Other / Unclassified"

    theme_counts = Counter(derived_theme.get(r["Subtheme"], "Other / Unclassified") for r in rows)
    print("2. DERIVED THEME DISTRIBUTION")
    print("-" * 60)
    for theme, count in theme_counts.most_common():
        pct = count / total * 100
        print(f"  {theme:50s}  {count:4d}  ({pct:5.1f}%)")
    print()

    # ─── 3. Normative Keyword Distribution (raw) ─────────────────────
    keyword_counts = Counter(r["Normative Keyword"] for r in rows)
    print("3. NORMATIVE KEYWORD DISTRIBUTION (raw)")
    print("-" * 50)
    for kw, count in keyword_counts.most_common():
        pct = count / total * 100
        print(f"  {kw:20s}  {count:4d}  ({pct:5.1f}%)")
    print()

    # ─── 4. Normative Force (normalized) ─────────────────────────────
    norm_counts = Counter(normalize_keyword(r["Normative Keyword"]) for r in rows)
    print("4. NORMATIVE FORCE (normalized)")
    print("-" * 50)
    for force, count in norm_counts.most_common():
        pct = count / total * 100
        print(f"  {force:20s}  {count:4d}  ({pct:5.1f}%)")
    print()

    # ─── 5. Cross-tab: Derived Theme x Normative Force ───────────────
    forces = ["REQUIRED", "RECOMMENDED", "OPTIONAL"]
    print("5. CROSS-TABULATION: Derived Theme x Normative Force")
    print("-" * 80)
    theme_force = defaultdict(lambda: Counter())
    for r in rows:
        nf = normalize_keyword(r["Normative Keyword"])
        th = derived_theme.get(r["Subtheme"], "Other")
        theme_force[th][nf] += 1

    header = f"  {'Theme':50s}" + "".join(f"{f:>12s}" for f in forces) + f"{'Total':>8s}"
    print(header)
    for theme in sorted(theme_force.keys()):
        vals = theme_force[theme]
        t = sum(vals.values())
        line = f"  {theme:50s}" + "".join(f"{vals[f]:>12d}" for f in forces) + f"{t:>8d}"
        print(line)
    print()

    # ─── 6. CISA Minimum Elements in CycloneDX ──────────────────────
    print("6. CISA MINIMUM ELEMENTS: CycloneDX Coverage")
    print("-" * 70)
    # Map CISA minimum elements to CycloneDX subthemes/fields
    cisa_fields = {
        "Supplier Name": ["metadata.supplier", "component supplier"],
        "Author Name": ["metadata.authors", "component authors"],
        "Timestamp": ["timestamp"],
        "Component Name": ["name property is Required"],
        "Version": ["version property"],
        "Unique Identifier": ["purl", "cpe", "swhid", "omniborId", "swid"],
        "Relationship": ["dependencies", "dependsOn", "dependency"],
        "Cryptographic Hash": ["hash", "hashes"],
    }
    
    for element, keywords in cisa_fields.items():
        matching = [r for r in rows if any(kw.lower() in r["Recommendation / Requirement"].lower() for kw in keywords)]
        req_count = sum(1 for r in matching if normalize_keyword(r["Normative Keyword"]) == "REQUIRED")
        rec_count = sum(1 for r in matching if normalize_keyword(r["Normative Keyword"]) == "RECOMMENDED")
        opt_count = sum(1 for r in matching if normalize_keyword(r["Normative Keyword"]) == "OPTIONAL")
        print(f"  {element:25s}  Total: {len(matching):3d}  REQUIRED: {req_count:3d}  RECOMMENDED: {rec_count:3d}  OPTIONAL: {opt_count:3d}")
    print()

    # ─── 7. Security-relevant requirements analysis ──────────────────
    print("7. SECURITY-RELEVANT SUBTHEMES")
    print("-" * 60)
    security_subthemes = [
        "Vulnerability Information",
        "Cryptographic Hashes",
        "Cryptographic Asset Mgmt (CBOM)",
        "Dependency Graph Representation",
        "Composition and Completeness",
        "Component Pedigree and Provenance",
        "Evidence and Substantiation",
        "Formulation and Reproducibility",
    ]
    for sub in security_subthemes:
        sub_rows = [r for r in rows if r["Subtheme"] == sub]
        if sub_rows:
            req = sum(1 for r in sub_rows if normalize_keyword(r["Normative Keyword"]) == "REQUIRED")
            rec = sum(1 for r in sub_rows if normalize_keyword(r["Normative Keyword"]) == "RECOMMENDED")
            opt = sum(1 for r in sub_rows if normalize_keyword(r["Normative Keyword"]) == "OPTIONAL")
            print(f"  {sub:50s}  Total: {len(sub_rows):3d}  REQ: {req:3d}  REC: {rec:3d}  OPT: {opt:3d}")
    print()

    # ─── 8. Top Sections by requirement count ────────────────────────
    section_counts = Counter(r["Section ID & Heading"].split(" ")[0] for r in rows)
    print("8. TOP 15 SECTIONS BY REQUIREMENT COUNT")
    print("-" * 50)
    for sec, count in section_counts.most_common(15):
        print(f"  Section {sec:15s}  {count:4d} requirements")
    print()

    # ─── 9. Optional vs Required ratio per subtheme ──────────────────
    print("9. OPTIONAL-TO-REQUIRED RATIO PER SUBTHEME (top 15 by total)")
    print("-" * 70)
    for sub, count in subtheme_counts.most_common(15):
        sub_rows = [r for r in rows if r["Subtheme"] == sub]
        req = sum(1 for r in sub_rows if normalize_keyword(r["Normative Keyword"]) == "REQUIRED")
        opt = sum(1 for r in sub_rows if normalize_keyword(r["Normative Keyword"]) == "OPTIONAL")
        ratio = f"{opt}/{req}" if req > 0 else f"{opt}/0"
        print(f"  {sub:50s}  OPT: {opt:3d}  REQ: {req:3d}  Ratio: {ratio}")
    print()

    # ─── 10. Dependency-specific requirements ────────────────────────
    print("10. DEPENDENCY GRAPH REPRESENTATION REQUIREMENTS")
    print("-" * 70)
    dep_rows = [r for r in rows if r["Subtheme"] == "Dependency Graph Representation"]
    for dr in dep_rows:
        nf = normalize_keyword(dr["Normative Keyword"])
        print(f"  [{nf:12s}] {dr['Recommendation / Requirement'][:100]}")
    print(f"  Total: {len(dep_rows)} requirements")
    print()

    # ─── Write summary ───────────────────────────────────────────────
    summary_path = os.path.join(OUTPUT_DIR, "cyclonedx_eda_summary.txt")
    with open(summary_path, "w") as f:
        f.write("CYCLONEDX 1.6 THEMATIC ANALYSIS SUMMARY\n")
        f.write(f"Total requirements: {total}\n\n")
        
        f.write("Subtheme Distribution:\n")
        for sub, count in subtheme_counts.most_common():
            pct = count / total * 100
            f.write(f"  {sub}: {count} ({pct:.1f}%)\n")
        
        f.write("\nDerived Theme Distribution:\n")
        for theme, count in theme_counts.most_common():
            pct = count / total * 100
            f.write(f"  {theme}: {count} ({pct:.1f}%)\n")
        
        f.write("\nNormative Force (normalized):\n")
        for force, count in norm_counts.most_common():
            pct = count / total * 100
            f.write(f"  {force}: {count} ({pct:.1f}%)\n")

    print(f"Summary written to: {summary_path}")

if __name__ == "__main__":
    main()
