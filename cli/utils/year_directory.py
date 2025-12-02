from dataclasses import dataclass
from pathlib import Path

from cli.utils.arguments.day import Day


@dataclass
class YearDirectory:
    """Class for handling the year directory."""

    root: Path

    def get_solution_dir_path(self, day: Day) -> Path:
        """Return path to the directory for the queried day."""
        return self.root / f"day{day:0>2}"
