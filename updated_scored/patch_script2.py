import sys

with open("figures/gen_methodology.py", "r") as f:
    code = f.read()

# 1. Req Extraction block header:
code = code.replace(
    't(c1x+c1w/2, TOP-HDH-0.22, "Hybrid Human-NotebookLM\\nApproach",\n  fs=7.2, fw="bold")',
    't(c1x+c1w/2, TOP-HDH-0.42, "Hybrid Human-NotebookLM\\nApproach",\n  fs=7.2, fw="bold")'
)

# 2. Req Extraction text:
code = code.replace(
    't(c1x+c1w/2, TOP-HDH-0.65,\n  "Pilot human extraction → scaled to\\nNotebookLM. Reliability: Kappa-validated.",\n  fs=8, col=MED)',
    't(c1x+c1w/2, TOP-HDH-0.85,\n  "Pilot human extraction →\\nscaled to NotebookLM.\\nReliability: Kappa-validated.",\n  fs=8, col=MED)'
)

# 3. Total Corpus box:
old_corpus = """corpus_y = BOT + 0.08
box(c1x+0.10, corpus_y, c1w-0.20, 0.74, fc=BOX, ec=BORD, lw=1.0, r=0.04, z=5)
t(c1x+c1w/2, corpus_y+0.62, "Total Corpus: 2,286 requirements",
  fs=7, fw="bold")
t(c1x+c1w/2, corpus_y+0.46, "CycloneDX  —  1,724", fs=6.8, col=MED)
t(c1x+c1w/2, corpus_y+0.30, "SPDX  —  429", fs=6.8, col=MED)
t(c1x+c1w/2, corpus_y+0.14, "CISA  —  133", fs=6.8, col=MED)"""

new_corpus = """corpus_y = BOT + 0.35
box(c1x+0.10, corpus_y, c1w-0.20, 0.85, fc=BOX, ec=BORD, lw=1.0, r=0.04, z=5)
t(c1x+c1w/2, corpus_y+0.71, "Total Corpus: 2,286 requirements",
  fs=7, fw="bold")
t(c1x+c1w/2, corpus_y+0.52, "CycloneDX  —  1,724", fs=8, col=MED)
t(c1x+c1w/2, corpus_y+0.33, "SPDX  —  429", fs=8, col=MED)
t(c1x+c1w/2, corpus_y+0.14, "CISA  —  133", fs=8, col=MED)"""
code = code.replace(old_corpus, new_corpus)

# 4. Taxonomy Requirements oval:
old_oval = """r_rad = 0.17
ax.add_patch(plt.Circle((rx, ry), r_rad, fc=HDR, ec=BORD, lw=0.8, zorder=7))
t(rx, ry, "Requirements", fs=6.5, fw="bold", col="white")"""

new_oval = """oval_w, oval_h = 1.0, 0.30
box(rx - oval_w/2, ry - oval_h/2, oval_w, oval_h, fc=HDR, ec=BORD, lw=0.8, r=0.15, z=7)
r_rad = oval_h/2
t(rx, ry, "Requirements", fs=6.5, fw="bold", col="white")"""
code = code.replace(old_oval, new_oval)

# 5. Taxonomy High-level Themes leaf:
old_leaves = """leaves = [
    (c3x+0.20, ry-0.88, "Initial\\nCodes"),
    (c3x+c3w/2, ry-0.88, "Sub-\\nthemes"),
    (c3x+c3w-0.20, ry-0.88, "High-level\\nThemes"),
]"""

new_leaves = """leaves = [
    (c3x+0.20, ry-0.88, "Initial\\nCodes"),
    (c3x+c3w/2, ry-0.88, "Sub-\\nthemes"),
    (c3x+c3w-0.20, ry-0.88, "High-\\nlevel\\nThemes"),
]"""
code = code.replace(old_leaves, new_leaves)

with open("figures/gen_methodology.py", "w") as f:
    f.write(code)

