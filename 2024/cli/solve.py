import typer
from rich import print
from typing_extensions import Annotated

from cli.utils.abstract_command import CommandBase
from cli.utils.day import Day
from cli.utils.part import Part, PartArg
from utilities.solution_abstract import SolutionAbstract

app = typer.Typer()


class SolveCommand(CommandBase):
    day: Day
    part: Part
    solution_instance: SolutionAbstract

    def __init__(self, day: Day, part: Part, use_test_data: bool):
        super().__init__()
        self.day = day
        self.part = part
        self.solution_instance = self.get_solution_instance(self.day, use_test_data=use_test_data)

    def run(self) -> None:
        """Return answer to the requested part with the given input choice."""
        print(f"AoC-{self.year}, day {self.day}, part {self.part}")
        print("computing solution ...")
        solution = self.solution_instance.solve(self.part)
        print(f"solution: {solution}")


@app.command()
def solve(
    day: Day,
    part: PartArg,
    use_test_data: Annotated[bool, typer.Option("--test", help="use test data")] = False,
):
    """Return answer to the requested part with the given input choice."""
    try:
        SolveCommand(day=day, part=part.to_part(), use_test_data=use_test_data).run()
    except Exception as e:
        print(f"failed to solve: {e}")
        raise typer.Exit(1)
