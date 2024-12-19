import typer
from rich import print
from typing_extensions import Annotated

from cli.utils.abstract_command import CommandBase
from cli.utils.day import Day
from cli.utils.part import Part, PartArg

app = typer.Typer()


class SolveCommand(CommandBase):
    day: Day
    part: Part
    input_file_name: str

    def __init__(self, day: Day, part: Part, input_file_name: str):
        super().__init__()
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


@app.command()
def solve(
    day: Day,
    part: PartArg,
    input_file_name: Annotated[
        str, typer.Option("--input-file", "-i", help="filename of file to read input data from")
    ] = "input.txt",
):
    """Return answer to the requested part with the given input choice."""
    try:
        SolveCommand(day=day, part=part.to_part(), input_file_name=input_file_name).run()
    except Exception as e:
        print(f"failed to solve: {e}")
        raise typer.Exit(1)
