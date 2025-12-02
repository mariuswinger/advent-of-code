from importlib import import_module
from pathlib import Path

from cli.utils.arguments.day import Day
from cli.utils.context import ContextObject
from utilities.solution_abstract import SolutionAbstract


class CommandBase:
    """Base class for AoC CLI commands."""

    _context: ContextObject

    def __init__(self, context: ContextObject) -> None:
        self._context = context

    @property
    def year(self) -> int:
        return self._context.year

    def get_solution_dir_path(self, day: Day) -> Path:
        """Return path to the directory for the queried day."""
        return self._context.year_directory.get_solution_dir_path(day)

    def get_solution_instance(self, day: Day, input_file_name: str) -> SolutionAbstract:
        """Return requested solution class instance."""
        solution_dir_path = self.get_solution_dir_path(day)

        try:
            solution_module = import_module(f"{solution_dir_path.name}.solution")
        except ModuleNotFoundError:
            raise ValueError(f"solution for day {day} does not exist yet") from None
        solution_class = getattr(solution_module, "Solution")

        return solution_class(solution_dir_path / input_file_name)
