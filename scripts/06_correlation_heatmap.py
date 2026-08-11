"""
06_correlation_heatmap.py
--------------------------
Reads the pre-computed correlation matrix produced by
04_correlation_and_portfolio_vol.py and renders it as a publication-quality
heatmap, then saves the figure to reports/correlation_heatmap.png.

Inputs:
    data/raw/correlation_matrix.csv   — N x N pairwise correlations

Outputs:
    reports/correlation_heatmap.png   — heatmap at 150 DPI
"""

import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ---------------------------------------------------------------------------
# 1. Make sure the output folder exists
# ---------------------------------------------------------------------------
# os.makedirs with exist_ok=True creates every missing directory in the path
# and does nothing (no error) if the folder is already there.  This means
# the script is safe to re-run without manual folder setup.
os.makedirs("reports", exist_ok=True)

# ---------------------------------------------------------------------------
# 2. Load the correlation matrix
# ---------------------------------------------------------------------------
# The CSV has ticker symbols as both the row index (first column) and the
# column headers.  index_col=0 tells pandas to treat that first column as
# the row labels rather than a data column, giving us a square DataFrame
# whose rows and columns are both indexed by ticker.
corr = pd.read_csv("data/raw/correlation_matrix.csv", index_col=0)

print(f"Loaded {corr.shape[0]}x{corr.shape[1]} correlation matrix.")
print(f"Tickers: {corr.columns.tolist()}\n")

# ---------------------------------------------------------------------------
# 3. Create the figure and axes
# ---------------------------------------------------------------------------
# figsize=(10, 8) gives a canvas that's wide enough for 10 tickers with
# readable labels.  tight_layout() is called later to avoid clipping.
fig, ax = plt.subplots(figsize=(10, 8))

# ---------------------------------------------------------------------------
# 4. Draw the heatmap
# ---------------------------------------------------------------------------
# sns.heatmap arguments explained:
#
#   data        — the square DataFrame of correlations
#   annot=True  — print the numeric value inside every cell
#   fmt=".2f"   — format those numbers to exactly 2 decimal places (e.g. 0.87)
#   cmap        — colour palette; "RdBu_r" is a diverging red-blue scale where
#                   red  = strong negative correlation (approx -1)
#                   white = zero correlation (approx 0)
#                   blue  = strong positive correlation (approx +1)
#                 The "_r" suffix reverses the default direction so blue sits
#                 on the positive side, matching financial convention.
#   vmin / vmax — pin the colour scale endpoints to -1 and +1 so the midpoint
#                 white always represents zero, regardless of the actual data
#                 range.  Without this, seaborn would auto-scale and white
#                 would shift away from zero if no pair reaches -1 or +1.
#   linewidths  — thin grid lines between cells make individual cells easier
#                 to read when many tickers are shown.
#   linecolor   — subtle grey rather than harsh black for the grid lines.
#   square      — force each cell to be square so the matrix looks symmetric.
#   ax          — draw onto the axes we created above (good practice when
#                 embedding in larger figures later).
sns.heatmap(
    data=corr,
    annot=True,
    fmt=".2f",
    cmap="RdBu_r",
    vmin=-1,
    vmax=1,
    linewidths=0.5,
    linecolor="lightgrey",
    square=True,
    ax=ax,
)

# ---------------------------------------------------------------------------
# 5. Cosmetic finishing touches
# ---------------------------------------------------------------------------
# Set the chart title.  fontsize=14 and fontweight="bold" make it stand out
# above the dense grid of numbers.  pad=12 adds a little breathing room
# between the title and the top of the heatmap.
ax.set_title(
    "Correlation Matrix \u2014 10-Stock Basket",
    fontsize=14,
    fontweight="bold",
    pad=12,
)

# Rotate the x-axis tick labels (column names) to horizontal so they don't
# overlap each other.  ha="center" keeps each label centred under its column.
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha="center")

# Keep the y-axis labels upright too -- easier to scan than rotated text.
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

# tight_layout() automatically adjusts margins so nothing gets clipped,
# especially useful when tick labels are long.
fig.tight_layout()

# ---------------------------------------------------------------------------
# 6. Save the figure
# ---------------------------------------------------------------------------
# dpi=150 is a good middle ground: crisp enough for presentations and PDF
# reports, but not as heavy as 300 dpi print resolution.
# bbox_inches="tight" trims any extra whitespace around the figure edges.
output_path = "reports/correlation_heatmap.png"
fig.savefig(output_path, dpi=150, bbox_inches="tight")

print(f"Heatmap saved to {output_path}")
