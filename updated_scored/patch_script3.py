import sys

with open("figures/gen_methodology.py", "r") as f:
    code = f.read()

# 1. Req Extraction block header (Hybrid Human...):
code = code.replace(
    't(c1x+c1w/2, TOP-HDH-0.42, "Hybrid Human-NotebookLM\\nApproach",\n  fs=7.2, fw="bold")',
    't(c1x+c1w/2, TOP-HDH-0.42, "Hybrid Human-NotebookLM\\nApproach",\n  fs=8.2, fw="bold")'
)

# 1b. Req Extraction text (Pilot human...):
code = code.replace(
    't(c1x+c1w/2, TOP-HDH-0.85,\n  "Pilot human extraction →\\nscaled to NotebookLM.\\nReliability: Kappa-validated.",\n  fs=8, col=MED)',
    't(c1x+c1w/2, TOP-HDH-0.85,\n  "Pilot human extraction →\\nscaled to NotebookLM.\\nReliability: Kappa-validated.",\n  fs=9, col=MED)'
)

# 2. Third block (Thematic Coding & Analysis):
old_bullets = """bullets = [
    "• Code Refinement &\\n  Multi-labeling",
    "• Grounded theory\\n  framework\\n  (Roberts et al.)",
    "• Reliability: Miles &\\n  Huberman inter-coder\\n  check",
]
bstart = TOP-HDH-0.20
for i, bl in enumerate(bullets):
    t(c2x+0.05, bstart - i*0.90, bl, fs=8.2, ha="left", va="top", col=DARK)"""

new_bullets = """bullets = [
    "• Code Refinement &\\n  Multi-labeling",
    "• Grounded theory\\n  framework\\n  (Roberts et al.)",
    "• Reliability: Miles &\\n  Huberman inter-coder\\n  check",
]
bstart = TOP-HDH-0.20
for i, bl in enumerate(bullets):
    t(c2x+0.05, bstart - i*0.94, bl, fs=9.2, ha="left", va="top", col=DARK)"""
code = code.replace(old_bullets, new_bullets)

# 3. Last block (Root Cause Analysis & Synthesis):
code = code.replace(
    't(c5x+0.12, sy, s, fs=7.5, fw="bold" if bold else "normal",\n          ha="left", col=DARK)',
    't(c5x+0.12, sy, s, fs=8.5, fw="bold" if bold else "normal",\n          ha="left", col=DARK)'
)

with open("figures/gen_methodology.py", "w") as f:
    f.write(code)

