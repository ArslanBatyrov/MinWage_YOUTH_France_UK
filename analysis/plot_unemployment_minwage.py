"""
Generate graphs of youth unemployment and minimum wage for France and the United Kingdom.
Uses real data from:
  - Youth unemployment: youth_unemployment_15_24_FR_UK_2000_2024.csv
  - Minimum wage: NATTIONAL MINIMUM WAGE.xlsx (UK, GBP) and minimum_wage_FR_UK_2000_2024.csv (FR, USD)
"""
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for headless/sandbox
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from load_national_minimum_wage import load_uk_nmw_from_excel


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    data_dir = base / "data"
    outputs_dir = base / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    # Paths
    unemployment_path = data_dir / "youth_unemployment_15_24_FR_UK_2000_2024.csv"
    minwage_csv_path = data_dir / "minimum_wage_FR_UK_2000_2024.csv"
    excel_path = base / "NATTIONAL MINIMUM WAGE.xlsx"

    # Load youth unemployment
    unemp = pd.read_csv(unemployment_path)
    unemp["Year"] = unemp["Year"].astype(int)
    unemp_col = "Unemployment rate, ages 15-24"

    # Load minimum wage: France from CSV (USD), UK from Excel (GBP)
    mw_csv = pd.read_csv(minwage_csv_path)
    mw_csv["Year"] = mw_csv["Year"].astype(int)
    mw_fr = mw_csv[mw_csv["Code"] == "FRA"][["Year", "Minimum wage (USD)"]].copy()
    mw_fr = mw_fr.rename(columns={"Minimum wage (USD)": "MinWage"})
    mw_fr["Unit"] = "USD"

    uk_nmw = load_uk_nmw_from_excel(excel_path)
    mw_uk = uk_nmw.rename(columns={"MinWage_GBP": "MinWage"})
    mw_uk["Unit"] = "GBP"

    # Filter to common year range
    years = range(2000, 2025)
    mw_fr = mw_fr[mw_fr["Year"].isin(years)]
    mw_uk = mw_uk[mw_uk["Year"].isin(years)]

    # --- France: youth unemployment + minimum wage ---
    u_fr = unemp[unemp["Code"] == "FRA"]
    u_fr = u_fr[u_fr["Year"].isin(years)].sort_values("Year")
    mw_fr = mw_fr.sort_values("Year")

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(
        u_fr["Year"],
        u_fr[unemp_col],
        color="tab:blue",
        marker="o",
        linewidth=2,
        markersize=5,
        label="Youth unemployment (15–24, %)",
    )
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Youth unemployment rate (%)", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    ax1.set_xlim(1999.5, 2024.5)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(
        mw_fr["Year"],
        mw_fr["MinWage"],
        color="tab:orange",
        marker="s",
        linewidth=2,
        markersize=5,
        label="Minimum wage (USD)",
    )
    ax2.set_ylabel("Minimum wage (USD)", color="tab:orange")
    ax2.tick_params(axis="y", labelcolor="tab:orange")

    ax1.set_title("France: Youth Unemployment and Minimum Wage (2000–2024)")
    fig1.tight_layout()
    fig1.savefig(outputs_dir / "fig_unemployment_minwage_FR.pdf", bbox_inches="tight")
    fig1.savefig(outputs_dir / "fig_unemployment_minwage_FR.png", dpi=150, bbox_inches="tight")
    plt.close(fig1)

    # --- UK: youth unemployment + minimum wage ---
    u_uk = unemp[unemp["Code"] == "GBR"]
    u_uk = u_uk[u_uk["Year"].isin(years)].sort_values("Year")
    mw_uk = mw_uk.sort_values("Year")

    fig2, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(
        u_uk["Year"],
        u_uk[unemp_col],
        color="tab:blue",
        marker="o",
        linewidth=2,
        markersize=5,
        label="Youth unemployment (15–24, %)",
    )
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Youth unemployment rate (%)", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    ax1.set_xlim(1999.5, 2024.5)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(
        mw_uk["Year"],
        mw_uk["MinWage"],
        color="tab:orange",
        marker="s",
        linewidth=2,
        markersize=5,
        label="National Minimum Wage / NLW (GBP)",
    )
    ax2.set_ylabel("Minimum wage (GBP)", color="tab:orange")
    ax2.tick_params(axis="y", labelcolor="tab:orange")

    ax1.set_title("United Kingdom: Youth Unemployment and National Minimum Wage (2000–2024)")
    fig2.tight_layout()
    fig2.savefig(outputs_dir / "fig_unemployment_minwage_UK.pdf", bbox_inches="tight")
    fig2.savefig(outputs_dir / "fig_unemployment_minwage_UK.png", dpi=150, bbox_inches="tight")
    plt.close(fig2)

    # --- Combined: youth unemployment (both countries) ---
    u_both = unemp[unemp["Year"].isin(years)].sort_values(["Code", "Year"])
    fr = u_both[u_both["Code"] == "FRA"]
    uk = u_both[u_both["Code"] == "GBR"]

    fig3, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        fr["Year"],
        fr[unemp_col],
        color="tab:blue",
        marker="o",
        linewidth=2,
        markersize=5,
        label="France",
    )
    ax.plot(
        uk["Year"],
        uk[unemp_col],
        color="tab:orange",
        marker="s",
        linewidth=2,
        markersize=5,
        label="United Kingdom",
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Youth unemployment rate (ages 15–24, %)")
    ax.set_xlim(1999.5, 2024.5)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_title("Youth Unemployment: France and United Kingdom (2000–2024)")
    fig3.tight_layout()
    fig3.savefig(outputs_dir / "fig_youth_unemployment_FR_UK.pdf", bbox_inches="tight")
    fig3.savefig(outputs_dir / "fig_youth_unemployment_FR_UK.png", dpi=150, bbox_inches="tight")
    plt.close(fig3)

    print("Saved:")
    print("  - outputs/fig_unemployment_minwage_FR.pdf, .png")
    print("  - outputs/fig_unemployment_minwage_UK.pdf, .png")
    print("  - outputs/fig_youth_unemployment_FR_UK.pdf, .png")


if __name__ == "__main__":
    main()
