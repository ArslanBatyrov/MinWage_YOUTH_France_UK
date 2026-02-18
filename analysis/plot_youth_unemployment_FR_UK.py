import os
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Paths
# -----------------------------
DATA_PATH = os.path.join("data", "youth_unemployment_15_24_FR_UK_2000_2024.csv")
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

OUT_PDF = os.path.join(OUT_DIR, "fig_youth_unemployment_FR_UK.pdf")
OUT_PNG = os.path.join(OUT_DIR, "fig_youth_unemployment_FR_UK.png")

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(DATA_PATH)

# Data is in long format: Entity, Code, Year, Unemployment rate
# Pivot to wide format for plotting
unemp_col = "Unemployment rate, ages 15-24"
df_wide = df.pivot(index="Year", columns="Entity", values=unemp_col)

# Extract France and UK columns
if "France" not in df_wide.columns or "United Kingdom" not in df_wide.columns:
    raise ValueError("Could not find France and United Kingdom in data. Check CSV structure.")

df_wide = df_wide[["France", "United Kingdom"]].dropna()
df_wide = df_wide.sort_index()

x = df_wide.index.astype(int).to_numpy()
y_fr = df_wide["France"].astype(float).to_numpy()
y_uk = df_wide["United Kingdom"].astype(float).to_numpy()

# -----------------------------
# Economic Journal-ish styling
# (clean, B/W friendly, minimal ink, readable in print)
# -----------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.direction": "out",
    "ytick.direction": "out",
})

fig, ax = plt.subplots(figsize=(6.8, 4.2))  # journal column-friendly

# Use marker+linestyle but keep it print-friendly
ax.plot(x, y_fr, linestyle="-", marker="o", markersize=3.2, linewidth=1.2, label="France")
ax.plot(x, y_uk, linestyle="-", marker="o", markersize=3.2, linewidth=1.2, label="United Kingdom")

ax.set_title("Youth Unemployment Rate (Ages 15–24), France vs United Kingdom, 2000–2024", pad=8)
ax.set_xlabel("Year")
ax.set_ylabel("Youth unemployment rate (15–24), %")

# Subtle grid (y only)
ax.grid(axis="y", linewidth=0.4, alpha=0.35)
ax.grid(axis="x", visible=False)

# Ticks: show fewer years to avoid clutter
if len(x) > 0:
    step = 5
    xticks = [t for t in x if (t - x[0]) % step == 0] + ([x[-1]] if x[-1] not in [t for t in x if (t - x[0]) % step == 0] else [])
    ax.set_xticks(sorted(set(xticks)))

# Legend: clean, no box
ax.legend(frameon=False, loc="upper left")

fig.tight_layout()

# Save vector + raster
fig.savefig(OUT_PDF, bbox_inches="tight")
fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {OUT_PDF}")
print(f"Saved: {OUT_PNG}")

