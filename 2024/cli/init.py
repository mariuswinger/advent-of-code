import shutil
from pathlib import Path

import requests
import typer
from requests.models import Response
from rich import print
from typing_extensions import Annotated

from cli.utils.abstract_command import CommandBase
from cli.utils.day import Day

app = typer.Typer()


class InitCommand(CommandBase):
    day: Day
    solution_dir_path: Path

    def __init__(self, day: Day):
        super().__init__()
        self.day = day
        self.solution_dir_path = self.get_solution_dir_path(self.day)

    def run(self) -> None:
        """Initialize new directory for solving the queried day."""
        print(f"initializing AoC-{self.year}, day {self.day} ...")
        self._copy_template()

        print(f"downloading input data for AoC-{self.year} day {self.day} ...")
        response = self._post_request()
        if response.status_code != 200:
            raise ValueError(f"unexpected response code: {response.status_code}")

        print(f"writing input data to '{self.solution_dir_path}' ...")
        self._export_input_data(response.text)

    def _copy_template(self) -> None:
        """Copy template files to new directory."""
        self.solution_dir_path.mkdir()
        template_file = self.solution_dir_path.parent / "_template/solution.py"
        shutil.copy(template_file, self.solution_dir_path / "solution.py")

    def _post_request(self) -> Response:
        """Post request for getting input data."""
        url = f"https://adventofcode.com/{self.year}/day/{self.day}/input"
        return requests.get(url, cookies={"session": self.session_token})

    def _export_input_data(self, input_data: str) -> None:
        """Write input data to file."""
        input_file_path = self.solution_dir_path / "input.txt"
        with input_file_path.open("w") as file:
            file.writelines(input_data)


@app.command()
def init(
    day: Annotated[int, typer.Argument(min=1, max=25)],
):
    """Initialize new directory for solving the queried day."""
    try:
        InitCommand(day).run()
    except Exception as e:
        print(f"failed to init: {e}")
        raise typer.Exit(1)
