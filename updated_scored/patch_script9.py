import sys

with open("figures/gen_methodology.py", "r") as f:
    code = f.read()

# Increase width of Baseline and Conditional boxes
code = code.replace('_bw, _cw, _gap = 0.54, 0.60, 0.12', '_bw, _cw, _gap = 0.60, 0.75, 0.10')

with open("figures/gen_methodology.py", "w") as f:
    f.write(code)

