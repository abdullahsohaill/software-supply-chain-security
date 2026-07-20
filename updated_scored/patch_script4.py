import sys

with open("figures/gen_methodology.py", "r") as f:
    code = f.read()

# 1. Req Extraction block - Total Requirements
code = code.replace(
    't(c1x+c1w/2, corpus_y+0.71, "Total Corpus: 2,286 requirements",\n  fs=7, fw="bold")',
    't(c1x+c1w/2, corpus_y+0.71, "Total Requirements: 2,286",\n  fs=8, fw="bold")'
)

# 2. Headings (REQUIREMENT EXTRACTION and THEMATIC CODING & ANALYSIS)
# REQUIREMENT EXTRACTION is at fs=6.8, let's split into two lines and increase to fs=7.5
code = code.replace(
    'hdr(c1x, TOP-HDH, c1w, HDH, "REQUIREMENT EXTRACTION", fs=6.8)',
    'hdr(c1x, TOP-HDH, c1w, HDH, "REQUIREMENT\\nEXTRACTION", fs=7.5)'
)
# THEMATIC CODING & ANALYSIS
code = code.replace(
    'hdr(c2x, TOP-HDH, c2w, HDH, "THEMATIC CODING & ANALYSIS", fs=6.8)',
    'hdr(c2x, TOP-HDH, c2w, HDH, "THEMATIC CODING\\n& ANALYSIS", fs=7.5)'
)

# 3. RQ2/RQ3 Sub-boxes (normative prose, annotator schema, baseline, conditional)
code = code.replace(
    't(s1x+0.06+sub_w*0.22, rq2_y+0.33, "Normative\\nProse", fs=6.5)',
    't(s1x+0.06+sub_w*0.22, rq2_y+0.33, "Normative\\nProse", fs=7.5)'
)
code = code.replace(
    't(s1x+sub_w*0.52+sub_w*0.22, rq2_y+0.33, "Annotator\\nSchema", fs=6.5)',
    't(s1x+sub_w*0.52+sub_w*0.22, rq2_y+0.33, "Annotator\\nSchema", fs=7.5)'
)
code = code.replace(
    't(_bx + _bw/2,   rq2_y+0.31, "Baseline",    fs=6.5)',
    't(_bx + _bw/2,   rq2_y+0.31, "Baseline",    fs=7.5)'
)
code = code.replace(
    't(_bx+_bw+_gap+_cw/2, rq2_y+0.31, "Conditional", fs=6.5)',
    't(_bx+_bw+_gap+_cw/2, rq2_y+0.31, "Conditional", fs=7.5)'
)

# 4. Taxonomy Block
# Move 3-Level Hierarchy up
code = code.replace(
    't(c3x+c3w/2, BOT+0.38,\n  "3-Level Hierarchy\\n(Systematic Framework)",\n  fs=6.8, col=MED)',
    't(c3x+c3w/2, BOT+0.58,\n  "3-Level Hierarchy\\n(Systematic Framework)",\n  fs=6.8, col=MED)'
)

# Increase font size of 'Requirements' by one point
code = code.replace(
    'oval_w, oval_h = 1.0, 0.30\nbox(rx - oval_w/2, ry - oval_h/2, oval_w, oval_h, fc=HDR, ec=BORD, lw=0.8, r=0.15, z=7)\nr_rad = oval_h/2\nt(rx, ry, "Requirements", fs=6.5, fw="bold", col="white")',
    'oval_w, oval_h = 1.1, 0.35\nbox(rx - oval_w/2, ry - oval_h/2, oval_w, oval_h, fc=HDR, ec=BORD, lw=0.8, r=0.17, z=7)\nr_rad = oval_h/2\nt(rx, ry, "Requirements", fs=7.5, fw="bold", col="white")'
)


with open("figures/gen_methodology.py", "w") as f:
    f.write(code)

