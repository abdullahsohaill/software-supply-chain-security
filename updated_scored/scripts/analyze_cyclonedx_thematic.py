#!/usr/bin/env python3
"""Recompute CycloneDX thematic-analysis artifacts for the ICSE paper.

The input is the extracted CycloneDX requirements CSV in the SSC root. The
script performs a deterministic second-pass recoding from the earlier
single-subtheme labels into a generator/consumer-oriented codebook, then emits
CSV summaries and small TikZ figures used by the paper.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "icse_paper"
INPUT = ROOT / "cyclonedx_extractions.csv"
DATA = PAPER / "data"
FIGURES = PAPER / "figures"


SUBTHEME_MAP = {
    "AI/ML Model Cards (ML-BOM)": (
        "ml_model_card_modeling",
        "Specialized BOM extensions",
        "Specialized security data models",
        "generator-population",
        "inventory/provenance",
    ),
    "Annotations": (
        "annotation_population",
        "Extension and annotation mechanisms",
        "Structural conformance and validation",
        "shared-validation",
        "inventory/provenance",
    ),
    "Attestations and Declarations": (
        "attestation_declaration_modeling",
        "Specialized BOM extensions",
        "Specialized security data models",
        "generator-population",
        "inventory/provenance",
    ),
    "BOM Format and Versioning": (
        "bom_format_versioning",
        "Document structure and conformance",
        "Structural conformance and validation",
        "shared-validation",
        "inventory/provenance",
    ),
    "BOM Identification": (
        "bom_document_identity",
        "BOM identity and references",
        "Provenance, identity, and trust",
        "generator-obligation",
        "inventory/provenance",
    ),
    "BOM Metadata": (
        "document_metadata_population",
        "Producer and document metadata",
        "Provenance, identity, and trust",
        "generator-population",
        "provenance",
    ),
    "Component Assemblies (Nesting)": (
        "component_nesting",
        "Dependency and assembly semantics",
        "Dependency and downstream-use semantics",
        "generator-population",
        "inventory/provenance",
    ),
    "Component Pedigree and Provenance": (
        "pedigree_population",
        "Build provenance and evidence",
        "Completeness and evidence",
        "generator-obligation; generator-population",
        "completeness/evidence",
    ),
    "Component Scope": (
        "scope_runtime_semantics",
        "Dependency and assembly semantics",
        "Dependency and downstream-use semantics",
        "downstream-use",
        "dependencies",
    ),
    "Component and Service Definition": (
        "component_service_population",
        "Component identity and metadata",
        "Component inventory and identity",
        "generator-population",
        "inventory/provenance",
    ),
    "Component and Service Identification": (
        "component_service_identity",
        "Component identity and metadata",
        "Component inventory and identity",
        "generator-population",
        "inventory/provenance",
    ),
    "Component and Service Typing": (
        "component_service_typing",
        "Component identity and metadata",
        "Component inventory and identity",
        "generator-population",
        "inventory/provenance",
    ),
    "Composition and Completeness": (
        "completeness_assertion",
        "Completeness and evidence claims",
        "Completeness and evidence",
        "downstream-use",
        "dependencies; completeness/evidence",
    ),
    "Contact Information": (
        "contact_provenance_population",
        "Producer and document metadata",
        "Provenance, identity, and trust",
        "generator-population",
        "inventory/provenance",
    ),
    "Cryptographic Asset Management (CBOM)": (
        "cryptographic_asset_modeling",
        "Specialized BOM extensions",
        "Specialized security data models",
        "generator-population",
        "inventory/provenance",
    ),
    "Cryptographic Hashes": (
        "hash_integrity_population",
        "Integrity metadata",
        "Provenance, identity, and trust",
        "generator-population",
        "inventory/provenance",
    ),
    "Data Components and Governance": (
        "data_governance_modeling",
        "Specialized BOM extensions",
        "Specialized security data models",
        "generator-population",
        "inventory/provenance",
    ),
    "Dependency Graph Representation": (
        "dependency_graph_population",
        "Dependency and assembly semantics",
        "Dependency and downstream-use semantics",
        "downstream-use",
        "dependencies",
    ),
    "Descriptive Metadata": (
        "component_descriptive_metadata",
        "Component identity and metadata",
        "Component inventory and identity",
        "generator-population",
        "inventory/provenance",
    ),
    "Digital Signatures": (
        "signature_integrity_population",
        "Integrity metadata",
        "Provenance, identity, and trust",
        "generator-population",
        "inventory/provenance",
    ),
    "Evidence and Substantiation": (
        "evidence_population",
        "Build provenance and evidence",
        "Completeness and evidence",
        "generator-population",
        "completeness/evidence",
    ),
    "Extensibility via Properties": (
        "extension_property_population",
        "Extension and annotation mechanisms",
        "Structural conformance and validation",
        "shared-validation",
        "inventory/provenance",
    ),
    "External References": (
        "external_reference_population",
        "External identifiers and references",
        "Component inventory and identity",
        "generator-population",
        "inventory/provenance",
    ),
    "Formulation and Reproducible Builds": (
        "formulation_build_evidence",
        "Build provenance and evidence",
        "Completeness and evidence",
        "generator-population",
        "completeness/evidence",
    ),
    "Internal Referencing (bom-ref)": (
        "bom_ref_identity_links",
        "BOM identity and references",
        "Provenance, identity, and trust",
        "generator-population",
        "provenance",
    ),
    "Licensing and Copyright": (
        "license_copyright_population",
        "Legal and licensing metadata",
        "Component inventory and identity",
        "generator-population",
        "inventory/provenance",
    ),
    "Lifecycle Information": (
        "field_level_constraint",
        "Document structure and conformance",
        "Structural conformance and validation",
        "generator-population",
        "inventory/provenance",
    ),
    "Organizational Entity Definition": (
        "entity_provenance_population",
        "Producer and document metadata",
        "Provenance, identity, and trust",
        "generator-population",
        "provenance",
    ),
    "Property Taxonomies": (
        "property_taxonomy_normalization",
        "Extension and annotation mechanisms",
        "Structural conformance and validation",
        "shared-validation",
        "inventory/provenance",
    ),
    "Root Object Model": (
        "root_object_population",
        "Document structure and conformance",
        "Structural conformance and validation",
        "shared-validation",
        "provenance",
    ),
    "Specification Conformance": (
        "implementation_conformance",
        "Document structure and conformance",
        "Structural conformance and validation",
        "consumer-interpretation; shared-validation",
        "downstream-use",
    ),
    "Standardized External Identifiers": (
        "identifier_normalization",
        "External identifiers and references",
        "Component inventory and identity",
        "generator-population",
        "inventory/provenance",
    ),
    "Timestamping": (
        "timestamp_population",
        "Producer and document metadata",
        "Provenance, identity, and trust",
        "generator-population",
        "provenance",
    ),
    "Tooling Information": (
        "tool_metadata_population",
        "Producer and document metadata",
        "Provenance, identity, and trust",
        "generator-population",
        "provenance",
    ),
    "Vulnerability Impact Analysis (VEX)": (
        "vex_analysis_semantics",
        "Vulnerability and VEX records",
        "Vulnerability and VEX semantics",
        "downstream-use",
        "vulnerabilities",
    ),
    "Vulnerability Information (Vulnerability Object)": (
        "vulnerability_record_population",
        "Vulnerability and VEX records",
        "Vulnerability and VEX semantics",
        "generator-population",
        "vulnerabilities",
    ),
}


def read_rows() -> list[dict[str, str]]:
    with INPUT.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def pct(count: int, total: int) -> str:
    return f"{(count / total * 100):.1f}"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def latex_escape(text: str) -> str:
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def write_count_table(path: Path, rows: list[dict[str, object]], label_col: str, caption: str, label: str) -> None:
    lines = [
        r"\begin{table}[t]",
        rf"\caption{{{latex_escape(caption)}}}",
        rf"\label{{{label}}}",
        r"\centering",
        r"\small",
        r"\begin{tabularx}{\columnwidth}{@{}Xrr@{}}",
        r"\toprule",
        rf"\textbf{{{latex_escape(label_col)}}} & \textbf{{Count}} & \textbf{{\%}} \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            f"{latex_escape(str(row[label_col]))} & {row['count']} & {row['percent']} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabularx}", r"\end{table}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_bar_figure(path: Path, rows: list[dict[str, object]], label_col: str, caption: str, label: str) -> None:
    max_count = max(int(row["count"]) for row in rows)
    y_step = 0.55
    lines = [
        r"\begin{figure}[t]",
        r"\centering",
        r"\begin{tikzpicture}[x=1cm,y=1cm]",
        r"\scriptsize",
    ]
    for idx, row in enumerate(rows):
        y = -idx * y_step
        width = int(row["count"]) / max_count * 4.2
        row_label = latex_escape(str(row[label_col]))
        lines.append(rf"\node[anchor=east] at (0,{y:.2f}) {{{row_label}}};")
        lines.append(rf"\fill[blue!35] (0.10,{y - 0.13:.2f}) rectangle ({0.10 + width:.2f},{y + 0.13:.2f});")
        lines.append(rf"\node[anchor=west] at ({0.20 + width:.2f},{y:.2f}) {{{row['count']} ({row['percent']}\%)}};")
    lines.extend(
        [
            r"\end{tikzpicture}",
            rf"\caption{{{latex_escape(caption)}}}",
            rf"\label{{{label}}}",
            r"\end{figure}",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def distribution(rows: list[dict[str, str]], field: str, total: int, top: int | None = None) -> list[dict[str, object]]:
    counts = Counter(row[field] for row in rows)
    items = counts.most_common(top)
    return [
        {field: key, "count": count, "percent": pct(count, total)}
        for key, count in items
    ]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    raw_rows = read_rows()
    coded_rows: list[dict[str, str]] = []
    missing = sorted({r["Subtheme"] for r in raw_rows if r["Subtheme"] not in SUBTHEME_MAP})
    if missing:
        raise SystemExit(f"Unmapped CycloneDX subthemes: {missing}")

    for idx, row in enumerate(raw_rows, start=1):
        initial_code, subtheme, theme, axis, focus = SUBTHEME_MAP[row["Subtheme"]]
        coded_rows.append(
            {
                "id": f"CDX-{idx:04d}",
                "section": row["Section ID & Heading"],
                "requirement": row["Recommendation / Requirement"],
                "normative_force": row["Normative Keyword"],
                "initial_code": initial_code,
                "subtheme": subtheme,
                "theme": theme,
                "generator_consumer_axis": axis,
                "issue_focus": focus,
                "previous_single_subtheme": row["Subtheme"],
            }
        )

    total = len(coded_rows)
    write_csv(
        DATA / "cyclonedx_generator_consumer_coding.csv",
        [
            "id",
            "section",
            "requirement",
            "normative_force",
            "initial_code",
            "subtheme",
            "theme",
            "generator_consumer_axis",
            "issue_focus",
            "previous_single_subtheme",
        ],
        coded_rows,
    )

    grouped: dict[tuple[str, str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in coded_rows:
        grouped[
            (
                row["theme"],
                row["subtheme"],
                row["initial_code"],
                row["generator_consumer_axis"],
                row["issue_focus"],
            )
        ].append(row)

    codebook_rows = []
    for (theme, subtheme, initial_code, axis, focus), members in grouped.items():
        codebook_rows.append(
            {
                "theme": theme,
                "subtheme": subtheme,
                "initial_code": initial_code,
                "generator_consumer_axis": axis,
                "issue_focus": focus,
                "count": len(members),
                "percent": pct(len(members), total),
                "example_requirement": members[0]["requirement"],
            }
        )
    codebook_rows.sort(key=lambda r: (-int(r["count"]), r["theme"], r["subtheme"]))
    write_csv(
        DATA / "cyclonedx_generator_consumer_codebook.csv",
        [
            "theme",
            "subtheme",
            "initial_code",
            "generator_consumer_axis",
            "issue_focus",
            "count",
            "percent",
            "example_requirement",
        ],
        codebook_rows,
    )

    outputs = [
        ("theme", "cyclonedx_theme_distribution.csv", None),
        ("subtheme", "cyclonedx_subtheme_distribution.csv", None),
        ("initial_code", "cyclonedx_code_distribution.csv", None),
        ("generator_consumer_axis", "cyclonedx_axis_distribution.csv", None),
        ("issue_focus", "cyclonedx_issue_focus_distribution.csv", None),
        ("normative_force", "cyclonedx_normative_force_distribution.csv", None),
    ]
    for field, filename, top in outputs:
        rows = distribution(coded_rows, field, total, top)
        write_csv(DATA / filename, [field, "count", "percent"], rows)

    theme_rows = distribution(coded_rows, "theme", total)
    subtheme_rows = distribution(coded_rows, "subtheme", total, top=12)
    code_rows = distribution(coded_rows, "initial_code", total, top=12)
    axis_rows = distribution(coded_rows, "generator_consumer_axis", total)
    focus_rows = distribution(coded_rows, "issue_focus", total)
    force_rows = distribution(coded_rows, "normative_force", total)

    write_count_table(DATA / "cyclonedx_theme_distribution_table.tex", theme_rows, "theme", "CycloneDX thematic distribution.", "tab:cdx-theme-distribution")
    write_count_table(DATA / "cyclonedx_top_subthemes_table.tex", subtheme_rows, "subtheme", "Top CycloneDX subthemes after recoding.", "tab:cdx-top-subthemes")
    write_count_table(DATA / "cyclonedx_top_codes_table.tex", code_rows, "initial_code", "Top CycloneDX initial codes after recoding.", "tab:cdx-top-codes")
    write_count_table(DATA / "cyclonedx_axis_distribution_table.tex", axis_rows, "generator_consumer_axis", "Secondary interface-role distribution for CycloneDX requirements.", "tab:cdx-axis-distribution")
    write_count_table(DATA / "cyclonedx_issue_focus_table.tex", focus_rows, "issue_focus", "Secondary analysis-focus distribution for CycloneDX requirements.", "tab:cdx-issue-focus")
    write_count_table(DATA / "cyclonedx_normative_force_table.tex", force_rows, "normative_force", "CycloneDX normative-force distribution.", "tab:cdx-normative-force")

    write_bar_figure(FIGURES / "cyclonedx_theme_distribution_tikz.tex", theme_rows, "theme", "CycloneDX theme distribution recomputed from 1,724 extracted requirements.", "fig:cdx-theme-distribution")
    write_bar_figure(FIGURES / "cyclonedx_axis_distribution_tikz.tex", axis_rows, "generator_consumer_axis", "Secondary interface-role distribution for CycloneDX requirements.", "fig:cdx-axis-distribution")
    write_bar_figure(FIGURES / "cyclonedx_issue_focus_tikz.tex", focus_rows, "issue_focus", "Secondary analysis-focus distribution for CycloneDX requirements.", "fig:cdx-issue-focus")

    print(f"Recomputed {total} CycloneDX requirements.")
    print("Top themes:")
    for row in theme_rows:
        print(f"  {row['theme']}: {row['count']} ({row['percent']}%)")


if __name__ == "__main__":
    main()
