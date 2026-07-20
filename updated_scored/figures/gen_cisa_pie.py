import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Data
labels = [
    'Component & SBOM Attributes',
    'SBOM Operations & Lifecycle',
    'Data Governance & Transparency',
    'Supply Chain Relationships',
    'Foundational Principles',
    'Use Case Enablement'
]
sizes = [36.1, 29.3, 12.8, 9.0, 8.3, 4.5]

import numpy as np

# Colors derived from the methodology pipeline script
colors = [
    "#2d2d3a", # HDR dark slate
    "#52526a", # MED slate
    "#9999aa", # LITE slate
    "#c8e6c9", # pale green
    "#fff9c4", # pale yellow
    "#e4e7ed"  # BOX light grey
]

# Matplotlib figure
fig, ax = plt.subplots(figsize=(14, 8), subplot_kw=dict(aspect="equal"))
fig.patch.set_facecolor('white')

# Combine labels and percentages
combined_labels = [f"{label}\n{size}%" for label, size in zip(labels, sizes)]

# Create donut chart without default labels
wedges, texts = ax.pie(
    sizes, 
    colors=colors, 
    startangle=140,
    wedgeprops=dict(width=0.4, edgecolor='white', linewidth=1.5)
)

# Add callout lines and labels
kw = dict(arrowprops=dict(arrowstyle="-", color="black", lw=1.5),
          zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1) / 2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    
    # Position the text further out
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = f"angle,angleA=0,angleB={ang}"
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    
    # Base label position
    y_text = 1.25 * y
    
    # Manual offsets to prevent overlapping labels on the top-left
    if i == 4: # Foundational Principles
        y_text += 0.25
    elif i == 5: # Use Case Enablement
        y_text -= 0.15
    
    # xy is on the outer edge of the pie (radius=1)
    # xytext is the label position
    ax.annotate(combined_labels[i], xy=(x, y), xytext=(1.25 * np.sign(x), y_text),
                horizontalalignment=horizontalalignment, fontsize=24, color="black", 
                multialignment='center', **kw)

plt.tight_layout()
out_path = "cisa_theme_pie.pdf"
fig.savefig(out_path, bbox_inches="tight", dpi=300)
print(f"Saved: {out_path}")
