import sys

with open("figures/gen_methodology.py", "r") as f:
    code = f.read()

# 1. Move the Hybrid Human... header down
code = code.replace(
    't(c1x+c1w/2, TOP-HDH-0.42, "Hybrid Human-NotebookLM\\nApproach",\n  fs=8.2, fw="bold")',
    't(c1x+c1w/2, TOP-HDH-0.52, "Hybrid Human-NotebookLM\\nApproach",\n  fs=8.2, fw="bold")'
)

# Move Pilot human text down
code = code.replace(
    't(c1x+c1w/2, TOP-HDH-0.85,\n  "Pilot human extraction →\\nscaled to NotebookLM.\\nReliability: Kappa-validated.",\n  fs=9, col=MED)',
    't(c1x+c1w/2, TOP-HDH-0.95,\n  "Pilot human extraction →\\nscaled to NotebookLM.\\nReliability: Kappa-validated.",\n  fs=9, col=MED)'
)

# 2. Move Total Requirements block up
code = code.replace(
    'corpus_y = BOT + 0.35',
    'corpus_y = BOT + 0.45'
)

with open("figures/gen_methodology.py", "w") as f:
    f.write(code)

