import sys

with open("figures/gen_methodology.py", "r") as f:
    code = f.read()

# Adjust the x-coordinate of the "High-level Themes" leaf node
code = code.replace(
    '(c3x+c3w-0.20, ry-0.88, "High-\\nlevel\\nThemes")',
    '(c3x+c3w-0.30, ry-0.88, "High-\\nlevel\\nThemes")'
)

with open("figures/gen_methodology.py", "w") as f:
    f.write(code)

