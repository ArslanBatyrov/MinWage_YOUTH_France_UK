# Youth Unemployment Data: France and United Kingdom (2000-2024)

This repository contains youth unemployment rate data (ages 15-24) for France and the United Kingdom from 2000 to 2024, along with a Python script to download and process the data.

## Data Source

The data is sourced from **Our World in Data**, which provides harmonized, modelled estimates from the **International Labour Organization (ILO)**. This ensures cross-country comparability and consistent methodology.

- **Indicator**: Youth unemployment rate (ages 15-24, % of labor force in that age group)
- **Countries**: France, United Kingdom
- **Period**: 2000-2024
- **Source URL**: https://ourworldindata.org/grapher/unemployment-rate-for-young-people

## Files

### Data
- `data/youth_unemployment_15_24_FR_UK_2000_2024.csv` - Youth unemployment rates for France and UK
- `data/minimum_wage_FR_UK_2000_2024.csv` - Minimum wage (USD) for France and UK
- `NATTIONAL MINIMUM WAGE.xlsx` - UK National Minimum Wage / National Living Wage history (GBP) from official sources

### Scripts
- `analysis/download_youth_unemployment_15_24_FR_UK.py` - Download youth unemployment data from Our World in Data
- `analysis/load_national_minimum_wage.py` - Load and process UK NMW/NLW from the Excel file
- `analysis/plot_unemployment_minwage.py` - Generate graphs combining youth unemployment and minimum wage

## Usage

### Download the data

```bash
python download_youth_unemployment_15_24_FR_UK.py
```

This will download the latest data from Our World in Data and save it as `data/youth_unemployment_15_24_FR_UK_2000_2024.csv`.

### Generate graphs

```bash
pip install -r requirements.txt
python analysis/plot_unemployment_minwage.py
```

This produces, in `outputs/`:
- `fig_unemployment_minwage_FR.pdf` / `.png` - France: youth unemployment + minimum wage (USD)
- `fig_unemployment_minwage_UK.pdf` / `.png` - UK: youth unemployment + National Minimum Wage (GBP, from Excel)
- `fig_youth_unemployment_FR_UK.pdf` / `.png` - Combined youth unemployment for both countries

## Data Format

The CSV file contains the following columns:
- `Entity`: Country name (France or United Kingdom)
- `Code`: ISO country code (FRA or GBR)
- `Year`: Year of observation
- `Unemployment rate, ages 15-24`: Youth unemployment rate as a percentage





