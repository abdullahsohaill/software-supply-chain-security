import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

fig_w, fig_h = 15.0, 3.78
fig, ax = plt.subplots(figsize=(fig_w, fig_h))
ax.set_xlim(0, fig_w)
ax.set_ylim(0, fig_h)
ax.axis("off")
fig.patch.set_facecolor("#f4f5f7")
ax.set_facecolor("#f4f5f7")

# grid
for gx in [i*0.35 for i in range(int(fig_w/0.35)+2)]:
    ax.plot([gx, gx], [0, fig_h], color="#dce0e8", lw=0.25, alpha=0.7, zorder=0)
for gy in [i*0.35 for i in range(int(fig_h/0.35)+2)]:
    ax.plot([0, fig_w], [gy, gy], color="#dce0e8", lw=0.25, alpha=0.7, zorder=0)

BG   = "#ffffff"
DARK = "#1a1a2e"
MED  = "#52526a"
LITE = "#9999aa"
BORD = "#2a2a2a"
BOX  = "#e4e7ed"
HDR  = "#2d2d3a"

def box(x, y, w, h, fc=BG, ec=BORD, lw=1.2, ls="-", r=0.0, z=2):
    if r:
        p = FancyBboxPatch((x,y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                           fc=fc, ec=ec, lw=lw, ls=ls, zorder=z)
    else:
        p = Rectangle((x,y), w, h, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z)
    ax.add_patch(p)

def t(x, y, s, fs=7.5, fw="normal", ha="center", va="center", col=DARK):
    ax.text(x, y, s, fontsize=fs, fontweight=fw, ha=ha, va=va,
            color=col, fontfamily="DejaVu Sans", zorder=7, clip_on=False)

def arr(x0, y0, x1, y1, lw=1.3):
    ax.annotate("", xy=(x1,y1), xytext=(x0,y0),
                arrowprops=dict(
                    arrowstyle="-|>, head_width=0.16, head_length=0.12",
                    color=DARK, lw=lw), zorder=5)

def hdr(x, y, w, h, s, fs=7.5):
    box(x, y, w, h, fc=HDR, ec=BORD, lw=1.3, z=4)
    t(x+w/2, y+h/2, s, fs=fs, fw="bold", col="white")

# ── layout ────────────────────────────────────────────────────────────────
L   = 0.18
BOT = 0.10
TOP = 3.57
CH  = TOP - BOT       # 3.47
HDH = 0.30

# column x + width — carefully chosen so total ≤ fig_w
c0x, c0w = L,    1.15   # input sources (small)
c1x, c1w = 1.44, 2.00   # step 1 — wider to fit content
c2x, c2w = 3.56, 1.70   # step 2
c3x, c3w = 5.38, 1.70   # taxonomy — slightly wider
rqX, rqW = 7.20, 4.98   # RQ2+RQ3
c5x, c5w = 12.30, 2.56  # synthesis

# outer frame
box(L-0.08, BOT-0.08, fig_w-2*(L-0.08), CH+0.24,
    fc="#f4f5f7", ec=BORD, lw=1.8, r=0.10, z=1)



# ══════════════════════════════════════════════════════════════════════════
# COL 0 — INPUT SOURCES  (tight, no wasted space)
# ══════════════════════════════════════════════════════════════════════════
hdr(c0x, TOP-HDH, c0w, HDH, "INPUT\nSOURCES", fs=7.5)
box(c0x, BOT, c0w, CH-HDH)

# 3 tight source boxes – packed near centre
src_h = 0.31
src_gap = 0.10
src_items = ["CISA Minimum\nElements", "CycloneDX 1.6", "SPDX 3.0.1"]
n = len(src_items)
blk_h = n*src_h + (n-1)*src_gap
start_y = BOT + (CH-HDH-blk_h)/2
for i, lbl in enumerate(src_items):
    by = start_y + i*(src_h+src_gap)
    box(c0x+0.08, by, c0w-0.16, src_h, fc=BOX, ec=BORD, lw=0.9, r=0.04, z=5)
    t(c0x+c0w/2, by+src_h/2, lbl, fs=7.2, fw="bold")

# ══════════════════════════════════════════════════════════════════════════
# COL 1 — STEP 1: REQUIREMENT EXTRACTION
# ══════════════════════════════════════════════════════════════════════════
# RQ1 badge — small box at top-right corner of Step1 header
hdr(c1x, TOP-HDH, c1w, HDH, "REQUIREMENT\nEXTRACTION", fs=7.5)
box(c1x, BOT, c1w, CH-HDH, ls=(0,(5,3)))

# Title (replaces person icon)
t(c1x+c1w/2, TOP-HDH-0.52, "Hybrid Human-NotebookLM\nApproach",
  fs=8.2, fw="bold")

# Body text — moved up, no gap waste
t(c1x+c1w/2, TOP-HDH-1.00,
  "Human pilot (20%)\nNotebookLM scaling\nPilot agreement:\nCohen's kappa",
  fs=8.0, col=MED)

# Corpus box — tight, near bottom
corpus_y = BOT + 0.45
box(c1x+0.10, corpus_y, c1w-0.20, 0.85, fc=BOX, ec=BORD, lw=1.0, r=0.04, z=5)
t(c1x+c1w/2, corpus_y+0.71, "Realized rows: 2,286",
  fs=7.8, fw="bold")
t(c1x+c1w/2, corpus_y+0.52, "CycloneDX  —  1,724", fs=8, col=MED)
t(c1x+c1w/2, corpus_y+0.33, "SPDX  —  429", fs=8, col=MED)
t(c1x+c1w/2, corpus_y+0.14, "CISA  —  133", fs=8, col=MED)

# ══════════════════════════════════════════════════════════════════════════
# COL 2 — STEP 2: THEMATIC CODING & ANALYSIS
# ══════════════════════════════════════════════════════════════════════════
hdr(c2x, TOP-HDH, c2w, HDH, "THEMATIC CODING\n& ANALYSIS", fs=7.5)
box(c2x, BOT, c2w, CH-HDH, ls=(0,(5,3)))

# 3 bullet points, tightly packed near top of column
bullets = [
    "• Codebook\n  development\n  & reconciliation",
    "• Grounded-theory\n  framework\n  (Roberts et al.)",
    "• Subtheme coding\n  & agreement",
]
bstart = TOP-HDH-0.20
y_coords = [bstart, bstart - 0.70, bstart - 1.50]
for i, bl in enumerate(bullets):
    t(c2x+0.05, y_coords[i], bl, fs=9.2, ha="left", va="top", col=DARK)
# Network Graph Icon (Thematic Coding / Grounded Theory)
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



# ══════════════════════════════════════════════════════════════════════════
# COL 3 — RESULTING TAXONOMY  (cleaner, smaller)
# ══════════════════════════════════════════════════════════════════════════
hdr(c3x, TOP-HDH, c3w, HDH, "TAXONOMY  [RQ1]", fs=7.5)
box(c3x, BOT, c3w, CH-HDH)

# Small tree diagram
rx, ry = c3x+c3w/2, TOP-HDH-0.38   # root node
oval_w, oval_h = 1.1, 0.35
box(rx - oval_w/2, ry - oval_h/2, oval_w, oval_h, fc=HDR, ec=BORD, lw=0.8, r=0.17, z=7)
r_rad = oval_h/2
t(rx, ry, "Requirements", fs=7.5, fw="bold", col="white")

# 3 leaf nodes
leaves = [
    (c3x+0.20, ry-0.88, "Initial\nCodes"),
    (c3x+c3w/2, ry-0.88, "Sub-\nthemes"),
    (c3x+c3w-0.30, ry-0.88, "High-\nlevel\nThemes"),
]
leaf_rad = 0.08
for lx, ly, lbl in leaves:
    ax.plot([rx, lx], [ry-r_rad, ly+leaf_rad], color=BORD, lw=0.9, zorder=5)
    ax.add_patch(plt.Circle((lx, ly), leaf_rad, fc=BOX, ec=BORD, lw=0.8, zorder=7))
    t(lx, ly-leaf_rad-0.11, lbl, fs=7.8, va="top")

# label below
t(c3x+c3w/2, BOT+0.85,
  "3-Level Hierarchy\n(Systematic Framework)",
  fs=7.5, col=MED)
# taxonomy icon (Inverted 3-Level Pyramid/Funnel)
tx = c3x+c3w/2
ty = BOT+0.35
pw, ph = 0.35, 0.28
# Top (Widest)
ax.add_patch(plt.Polygon([[tx-pw/2, ty+ph], [tx+pw/2, ty+ph], [tx+pw/2*0.66, ty+ph*0.66], [tx-pw/2*0.66, ty+ph*0.66]], fc="#e4e7ed", ec=MED, lw=1.2, zorder=5))
# Middle
ax.add_patch(plt.Polygon([[tx-pw/2*0.66, ty+ph*0.66], [tx+pw/2*0.66, ty+ph*0.66], [tx+pw/2*0.33, ty+ph*0.33], [tx-pw/2*0.33, ty+ph*0.33]], fc="#dce0e8", ec=MED, lw=1.2, zorder=5))
# Bottom (Pointy tip)
ax.add_patch(plt.Polygon([[tx-pw/2*0.33, ty+ph*0.33], [tx+pw/2*0.33, ty+ph*0.33], [tx, ty]], fc=BOX, ec=MED, lw=1.2, zorder=5))



# ══════════════════════════════════════════════════════════════════════════
# RQ2 / RQ3 DASHED REGION
# ══════════════════════════════════════════════════════════════════════════
box(rqX, BOT-0.04, rqW, CH+0.12,
    fc="#eff1f4", ec=BORD, lw=1.8, ls=(0,(5,3)), r=0.07, z=1)

# Label INSIDE the region at very top
hdr(rqX+0.12, TOP-HDH, rqW-0.24, HDH, "RQ2 / RQ3  Analysis", fs=8)

# sub-regions geometry
rq2_h = (CH - HDH) * 0.52
rq3_h = (CH - HDH) * 0.44
rq3_y = BOT + 0.04
rq2_y = rq3_y + rq3_h + 0.06

sub_w = (rqW - 0.32) / 2
s1x = rqX + 0.16
s2x = rqX + 0.20 + sub_w

# ─── RQ2 ──────────────────────────────────────────────────────────────────
hdr(rqX+0.12, rq2_y+rq2_h-HDH, rqW-0.24, HDH,
    "RQ2:  SPECIFICATION FLEXIBILITY ANALYSIS", fs=8.0)
box(rqX+0.12, rq2_y, rqW-0.24, rq2_h, ls=(0,(4,2)), z=2)

# sub-col 1: Schema vs. Spec Prose
t(s1x+sub_w/2, rq2_y+rq2_h-HDH-0.20,
  "Spec Prose vs. Schema Analysis", fs=8.0, fw="bold")
t(s1x+sub_w/2, rq2_y+rq2_h-HDH-0.44,
  "Compare normative prose\nwith official JSON/XML schemas",
  fs=8.0, col=MED)
# two boxes with "Prose" vs "Schema"
box(s1x+0.06, rq2_y+0.14, sub_w*0.44, 0.38, fc=BOX, ec=BORD, lw=0.8, z=6)
t(s1x+0.06+sub_w*0.22, rq2_y+0.33, "Normative\nProse", fs=8.0)
t(s1x+sub_w/2, rq2_y+0.33, "→", fs=9, fw="bold")
box(s1x+sub_w*0.52, rq2_y+0.14, sub_w*0.44, 0.38, fc=BOX, ec=BORD, lw=0.8, z=6)
t(s1x+sub_w*0.52+sub_w*0.22, rq2_y+0.33, "Official\nSchema", fs=8.0)

# sub-col 2: Conditionality
t(s2x+sub_w/2, rq2_y+rq2_h-HDH-0.20,
  "Conditionality Analysis\n", fs=8.0, fw="bold")
t(s2x+sub_w/2, rq2_y+rq2_h-HDH-0.44,
  "Classify requirements as:\nbaseline (always) vs.\nconditional (context-dependent)",
  fs=8.0, col=MED)
# baseline/conditional boxes — centered within the right sub-column
_bw, _cw, _gap = 0.60, 0.75, 0.10
_total = _bw + _gap + _cw
_bx = s2x + (sub_w - _total) / 2          # left edge of Baseline box
box(_bx,         rq2_y+0.20, _bw, 0.22, fc="#c8e6c9", ec=BORD, lw=0.7, z=6)
t(_bx + _bw/2,   rq2_y+0.31, "Baseline",    fs=8.0)
box(_bx+_bw+_gap, rq2_y+0.20, _cw, 0.22, fc="#fff9c4", ec=BORD, lw=0.7, z=6)
t(_bx+_bw+_gap+_cw/2, rq2_y+0.31, "Conditional", fs=8.0)

# divider
ax.plot([rqX+0.12+sub_w+0.06]*2,
        [rq2_y+0.06, rq2_y+rq2_h-HDH-0.04],
        color=BORD, lw=0.7, ls="--", zorder=5)

# ─── RQ3 ──────────────────────────────────────────────────────────────────
hdr(rqX+0.12, rq3_y+rq3_h-HDH, rqW-0.24, HDH,
    "RQ3:  IMPLEMENTATION INSPECTION", fs=8.0)
box(rqX+0.12, rq3_y, rqW-0.24, rq3_h, ls=(0,(4,2)), z=2)

c3sw = (rqW-0.36)/3

rq3_content = [
    (
        "1. Tool Selection",
        "Syft, Trivy, cdxgen,\nMS-SBOM Tool\n(4 tools total)",
    ),
    (
        "2. Static Inspection",
        "Source code analysis:\nfield population logic,\ndep. graph construction,\nscope/filter behavior",
    ),
    (
        "3. Dynamic Analysis",
        "40 selected PyPI/Maven\nrepositories;\nbounded output checks",
    ),
]

for ci, (sub_title, body) in enumerate(rq3_content):
    cx = rqX + 0.16 + ci*c3sw
    t(cx+c3sw/2, rq3_y+rq3_h-HDH-0.18, sub_title, fs=8.0, fw="bold")
    t(cx+c3sw/2, rq3_y+rq3_h-HDH-0.66, body, fs=8.0, col=MED)
    if ci < 2:
        sep_x = rqX+0.12+(ci+1)*c3sw
        ax.plot([sep_x]*2,
                [rq3_y+0.04, rq3_y+rq3_h-HDH-0.04],
                color=BORD, lw=0.7, ls="--", zorder=5)
        arr_y = rq3_y + (rq3_h-HDH)/2
        arr(sep_x - 0.15, arr_y, sep_x + 0.15, arr_y, lw=1.5)

# ══════════════════════════════════════════════════════════════════════════
# COL SYNTHESIS — RQ4
# ══════════════════════════════════════════════════════════════════════════
hdr(c5x, TOP-HDH, c5w, HDH, "INTERFACE-BOUNDARY SYNTHESIS", fs=7.5)
box(c5x, BOT, c5w, CH-HDH)

synth_sections = [
    ("8 Interface Classes Summarized:", True),
    ("For each class, map:", False),
    ("  • Specification clause/boundary", False),
    ("  • Source/output evidence", False),
    ("  • Artifact-level risk", False),
    ("  • Mitigation/conformance check", False),
    ("", False),
    ("Classes include:", True),
    ("Missing provenance · Shallow graphs", False),
    ("Scope disagreement · Leaf ambiguity", False),
    ("Schema/prose mismatch · VEX absence", False),
    ("Producer-consumer asymmetry", False),
]
sy = TOP - HDH - 0.22
for s, bold in synth_sections:
    if s:
        t(c5x+0.12, sy, s, fs=8.5, fw="bold" if bold else "normal",
          ha="left", col=DARK)
    sy -= 0.25

# ══════════════════════════════════════════════════════════════════════════
# ARROWS
# ══════════════════════════════════════════════════════════════════════════
mid_y = (TOP + BOT) / 2

arr(c0x+c0w, mid_y, c1x, mid_y)
arr(c1x+c1w, mid_y, c2x, mid_y)
arr(c2x+c2w, mid_y, c3x, mid_y)

rq2_mid = rq2_y + rq2_h/2
rq3_mid = rq3_y + rq3_h/2
arr(c3x+c3w, rq2_mid, rqX+0.12, rq2_mid)
arr(c3x+c3w, rq3_mid, rqX+0.12, rq3_mid)
arr(rqX+rqW-0.12, rq2_mid, c5x, rq2_mid)
arr(rqX+rqW-0.12, rq3_mid, c5x, rq3_mid)

out_path = "/Users/abdullahsohail/abdullahsohail/undergrad_research/SSC/updated_scored/figures/methodology_pipeline.png"
plt.tight_layout(pad=0.05)
fig.savefig(out_path, dpi=220, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved: {out_path}")
