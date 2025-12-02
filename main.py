import os
import sys
from pathlib import Path

import typer

from cli.cli import cli

app = typer.Typer(help="Advent of Code CLI", pretty_exceptions_show_locals=False)
app.add_typer(cli, name="")

PROJECT_ROOT = Path(__file__).parent


def validate_year_callback(year: int) -> int:
    if not (PROJECT_ROOT / str(year)).exists():
        raise typer.BadParameter(f"selected year '{year}' does not have any solutions")
    return year


@app.callback()
def main(
    ctx: typer.Context,
    year: int = typer.Option(2025, help="Advent of Code year", callback=validate_year_callback),
):
    """Advent of Code CLI"""
    try:
        session_token = os.environ["AOC_SESSION_TOKEN"]
    except KeyError:
        raise ValueError("environment variable 'AOC_SESSION_TOKEN' is not set")
    ctx.obj = {
        "year": year,
        "project_root": PROJECT_ROOT,
        "session_token": session_token,
    }

    # Add the year directory to sys.path so solutions can be imported
    # This is necessary because the solutions are dynamically imported by name (e.g. "day01.solution")
    sys.path.append(str(PROJECT_ROOT / str(year)))


if __name__ == "__main__":
    app()
