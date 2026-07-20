import sys

with open("figures/gen_methodology.py", "r") as f:
    code = f.read()

# 1. Widths:
code = code.replace("c3x, c3w = 5.38, 1.30", "c3x, c3w = 5.38, 1.70")
code = code.replace("rqX, rqW = 6.80, 5.38", "rqX, rqW = 7.20, 4.98")

# 2. Taxonomy (c3) font sizes & positions:
code = code.replace(
    't(c3x+c3w/2, BOT+0.58,\n  "3-Level Hierarchy\\n(Systematic Framework)",\n  fs=6.8, col=MED)',
    't(c3x+c3w/2, BOT+0.85,\n  "3-Level Hierarchy\\n(Systematic Framework)",\n  fs=7.5, col=MED)\n'
    '# taxonomy icon\n'
    'tx = c3x+c3w/2\n'
    'ty = BOT+0.45\n'
    'ax.plot([tx, tx], [ty+0.08, ty+0.02], color=MED, lw=1.5, zorder=4)\n'
    'ax.plot([tx-0.12, tx+0.12], [ty+0.02, ty+0.02], color=MED, lw=1.5, zorder=4)\n'
    'ax.plot([tx-0.12, tx-0.12], [ty+0.02, ty-0.03], color=MED, lw=1.5, zorder=4)\n'
    'ax.plot([tx+0.12, tx+0.12], [ty+0.02, ty-0.03], color=MED, lw=1.5, zorder=4)\n'
    'ax.add_patch(plt.Rectangle((tx-0.06, ty+0.08), 0.12, 0.08, fc=BOX, ec=MED, lw=1.2, zorder=5))\n'
    'ax.add_patch(plt.Rectangle((tx-0.18, ty-0.11), 0.12, 0.08, fc=BOX, ec=MED, lw=1.2, zorder=5))\n'
    'ax.add_patch(plt.Rectangle((tx+0.06, ty-0.11), 0.12, 0.08, fc=BOX, ec=MED, lw=1.2, zorder=5))\n'
)

# leaf node text size
code = code.replace(
    't(lx, ly-leaf_rad-0.11, lbl, fs=6.8, va="top")',
    't(lx, ly-leaf_rad-0.11, lbl, fs=7.8, va="top")'
)

# 3. Thematic Coding (c2) text spacing & icon:
code = code.replace(
    'for i, bl in enumerate(bullets):\n    t(c2x+0.05, bstart - i*0.94, bl, fs=9.2, ha="left", va="top", col=DARK)',
    'for i, bl in enumerate(bullets):\n    t(c2x+0.05, bstart - i*0.80, bl, fs=9.2, ha="left", va="top", col=DARK)\n'
    '# Search/Coding icon\n'
    'sx = c2x+c2w/2\n'
    'sy = BOT+0.55\n'
    'ax.add_patch(plt.Circle((sx-0.02, sy+0.05), 0.07, fc="none", ec=MED, lw=1.8, zorder=5))\n'
    'ax.plot([sx+0.03, sx+0.12], [sy, sy-0.09], color=MED, lw=2.2, zorder=5)\n'
)

with open("figures/gen_methodology.py", "w") as f:
    f.write(code)

