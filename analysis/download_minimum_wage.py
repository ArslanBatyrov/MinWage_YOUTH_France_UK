import csv
import io
import sys
from pathlib import Path
from urllib.request import Request, urlopen


# Try multiple potential URLs for minimum wage data
POTENTIAL_URLS = [
    "https://ourworldindata.org/grapher/minimum-wage-levels.csv",
    "https://ourworldindata.org/grapher/minimum-wage.csv",
    "https://ourworldindata.org/grapher/statutory-minimum-wage.csv",
]


def download_and_filter(
    url: str,
    countries=("France", "United Kingdom"),
    start_year: int = 2000,
    end_year: int = 2024,
    output_path: Path | None = None,
) -> Path:
    """
    Download minimum wage data from Our World in Data,
    filter for given countries and year range, and save as a CSV.
    """
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    if output_path is None:
        output_path = project_root / "data" / "minimum_wage_FR_UK_2000_2024.csv"

    print(f"Trying URL: {url} ...")
    # Some servers may return 403 to requests without a browser-like User-Agent
    req = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        },
    )

    try:
        with urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Failed to download from {url}: {e}")

    reader = csv.DictReader(io.StringIO(raw))
    rows = []
    for row in reader:
        try:
            year = int(row["Year"])
        except (KeyError, ValueError):
            continue

        if row.get("Entity") in countries and start_year <= year <= end_year:
            rows.append(row)

    if not rows:
        raise RuntimeError("No rows matched the filters; check URL or filters.")

    fieldnames = list(rows[0].keys())
    output_path = Path(output_path)

    print(f"Writing filtered data to {output_path.resolve()} ...")
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Done.")
    return output_path


if __name__ == "__main__":
    # Try each URL until one works
    for url in POTENTIAL_URLS:
        try:
            download_and_filter(url)
            print(f"Successfully downloaded from: {url}")
            sys.exit(0)
        except Exception as e:
            print(f"Failed: {e}")
            continue
    
    print("\nAll URLs failed. You may need to manually download minimum wage data.")
    print("Alternative: Create data/minimum_wage_FR_UK_2000_2024.csv manually with columns:")
    print("  Entity, Code, Year, Minimum wage (or similar column name)")
    sys.exit(1)
