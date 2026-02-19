# Youth Unemployment Data: France and United Kingdom (2000-2024)

This repository contains youth unemployment rate data (ages 15-24) for France and the United Kingdom from 2000 to 2024, along with a Python script to download and process the data.

## Data Source

The data is sourced from **Our World in Data**, which provides harmonized, modelled estimates from the **International Labour Organization (ILO)**. This ensures cross-country comparability and consistent methodology.

- **Indicator**: Youth unemployment rate (ages 15-24, % of labor force in that age group)
- **Countries**: France, United Kingdom
- **Period**: 2000-2024
- **Source URL**: https://ourworldindata.org/grapher/unemployment-rate-for-young-people

## Files

- `youth_unemployment_15_24_FR_UK_2000_2024.csv` - Filtered dataset containing annual youth unemployment rates for France and UK
- `download_youth_unemployment_15_24_FR_UK.py` - Python script to download and filter the data from Our World in Data

## Usage

### Download the data

```bash
python download_youth_unemployment_15_24_FR_UK.py
```

This will download the latest data from Our World in Data and save it as `youth_unemployment_15_24_FR_UK_2000_2024.csv`.

## Data Format

The CSV file contains the following columns:
- `Entity`: Country name (France or United Kingdom)
- `Code`: ISO country code (FRA or GBR)
- `Year`: Year of observation
- `Unemployment rate, ages 15-24`: Youth unemployment rate as a percentage



