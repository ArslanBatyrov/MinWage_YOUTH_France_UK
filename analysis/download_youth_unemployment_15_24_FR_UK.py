import csv
import io
import sys
from pathlib import Path
from urllib.request import Request, urlopen


OWID_YOUTH_UNEMPLOYMENT_URL = (
    "https://ourworldindata.org/grapher/unemployment-rate-for-young-people.csv"
)


def download_and_filter(
    url: str = OWID_YOUTH_UNEMPLOYMENT_URL,
    countries=("France", "United Kingdom"),
    start_year: int = 2000,
    end_year: int = 2024,
    output_path: Path | None = None,
) -> Path:
    """
    Download youth unemployment data (ages 15–24) from Our World in Data,
    filter for given countries and year range, and save as a CSV.
    """
    if output_path is None:
        # Output to data/ folder relative to project root
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        output_path = project_root / "data" / "youth_unemployment_15_24_FR_UK_2000_2024.csv"

    print(f"Downloading data from {url} ...")
    # Some servers (including Our World in Data's file host) may return 403
    # to requests without a browser-like User-Agent, so we set one explicitly.
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

    with urlopen(req) as resp:
        raw = resp.read().decode("utf-8")

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
    # Optional: allow a custom output file path via CLI argument
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    try:
        download_and_filter(output_path=out)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


