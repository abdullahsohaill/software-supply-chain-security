import sys

with open("figures/gen_methodology.py", "r") as f:
    code = f.read()

# 1. REQUIREMENT EXTRACTION:
code = code.replace(
    't(c1x+c1w/2, TOP-HDH-0.65,\n  "Pilot human extraction → scaled to\\nNotebookLM. Reliability: Kappa-validated.",\n  fs=7, col=MED)',
    't(c1x+c1w/2, TOP-HDH-0.65,\n  "Pilot human extraction → scaled to\\nNotebookLM. Reliability: Kappa-validated.",\n  fs=8, col=MED)'
)

# 2. THEMATIC CODING & ANALYSIS:
old_bullets = """bullets = [
    "• Code Refinement &\\n  Multi-labeling",
    "• Grounded theory framework\\n  (Roberts et al.)",
    "• Reliability: Miles &\\n  Huberman inter-coder check",
]
bstart = TOP-HDH-0.25
for i, bl in enumerate(bullets):
    t(c2x+0.12, bstart - i*0.82, bl, fs=7, ha="left", va="top", col=DARK)"""

new_bullets = """bullets = [
    "• Code Refinement &\\n  Multi-labeling",
    "• Grounded theory\\n  framework\\n  (Roberts et al.)",
    "• Reliability: Miles &\\n  Huberman inter-coder\\n  check",
]
bstart = TOP-HDH-0.20
for i, bl in enumerate(bullets):
    t(c2x+0.05, bstart - i*0.90, bl, fs=8.2, ha="left", va="top", col=DARK)"""
code = code.replace(old_bullets, new_bullets)

# 3. TAXONOMY:
# req -> requirements
code = code.replace(
    'r_rad = 0.10\nax.add_patch(plt.Circle((rx, ry), r_rad, fc=HDR, ec=BORD, lw=0.8, zorder=7))\nt(rx, ry, "Req.", fs=5.5, fw="bold", col="white")',
    'r_rad = 0.17\nax.add_patch(plt.Circle((rx, ry), r_rad, fc=HDR, ec=BORD, lw=0.8, zorder=7))\nt(rx, ry, "Requirements", fs=6.5, fw="bold", col="white")'
)
# initial codes, sub-themes
code = code.replace(
    't(lx, ly-leaf_rad-0.11, lbl, fs=5.2, va="top")',
    't(lx, ly-leaf_rad-0.11, lbl, fs=6.8, va="top")'
)
# Make leaves text slightly more compact vertically or shift them
code = code.replace(
    'leaves = [\n    (c3x+0.20, ry-0.88, "Initial\\nCodes"),\n    (c3x+c3w/2, ry-0.88, "Sub-\\nthemes"),\n    (c3x+c3w-0.20, ry-0.88, "High-level\\nThemes"),\n]',
    'leaves = [\n    (c3x+0.20, ry-0.88, "Initial\\nCodes"),\n    (c3x+c3w/2, ry-0.88, "Sub-\\nthemes"),\n    (c3x+c3w-0.20, ry-0.88, "High-level\\nThemes"),\n]'
)

# 4. RQ2/RQ3 Analysis:
code = code.replace(
    't(s1x+sub_w/2, rq2_y+rq2_h-HDH-0.44,\n  "Compare normative prose requirements\\nvs. annotator-derived JSON/XML schemas",\n  fs=6.8, col=MED)',
    't(s1x+sub_w/2, rq2_y+rq2_h-HDH-0.44,\n  "Compare normative prose requirements\\nvs. annotator-derived JSON/XML schemas",\n  fs=7.5, col=MED)'
)
code = code.replace(
    't(s2x+sub_w/2, rq2_y+rq2_h-HDH-0.44,\n  "Classify requirements as:\\nbaseline (always) vs.\\nconditional (context-dependent)",\n  fs=6.8, col=MED)',
    't(s2x+sub_w/2, rq2_y+rq2_h-HDH-0.44,\n  "Classify requirements as:\\nbaseline (always) vs.\\nconditional (context-dependent)",\n  fs=7.5, col=MED)'
)

old_rq3_content = """rq3_content = [
    (
        "Tool Selection",
        "Syft, Trivy, cdxgen,\\nMS-SBOM Tool,\\nSPDX-Tools\\n(6 tools total)",
    ),
    (
        "Static Inspection",
        "Source code analysis:\\nfield population logic,\\ndep. graph construction,\\nscope/filter behavior",
    ),
    (
        "Dynamic Analysis",
        "18 PyPI packages\\nas controlled test cases;\\nhold ecosystem constant,\\nisolate generator choices",
    ),
]

for ci, (sub_title, body) in enumerate(rq3_content):
    cx = rqX + 0.16 + ci*c3sw
    t(cx+c3sw/2, rq3_y+rq3_h-HDH-0.18, sub_title, fs=7, fw="bold")
    t(cx+c3sw/2, rq3_y+rq3_h-HDH-0.62, body, fs=6.5, col=MED)"""

new_rq3_content = """rq3_content = [
    (
        "Tool Selection",
        "Syft, Trivy, cdxgen,\\nMS-SBOM Tool,\\nspdx-sbom-gen\\n(5 tools total)",
    ),
    (
        "Static Inspection",
        "Source code analysis:\\nfield population logic,\\ndep. graph construction,\\nscope/filter behavior",
    ),
    (
        "Dynamic Analysis",
        "18 PyPI packages\\nas controlled test cases;\\nhold ecosystem constant,\\nisolate generator choices",
    ),
]

for ci, (sub_title, body) in enumerate(rq3_content):
    cx = rqX + 0.16 + ci*c3sw
    t(cx+c3sw/2, rq3_y+rq3_h-HDH-0.18, sub_title, fs=7.5, fw="bold")
    t(cx+c3sw/2, rq3_y+rq3_h-HDH-0.66, body, fs=7.5, col=MED)"""
code = code.replace(old_rq3_content, new_rq3_content)

# 5. ROOT CAUSE ANALYSIS & SYNTHESIS:
code = code.replace(
    't(c5x+0.12, sy, s, fs=7, fw="bold" if bold else "normal",\n          ha="left", col=DARK)',
    't(c5x+0.12, sy, s, fs=7.5, fw="bold" if bold else "normal",\n          ha="left", col=DARK)'
)


with open("figures/gen_methodology.py", "w") as f:
    f.write(code)

