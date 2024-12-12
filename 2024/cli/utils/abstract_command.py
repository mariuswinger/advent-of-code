import os
import re
from importlib import import_module
from pathlib import Path

from cli.utils.day import Day
from utilities.solution_abstract import SolutionAbstract


class CommandBase:
    """Base class for AoC CLI commands."""

    year: int
    root_path: Path
    session_token: str

    def __init__(self):
        try:
            os.environ["AOC_YEAR"]
        except KeyError:
            pass
        file_path = Path(__file__).resolve()
        hits = re.search(r"advent-of-code\/(\d*)\/", str(file_path))
        if hits is None:
            raise ValueError(f"unable to find year from path '{file_path}'. Please set environment variable 'AOC_YEAR'")
        self.year = int(hits.group(1))

        for parent in Path(__file__).resolve().parents:
            if parent.name == str(self.year):
                self.root_path = parent
                # return parent / f"day{day:0>2}"
        if not hasattr(self, "root_path"):
            raise ValueError("invalid directory structure")

        try:
            self.session_token = os.environ["AOC_SESSION_TOKEN"]
        except KeyError:
            raise ValueError("environment variable 'AOC_SESSION_TOKEN' is not set")

    def get_solution_dir_path(self, day: Day) -> Path:
        """Return path to the directory for the queried day."""
        return self.root_path / f"day{day:0>2}"

    def get_solution_instance(self, day: Day, use_test_data: bool) -> SolutionAbstract:
        """Return requested solution class instance."""
        solution_dir_path = self.get_solution_dir_path(day)

        try:
            solution_module = import_module(f"{solution_dir_path.name}.solution")
        except ModuleNotFoundError:
            raise ValueError(f"solution for day {day} does not exist yet") from None
        solution_class = getattr(solution_module, "Solution")

        input_file_path = solution_dir_path / f"{"sample_input" if use_test_data else "input"}.txt"
        if not input_file_path.exists():
            raise ValueError("could not find input file")

        return solution_class(input_file_path=input_file_path)
