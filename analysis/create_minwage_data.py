"""
Create minimum wage data CSV from manual entry or download.
This script helps create the minimum_wage_FR_UK_2000_2024.csv file.
"""
import os
import pandas as pd
from pathlib import Path

# Get project root
script_dir = Path(__file__).parent
project_root = script_dir.parent
data_dir = project_root / "data"

# Known minimum wage values (approximate, in USD PPP-adjusted)
# You should replace these with actual data from official sources
MIN_WAGE_DATA = {
    "France": {
        2000: 6.41, 2001: 6.67, 2002: 6.83, 2003: 7.19, 2004: 7.61,
        2005: 7.95, 2006: 8.27, 2007: 8.44, 2008: 8.71, 2009: 9.00,
        2010: 9.22, 2011: 9.40, 2012: 9.43, 2013: 9.53, 2014: 9.61,
        2015: 9.67, 2016: 9.76, 2017: 9.88, 2018: 10.03, 2019: 10.15,
        2020: 10.25, 2021: 10.48, 2022: 10.57, 2023: 11.27, 2024: 11.65
    },
    "United Kingdom": {
        2000: 4.70, 2001: 4.85, 2002: 4.85, 2003: 4.85, 2004: 5.05,
        2005: 5.35, 2006: 5.52, 2007: 5.73, 2008: 5.73, 2009: 5.80,
        2010: 5.93, 2011: 6.08, 2012: 6.19, 2013: 6.31, 2014: 6.50,
        2015: 6.70, 2016: 7.20, 2017: 7.50, 2018: 7.83, 2019: 8.21,
        2020: 8.72, 2021: 8.91, 2022: 9.50, 2023: 10.42, 2024: 11.44
    }
}

def create_minwage_csv():
    """Create minimum wage CSV file from data dictionary."""
    rows = []
    for country in ["France", "United Kingdom"]:
        code = "FRA" if country == "France" else "GBR"
        for year in range(2000, 2025):
            rows.append({
                "Entity": country,
                "Code": code,
                "Year": year,
                "Minimum wage (USD)": MIN_WAGE_DATA[country].get(year, None)
            })
    
    df = pd.DataFrame(rows)
    output_path = data_dir / "minimum_wage_FR_UK_2000_2024.csv"
    df.to_csv(output_path, index=False)
    print(f"Created minimum wage CSV at: {output_path}")
    print(f"Note: These are approximate values. Please verify with official sources.")
    return output_path

if __name__ == "__main__":
    create_minwage_csv()

