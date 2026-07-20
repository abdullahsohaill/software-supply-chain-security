import sys

with open("figures/gen_methodology.py", "r") as f:
    code = f.read()

old_thematic_icon = """# Tag icon (Multi-labeling/Coding)
sx = c2x+c2w/2
sy = BOT+0.42
# Back tag
bx, by = sx - 0.08, sy + 0.06
ax.add_patch(plt.Polygon([[bx, by], [bx+0.06, by+0.06], [bx+0.22, by+0.06], [bx+0.22, by-0.06], [bx+0.06, by-0.06]], fc="#dce0e8", ec=MED, lw=1.2, zorder=4))
ax.add_patch(plt.Circle((bx+0.04, by), 0.015, fc="white", ec=MED, lw=0.8, zorder=5))
# Front tag
fx, fy = sx - 0.12, sy
ax.add_patch(plt.Polygon([[fx, fy], [fx+0.06, fy+0.06], [fx+0.22, fy+0.06], [fx+0.22, fy-0.06], [fx+0.06, fy-0.06]], fc="#e4e7ed", ec=MED, lw=1.2, zorder=6))
ax.add_patch(plt.Circle((fx+0.04, fy), 0.015, fc="white", ec=MED, lw=0.8, zorder=7))
# Label lines on front tag
ax.plot([fx+0.1, fx+0.18], [fy+0.02, fy+0.02], color=MED, lw=0.8, zorder=7)
ax.plot([fx+0.1, fx+0.15], [fy-0.02, fy-0.02], color=MED, lw=0.8, zorder=7)"""

new_thematic_icon = """# Network Graph Icon (Thematic Coding / Grounded Theory)
sx = c2x+c2w/2
sy = BOT+0.42
cn = (sx, sy)
n1 = (sx - 0.15, sy + 0.08)
n2 = (sx + 0.12, sy + 0.10)
n3 = (sx - 0.08, sy - 0.12)
n4 = (sx + 0.15, sy - 0.08)

# Edges
ax.plot([cn[0], n1[0]], [cn[1], n1[1]], color=MED, lw=1.5, zorder=4)
ax.plot([cn[0], n2[0]], [cn[1], n2[1]], color=MED, lw=1.5, zorder=4)
ax.plot([cn[0], n3[0]], [cn[1], n3[1]], color=MED, lw=1.5, zorder=4)
ax.plot([cn[0], n4[0]], [cn[1], n4[1]], color=MED, lw=1.5, zorder=4)
ax.plot([n1[0], n3[0]], [n1[1], n3[1]], color=MED, lw=1.0, ls="--", zorder=4)
ax.plot([n2[0], n4[0]], [n2[1], n4[1]], color=MED, lw=1.0, ls="--", zorder=4)

# Draw document behind n1
ax.add_patch(plt.Rectangle((n1[0]-0.10, n1[1]-0.05), 0.08, 0.10, fc="white", ec=MED, lw=0.8, zorder=3))
ax.plot([n1[0]-0.08, n1[0]-0.04], [n1[1]+0.02, n1[1]+0.02], color=MED, lw=0.5, zorder=3)
ax.plot([n1[0]-0.08, n1[0]-0.04], [n1[1]-0.01, n1[1]-0.01], color=MED, lw=0.5, zorder=3)

# Nodes
ax.add_patch(plt.Circle(cn, 0.05, fc=HDR, ec=BORD, lw=1.2, zorder=5))
ax.add_patch(plt.Circle(cn, 0.02, fc="white", zorder=6))
ax.add_patch(plt.Circle(n1, 0.035, fc=BOX, ec=MED, lw=1, zorder=5))
ax.add_patch(plt.Circle(n2, 0.04, fc="#dce0e8", ec=MED, lw=1, zorder=5))
ax.add_patch(plt.Circle(n3, 0.035, fc=BOX, ec=MED, lw=1, zorder=5))
ax.add_patch(plt.Circle(n4, 0.03, fc="#dce0e8", ec=MED, lw=1, zorder=5))
"""
code = code.replace(old_thematic_icon, new_thematic_icon)

with open("figures/gen_methodology.py", "w") as f:
    f.write(code)

