from pathlib import Path
from timeit import default_timer as timer

from rich import box, print
from rich.console import Console
from rich.table import Column, Table

from cli.utils.arguments.day import Day
from cli.utils.command_base import CommandBase
from cli.utils.context import ContextObject
from cli.utils.options.cut_off_time import CutOffTime
from cli.utils.options.force_rerun import ForceRerun
from cli.utils.options.output_file_name import OutputFileName
from cli.utils.options.run_count import RunCount
from cli.utils.part import Part
from cli.utils.profile_results import PartProfileResults, ProfileResults
from utilities.solution_abstract import SolutionAbstract


class ProfileCommand(CommandBase):
    day: Day
    run_count: RunCount
    cut_off_time: CutOffTime
    output_file_name: OutputFileName
    force_rerun: ForceRerun
    solution_dir_path: Path
    solution_instance: SolutionAbstract

    def __init__(
        self,
        context: ContextObject,
        day: Day,
        run_count: RunCount,
        cut_off_time: CutOffTime,
        output_file_name: OutputFileName,
        force_rerun: ForceRerun,
    ):
        super().__init__(context=context)
        self.day = day
        self.run_count = run_count
        self.cut_off_time = cut_off_time
        self.output_file_name = output_file_name
        self.force_rerun = force_rerun
        self.solution_dir_path = self.get_solution_dir_path(self.day)
        self.solution_instance = self.get_solution_instance(self.day, input_file_name="input.txt")

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
