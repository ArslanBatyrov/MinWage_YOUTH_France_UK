import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

# Get project root (parent of analysis/)
script_dir = Path(__file__).parent
project_root = script_dir.parent


def plot_time_series(csv_path: Path) -> None:
    """
    Plot France (red) and United Kingdom (blue) youth unemployment time series.
    Interactive plot with hover tooltips showing exact percentages.
    """
    df = pd.read_csv(csv_path)

    france = df[df["Entity"] == "France"]
    uk = df[df["Entity"] == "United Kingdom"]
    col = "Unemployment rate, ages 15-24"

    fig = go.Figure()

    # France in red
    fig.add_trace(
        go.Scatter(
            x=france["Year"],
            y=france[col],
            mode="lines+markers",
            name="France",
            line=dict(color="red", width=2),
            marker=dict(size=6),
            hovertemplate="<b>France</b><br>Year: %{x}<br>Unemployment Rate: %{y:.2f}%<extra></extra>",
        )
    )

    # UK in blue
    fig.add_trace(
        go.Scatter(
            x=uk["Year"],
            y=uk[col],
            mode="lines+markers",
            name="United Kingdom",
            line=dict(color="blue", width=2),
            marker=dict(size=6),
            hovertemplate="<b>United Kingdom</b><br>Year: %{x}<br>Unemployment Rate: %{y:.2f}%<extra></extra>",
        )
    )

    fig.update_layout(
        title="Youth Unemployment Rate (Ages 15–24), France vs UK, 2000–2024",
        xaxis_title="Year",
        yaxis_title="Youth unemployment rate (15–24, %)",
        hovermode="x unified",
        width=1000,
        height=600,
        legend=dict(x=0.02, y=0.98),
        template="plotly_white",
    )

    # Save to outputs folder
    output_file = project_root / "outputs" / "youth_unemployment_plot.html"
    fig.write_html(str(output_file))
    print(f"\nGraph saved to: {output_file.resolve()}")
    print(f"Open this file in your web browser to view the interactive graph.\n")
    
    # Also try to open in browser
    fig.show()


if __name__ == "__main__":
    # Default to data file in project
    default_csv = project_root / "data" / "youth_unemployment_15_24_FR_UK_2000_2024.csv"
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_csv

    if not csv_path.exists():
        raise SystemExit(
            f"CSV file not found at {csv_path.resolve()}. "
            "Make sure the data file exists in the data/ folder."
        )

    plot_time_series(csv_path)

