import sys

with open("figures/gen_methodology.py", "r") as f:
    code = f.read()

old_tax_icon = """# taxonomy icon (3-Level Pyramid)
tx = c3x+c3w/2
ty = BOT+0.35
pw, ph = 0.35, 0.28
# Base
ax.add_patch(plt.Polygon([[tx-pw/2, ty], [tx+pw/2, ty], [tx+pw/2*0.66, ty+ph*0.33], [tx-pw/2*0.66, ty+ph*0.33]], fc="#e4e7ed", ec=MED, lw=1.2, zorder=5))
# Middle
ax.add_patch(plt.Polygon([[tx-pw/2*0.66, ty+ph*0.33], [tx+pw/2*0.66, ty+ph*0.33], [tx+pw/2*0.33, ty+ph*0.66], [tx-pw/2*0.33, ty+ph*0.66]], fc="#dce0e8", ec=MED, lw=1.2, zorder=5))
# Top
ax.add_patch(plt.Polygon([[tx-pw/2*0.33, ty+ph*0.66], [tx+pw/2*0.33, ty+ph*0.66], [tx, ty+ph]], fc=BOX, ec=MED, lw=1.2, zorder=5))"""

new_tax_icon = """# taxonomy icon (Inverted 3-Level Pyramid/Funnel)
tx = c3x+c3w/2
ty = BOT+0.35
pw, ph = 0.35, 0.28
# Top (Widest)
ax.add_patch(plt.Polygon([[tx-pw/2, ty+ph], [tx+pw/2, ty+ph], [tx+pw/2*0.66, ty+ph*0.66], [tx-pw/2*0.66, ty+ph*0.66]], fc="#e4e7ed", ec=MED, lw=1.2, zorder=5))
# Middle
ax.add_patch(plt.Polygon([[tx-pw/2*0.66, ty+ph*0.66], [tx+pw/2*0.66, ty+ph*0.66], [tx+pw/2*0.33, ty+ph*0.33], [tx-pw/2*0.33, ty+ph*0.33]], fc="#dce0e8", ec=MED, lw=1.2, zorder=5))
# Bottom (Pointy tip)
ax.add_patch(plt.Polygon([[tx-pw/2*0.33, ty+ph*0.33], [tx+pw/2*0.33, ty+ph*0.33], [tx, ty]], fc=BOX, ec=MED, lw=1.2, zorder=5))"""

code = code.replace(old_tax_icon, new_tax_icon)

with open("figures/gen_methodology.py", "w") as f:
    f.write(code)

