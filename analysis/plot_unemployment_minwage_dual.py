"""
Create dual-axis graphs showing youth unemployment and minimum wage changes
for France and UK separately.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# Paths
# -----------------------------
UNEMP_DATA = os.path.join("data", "youth_unemployment_15_24_FR_UK_2000_2024.csv")
MINWAGE_DATA = os.path.join("data", "minimum_wage_FR_UK_2000_2024.csv")
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

# -----------------------------
# Load data
# -----------------------------
print("Loading unemployment data...")
df_unemp = pd.read_csv(UNEMP_DATA)

print("Loading minimum wage data...")
if not os.path.exists(MINWAGE_DATA):
    raise FileNotFoundError(
        f"Minimum wage data not found at {MINWAGE_DATA}. "
        "Please download or create this file first."
    )
df_mw = pd.read_csv(MINWAGE_DATA)

# -----------------------------
# Process unemployment data
# -----------------------------
df_unemp_wide = df_unemp.pivot(index="Year", columns="Entity", values="Unemployment rate, ages 15-24")

# -----------------------------
# Process minimum wage data
# -----------------------------
# Find the minimum wage column (could be named differently)
mw_col = None
for col in df_mw.columns:
    if "minimum" in col.lower() or "wage" in col.lower() or "smic" in col.lower():
        mw_col = col
        break

if mw_col is None:
    # Try to find numeric column that's not Year, Entity, or Code
    numeric_cols = df_mw.select_dtypes(include=[np.number]).columns.tolist()
    for col in ["Year", "Entity", "Code"]:
        if col in numeric_cols:
            numeric_cols.remove(col)
    if numeric_cols:
        mw_col = numeric_cols[0]
        print(f"Using column '{mw_col}' as minimum wage")
    else:
        raise ValueError("Could not identify minimum wage column in CSV")

df_mw_wide = df_mw.pivot(index="Year", columns="Entity", values=mw_col)

# Calculate annual percentage changes
df_mw_pct_change = df_mw_wide.pct_change() * 100

# -----------------------------
# Economic Journal styling
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

# -----------------------------
# Plot France
# -----------------------------
def plot_country(country_name, country_code):
    fig, ax1 = plt.subplots(figsize=(6.8, 4.2))
    
    # Left axis: Youth unemployment
    color_unemp = "black"
    ax1.set_xlabel("Year", fontsize=10)
    ax1.set_ylabel("Youth unemployment rate (15–24), %", color=color_unemp, fontsize=10)
    
    years = df_unemp_wide.index.astype(int)
    unemp_values = df_unemp_wide[country_name].values
    
    ax1.plot(years, unemp_values, color=color_unemp, linestyle="-", marker="o", 
             markersize=3.2, linewidth=1.2, label="Youth unemployment")
    ax1.tick_params(axis="y", labelcolor=color_unemp)
    ax1.grid(axis="y", linewidth=0.4, alpha=0.35)
    
    # Right axis: Minimum wage annual % change
    ax2 = ax1.twinx()
    color_mw = "red"
    ax2.set_ylabel("Minimum wage annual change, %", color=color_mw, fontsize=10)
    
    # Align years between datasets
    mw_years = df_mw_pct_change.index.astype(int)
    mw_values = df_mw_pct_change[country_name].values
    
    # Only plot where we have data
    valid_mask = ~np.isnan(mw_values)
    ax2.plot(mw_years[valid_mask], mw_values[valid_mask], 
             color=color_mw, linestyle="--", marker="s", 
             markersize=3.2, linewidth=1.2, label="Min wage change")
    ax2.tick_params(axis="y", labelcolor=color_mw)
    ax2.axhline(y=0, color=color_mw, linestyle=":", linewidth=0.5, alpha=0.5)
    
    # Title
    ax1.set_title(f"Youth Unemployment and Minimum Wage Changes: {country_name}, 2000–2024", pad=8)
    
    # X-axis ticks
    if len(years) > 0:
        step = 5
        xticks = [t for t in years if (t - years[0]) % step == 0] + ([years[-1]] if years[-1] not in [t for t in years if (t - years[0]) % step == 0] else [])
        ax1.set_xticks(sorted(set(xticks)))
    
    # Legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, frameon=False, loc="upper left")
    
    fig.tight_layout()
    
    # Save
    out_pdf = os.path.join(OUT_DIR, f"fig_unemployment_minwage_{country_code}.pdf")
    out_png = os.path.join(OUT_DIR, f"fig_unemployment_minwage_{country_code}.png")
    fig.savefig(out_pdf, bbox_inches="tight")
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    
    print(f"Saved: {out_pdf}")
    print(f"Saved: {out_png}")

# Plot both countries
print("\nCreating graph for France...")
plot_country("France", "FR")

print("\nCreating graph for United Kingdom...")
plot_country("United Kingdom", "UK")

print("\nDone!")

