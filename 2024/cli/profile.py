from pathlib import Path
from timeit import default_timer as timer

import typer
from rich import box, print
from rich.console import Console
from rich.table import Column, Table
from typing_extensions import Annotated

from cli.utils.abstract_command import CommandBase
from cli.utils.day import Day
from cli.utils.part import Part
from cli.utils.profile_results import PartProfileResults, ProfileResults
from utilities.solution_abstract import SolutionAbstract

app = typer.Typer()


class ProfileCommand(CommandBase):
    day: Day
    run_count: int
    cut_off_time: float
    output_file_name: str
    force_rerun: bool
    solution_dir_path: Path
    solution_instance: SolutionAbstract

    def __init__(self, day: Day, run_count: int, cut_off_time: float, output_file_name: str, force_rerun: bool):
        super().__init__()
        self.day = day
        self.run_count = run_count
        self.cut_off_time = cut_off_time
        self.output_file_name = output_file_name
        self.force_rerun = force_rerun
        self.solution_dir_path = self.get_solution_dir_path(self.day)
        self.solution_instance = self.get_solution_instance(self.day, use_test_data=False)

    @property
    def output_file_path(self) -> Path:
        """Return path to output file."""
        return self.solution_dir_path / self.output_file_name

    def run(self) -> None:
        """Profile the solutions for the queried day."""
        has_results = self.output_file_path.exists()
        if not has_results or self.force_rerun:
            print(f"Profiling solution for day {self.day}, part {Part.A} ...")
            part_a_results = self._profile_solution(Part.A)

            print(f"Profiling solution for day {self.day}, part {Part.B} ...")
            part_b_results = self._profile_solution(Part.B)
            results = ProfileResults(day=self.day, a=part_a_results, b=part_b_results)
            self._export_results_to_file(results)
        else:
            print(f"Reading profiling results from '{self.output_file_path}' ...")
            results = ProfileResults.from_file(self.output_file_path)

        self._export_results_to_console(results)

    def _profile_solution(self, part: Part) -> PartProfileResults:
        """Run solution to get profile timings."""
        times = []
        for i in range(self.run_count):
            start = timer()
            self.solution_instance.solve(part)
            end = timer()
            times.append(end - start)

            total_elapsed_time = sum(times)
            if total_elapsed_time >= self.cut_off_time:
                print(
                    f"Stopping profiling due to elapsed time ({total_elapsed_time:.2f}) being larger than allocated total time.\n"
                    f"Currently {self.cut_off_time} seconds are allocated. This can be adjusted by setting '--cut-off-time'.\n"
                )
                return PartProfileResults(part=part, run_count=i + 1, times=times)
        return PartProfileResults(part=part, run_count=self.run_count, times=times)

    def _export_results_to_file(self, results: ProfileResults) -> None:
        """Write profile results to file."""
        print(f"writing results to '{self.output_file_path}' ...")
        self.output_file_path.unlink(missing_ok=True)
        with self.output_file_path.open("w") as file:
            file.write(results.to_json())

    def _export_results_to_console(self, results: ProfileResults) -> None:
        """Print profile results to console."""
        console = Console()
        console.print("")
        table = Table(
            Column("Part", style="cyan"),
            Column("N", justify="right", style="cyan"),
            Column("Average", justify="right", style="yellow"),
            Column("Min", justify="right", style="green"),
            Column("Max", justify="right", style="red"),
            title=f"Profiling results for day {self.day}",
            show_header=True,
            header_style="bold",
            box=box.ROUNDED,
        )
        table.add_row(*results.a.to_table_row())
        table.add_row(*results.b.to_table_row())
        console.print(table)


@app.command()
def profile(
    day: Annotated[int, typer.Argument(min=1, max=25)],
    run_count: Annotated[int, typer.Option(help="number of times to run code")] = 10,
    cut_off_time: Annotated[
        float, typer.Option(help="upper limit in seconds for total time usage on profiling a solution")
    ] = 30,
    output_file_name: Annotated[
        str, typer.Option("--output", "-o", help="file name for output file")
    ] = "profiling.json",
    force_rerun: Annotated[bool, typer.Option("--force-rerun", "-f", help="rerun profiling")] = False,
):
    """Profile the solutions for the queried day."""
    try:
        ProfileCommand(
            day=day,
            run_count=run_count,
            cut_off_time=cut_off_time,
            output_file_name=output_file_name,
            force_rerun=force_rerun,
        ).run()
    except Exception as e:
        print(f"failed to profile solution: {e}")
        raise typer.Exit(1)
