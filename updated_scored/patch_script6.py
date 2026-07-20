import sys

with open("figures/gen_methodology.py", "r") as f:
    code = f.read()

# 1. Replace the Taxonomy hierarchy icon with a 3-Level Pyramid
old_tax_icon = """# taxonomy icon
tx = c3x+c3w/2
ty = BOT+0.45
ax.plot([tx, tx], [ty+0.08, ty+0.02], color=MED, lw=1.5, zorder=4)
ax.plot([tx-0.12, tx+0.12], [ty+0.02, ty+0.02], color=MED, lw=1.5, zorder=4)
ax.plot([tx-0.12, tx-0.12], [ty+0.02, ty-0.03], color=MED, lw=1.5, zorder=4)
ax.plot([tx+0.12, tx+0.12], [ty+0.02, ty-0.03], color=MED, lw=1.5, zorder=4)
ax.add_patch(plt.Rectangle((tx-0.06, ty+0.08), 0.12, 0.08, fc=BOX, ec=MED, lw=1.2, zorder=5))
ax.add_patch(plt.Rectangle((tx-0.18, ty-0.11), 0.12, 0.08, fc=BOX, ec=MED, lw=1.2, zorder=5))
ax.add_patch(plt.Rectangle((tx+0.06, ty-0.11), 0.12, 0.08, fc=BOX, ec=MED, lw=1.2, zorder=5))"""

new_tax_icon = """# taxonomy icon (3-Level Pyramid)
tx = c3x+c3w/2
ty = BOT+0.35
pw, ph = 0.35, 0.28
# Base
ax.add_patch(plt.Polygon([[tx-pw/2, ty], [tx+pw/2, ty], [tx+pw/2*0.66, ty+ph*0.33], [tx-pw/2*0.66, ty+ph*0.33]], fc="#e4e7ed", ec=MED, lw=1.2, zorder=5))
# Middle
ax.add_patch(plt.Polygon([[tx-pw/2*0.66, ty+ph*0.33], [tx+pw/2*0.66, ty+ph*0.33], [tx+pw/2*0.33, ty+ph*0.66], [tx-pw/2*0.33, ty+ph*0.66]], fc="#dce0e8", ec=MED, lw=1.2, zorder=5))
# Top
ax.add_patch(plt.Polygon([[tx-pw/2*0.33, ty+ph*0.66], [tx+pw/2*0.33, ty+ph*0.66], [tx, ty+ph]], fc=BOX, ec=MED, lw=1.2, zorder=5))
"""
code = code.replace(old_tax_icon, new_tax_icon)


# 2. Replace the Thematic Coding loop (spacing fix) and the icon (Tags instead of search)
old_thematic = """for i, bl in enumerate(bullets):
    t(c2x+0.05, bstart - i*0.80, bl, fs=9.2, ha="left", va="top", col=DARK)
# Search/Coding icon
sx = c2x+c2w/2
sy = BOT+0.55
ax.add_patch(plt.Circle((sx-0.02, sy+0.05), 0.07, fc="none", ec=MED, lw=1.8, zorder=5))
ax.plot([sx+0.03, sx+0.12], [sy, sy-0.09], color=MED, lw=2.2, zorder=5)"""

new_thematic = """y_coords = [bstart, bstart - 0.70, bstart - 1.50]
for i, bl in enumerate(bullets):
    t(c2x+0.05, y_coords[i], bl, fs=9.2, ha="left", va="top", col=DARK)
# Tag icon (Multi-labeling/Coding)
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
code = code.replace(old_thematic, new_thematic)

with open("figures/gen_methodology.py", "w") as f:
    f.write(code)

