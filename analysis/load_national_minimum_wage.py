"""
Load and process National Minimum Wage data from the NATTIONAL MINIMUM WAGE.xlsx file.
Extracts UK NMW/NLW rates (GBP) and produces an annual series for plotting.
"""
from pathlib import Path

import pandas as pd


def load_uk_nmw_from_excel(excel_path: Path) -> pd.DataFrame:
    """Load UK National Minimum Wage from Excel and return annual rates in GBP."""
    df = pd.read_excel(excel_path, sheet_name="Sheet1", header=1)

    # First column is Month, parse dates and filter out note rows
    df = df.copy()
    df["Month"] = pd.to_datetime(df.iloc[:, 0], errors="coerce")
    df = df.dropna(subset=["Month"])

    # Filter out rows where Month is clearly a note (e.g. contains text)
    df = df[df["Month"].dt.year >= 1999]

    # Main adult rate: prefer NLW (25+), then 21+ rate, then 22+ rate
    def main_rate(r):
        v = r.get("NLW (25+)")
        if pd.notna(v):
            return float(v)
        v = r.get("21+ rate")
        if pd.notna(v):
            return float(v)
        v = r.get("22+ rate")
        if pd.notna(v):
            return float(v)
        return None

    rates = []
    for _, row in df.iterrows():
        y = row["Month"].year
        v = main_rate(row)
        if v is not None:
            rates.append({"Year": y, "MinWage_GBP": v})

    out = pd.DataFrame(rates)

    # One value per year: take the last (most recent) rate in each year
    out = out.groupby("Year", as_index=False).last()

    # Extend with known NLW rates for 2020-2024 (UK government)
    extra = pd.DataFrame({
        "Year": [2020, 2021, 2022, 2023, 2024],
        "MinWage_GBP": [8.72, 8.91, 9.50, 10.42, 11.44],
    })
    out = pd.concat([out, extra], ignore_index=True).drop_duplicates(subset=["Year"], keep="last")
    out = out.sort_values("Year").reset_index(drop=True)

    return out
