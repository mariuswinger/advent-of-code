from rich import print

from cli.utils.arguments.day import Day
from cli.utils.command_base import CommandBase
from cli.utils.context import ContextObject
from cli.utils.part import Part


class SolveCommand(CommandBase):
    day: Day
    part: Part
    input_file_name: str

    def __init__(self, context: ContextObject, day: Day, part: Part, input_file_name: str):
        super().__init__(context=context)
        self.day = day
        self.part = part
        self.input_file_name = input_file_name

    def run(self) -> None:
        """Return answer to the requested part with the given input choice."""
        print(f"AoC-{self.year}, day {self.day}, part {self.part}")
        print(f"computing solution with input from '{self.input_file_name}'...")
        solution_instance = self.get_solution_instance(day=self.day, input_file_name=self.input_file_name)
        solution = solution_instance.solve(self.part)
        print(f"solution: {solution}")
