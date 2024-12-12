from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from cli.utils.part import Part


class SolutionAbstract(ABC):
    """Abstract base class for each day of AoC."""

    raw_data: list[str]

    def __init__(self, input_file_path: Path):
        with input_file_path.open("r") as file:
            self.raw_data = [line.strip("\r\n") for line in file.readlines()]
        self._parse_input()

    @abstractmethod
    def _parse_input(self) -> Any:
        pass

    @abstractmethod
    def part_a(self) -> Any:
        pass

    @abstractmethod
    def part_b(self) -> Any:
        pass

    def solve(self, part: Part) -> int:
        """Return solution for the given part."""
        if part == Part.A:
            return self.part_a()
        else:
            return self.part_b()
