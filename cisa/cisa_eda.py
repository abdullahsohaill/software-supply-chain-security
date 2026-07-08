#!/usr/bin/env python3
"""
Comprehensive EDA for CISA Thematic Analysis
Produces counts, distributions, cross-tabulations, and figures.
"""

import csv
import os
from collections import Counter, defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "cisa_thematic.csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "eda_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalize whitespace
            cleaned = {k.strip(): v.strip() for k, v in row.items()}
            rows.append(cleaned)
    return rows

def normalize_keyword(kw):
    """Map all keyword variants to a canonical form."""
    kw = kw.upper().strip()
    mapping = {
        "MUST": "REQUIRED",
        "REQUIRED": "REQUIRED",
        "SHOULD": "RECOMMENDED",
        "RECOMMENDED": "RECOMMENDED",
        "MAY": "OPTIONAL",
        "OPTIONAL": "OPTIONAL",
        "MUST NOT": "REQUIRED",
    }
    return mapping.get(kw, kw)

def main():
    rows = load_data(CSV_PATH)
    total = len(rows)
    
    print(f"=" * 70)
    print(f"CISA THEMATIC ANALYSIS EDA")
    print(f"=" * 70)
    print(f"Total requirements extracted: {total}")
    print()

    # ─── 1. Theme Distribution ───────────────────────────────────────
    theme_counts = Counter(r["Theme"] for r in rows)
    print("1. THEME DISTRIBUTION")
    print("-" * 50)
    for theme, count in theme_counts.most_common():
        pct = count / total * 100
        print(f"  {theme:40s}  {count:3d}  ({pct:5.1f}%)")
    print()

    # ─── 2. Subtheme Distribution ────────────────────────────────────
    subtheme_counts = Counter(r["Subtheme"] for r in rows)
    print("2. SUBTHEME DISTRIBUTION")
    print("-" * 50)
    for sub, count in subtheme_counts.most_common():
        pct = count / total * 100
        print(f"  {sub:40s}  {count:3d}  ({pct:5.1f}%)")
    print()

    # ─── 3. Normative Keyword Distribution (raw) ─────────────────────
    keyword_counts = Counter(r["Normative Keyword"] for r in rows)
    print("3. NORMATIVE KEYWORD DISTRIBUTION (raw)")
    print("-" * 50)
    for kw, count in keyword_counts.most_common():
        pct = count / total * 100
        print(f"  {kw:20s}  {count:3d}  ({pct:5.1f}%)")
    print()

    # ─── 4. Normative Force (normalized to REQUIRED/RECOMMENDED/OPTIONAL)
    norm_counts = Counter(normalize_keyword(r["Normative Keyword"]) for r in rows)
    print("4. NORMATIVE FORCE (normalized)")
    print("-" * 50)
    for force, count in norm_counts.most_common():
        pct = count / total * 100
        print(f"  {force:20s}  {count:3d}  ({pct:5.1f}%)")
    print()

    # ─── 5. Cross-tab: Theme x Normative Force ──────────────────────
    print("5. CROSS-TABULATION: Theme x Normative Force")
    print("-" * 70)
    forces = ["REQUIRED", "RECOMMENDED", "OPTIONAL"]
    theme_force = defaultdict(lambda: Counter())
    for r in rows:
        nf = normalize_keyword(r["Normative Keyword"])
        theme_force[r["Theme"]][nf] += 1
    
    header = f"  {'Theme':40s}" + "".join(f"{f:>12s}" for f in forces) + f"{'Total':>8s}"
    print(header)
    for theme in sorted(theme_force.keys()):
        vals = theme_force[theme]
        t = sum(vals.values())
        line = f"  {theme:40s}" + "".join(f"{vals[f]:>12d}" for f in forces) + f"{t:>8d}"
        print(line)
    print()

    # ─── 6. Cross-tab: Subtheme x Normative Force ───────────────────
    print("6. CROSS-TABULATION: Subtheme x Normative Force")
    print("-" * 70)
    sub_force = defaultdict(lambda: Counter())
    for r in rows:
        nf = normalize_keyword(r["Normative Keyword"])
        sub_force[r["Subtheme"]][nf] += 1

    header = f"  {'Subtheme':40s}" + "".join(f"{f:>12s}" for f in forces) + f"{'Total':>8s}"
    print(header)
    for sub in sorted(sub_force.keys()):
        vals = sub_force[sub]
        t = sum(vals.values())
        line = f"  {sub:40s}" + "".join(f"{vals[f]:>12d}" for f in forces) + f"{t:>8d}"
        print(line)
    print()

    # ─── 7. Section Coverage ─────────────────────────────────────────
    section_counts = Counter()
    for r in rows:
        sec = r["Section ID & Heading"].split(" ")[0]  # Take section number
        section_counts[sec] += 1
    print("7. SECTION COVERAGE (top-level section => count)")
    print("-" * 50)
    top_sections = Counter()
    for sec, count in section_counts.items():
        # Extract top-level (e.g., "2.2.2.3" => "2")
        top = sec.split(".")[0]
        top_sections[top] += count
    for sec in sorted(top_sections.keys()):
        print(f"  Section {sec}: {top_sections[sec]} requirements")
    print()

    # ─── 8. CISA Minimum Elements Focus ──────────────────────────────
    print("8. CISA MINIMUM ELEMENTS FOCUS")
    print("-" * 50)
    min_element_sections = {
        "Author Name": "2.2.1.1",
        "Timestamp": "2.2.1.2",
        "Supplier Name": "2.2.2.3",
        "Component Name": "2.2.2.1",
        "Version": "2.2.2.2",
        "Unique Identifier": "2.2.2.4",
        "Relationship": "2.2.2.6",
        "Cryptographic Hash": "2.2.2.5",
    }
    for element, sec_prefix in min_element_sections.items():
        elem_rows = [r for r in rows if r["Section ID & Heading"].startswith(sec_prefix)]
        req_count = sum(1 for r in elem_rows if normalize_keyword(r["Normative Keyword"]) == "REQUIRED")
        rec_count = sum(1 for r in elem_rows if normalize_keyword(r["Normative Keyword"]) == "RECOMMENDED")
        opt_count = sum(1 for r in elem_rows if normalize_keyword(r["Normative Keyword"]) == "OPTIONAL")
        print(f"  {element:25s}  Total: {len(elem_rows):2d}  REQUIRED: {req_count}  RECOMMENDED: {rec_count}  OPTIONAL: {opt_count}")
    print()

    # ─── 9. Key Insight: Operations vs Data Quality ──────────────────
    print("9. KEY INSIGHT: Operations vs Data Quality normative force")
    print("-" * 50)
    ops_rows = [r for r in rows if r["Theme"] == "SBOM Operations & Lifecycle"]
    attr_rows = [r for r in rows if r["Theme"] == "Component & SBOM Attributes"]

    ops_force = Counter(normalize_keyword(r["Normative Keyword"]) for r in ops_rows)
    attr_force = Counter(normalize_keyword(r["Normative Keyword"]) for r in attr_rows)

    print(f"  SBOM Operations & Lifecycle ({len(ops_rows)} requirements):")
    for f in forces:
        pct = ops_force[f] / len(ops_rows) * 100 if ops_rows else 0
        print(f"    {f:20s}  {ops_force[f]:3d}  ({pct:5.1f}%)")

    print(f"  Component & SBOM Attributes ({len(attr_rows)} requirements):")
    for f in forces:
        pct = attr_force[f] / len(attr_rows) * 100 if attr_rows else 0
        print(f"    {f:20s}  {attr_force[f]:3d}  ({pct:5.1f}%)")
    print()

    # ─── 10. Dependency & Relationship requirements breakdown ────────
    print("10. DEPENDENCY & RELATIONSHIP MAPPING DETAIL")
    print("-" * 50)
    dep_rows = [r for r in rows if r["Subtheme"] == "Dependency & Relationship Mapping"]
    for dr in dep_rows:
        nf = normalize_keyword(dr["Normative Keyword"])
        print(f"  [{nf:12s}] {dr['Recommendation / Requirement'][:90]}")
    print(f"  Total: {len(dep_rows)} requirements")
    print()

    # ─── Write summary to file ───────────────────────────────────────
    summary_path = os.path.join(OUTPUT_DIR, "cisa_eda_summary.txt")
    # Redirect all output above is already printed, write key tables to file
    with open(summary_path, "w") as f:
        f.write("CISA THEMATIC ANALYSIS SUMMARY\n")
        f.write(f"Total requirements: {total}\n\n")
        
        f.write("Theme Distribution:\n")
        for theme, count in theme_counts.most_common():
            pct = count / total * 100
            f.write(f"  {theme}: {count} ({pct:.1f}%)\n")
        
        f.write("\nSubtheme Distribution:\n")
        for sub, count in subtheme_counts.most_common():
            pct = count / total * 100
            f.write(f"  {sub}: {count} ({pct:.1f}%)\n")
        
        f.write("\nNormative Force (normalized):\n")
        for force, count in norm_counts.most_common():
            pct = count / total * 100
            f.write(f"  {force}: {count} ({pct:.1f}%)\n")

    print(f"Summary written to: {summary_path}")

if __name__ == "__main__":
    main()
