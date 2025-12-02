import shutil
from dataclasses import dataclass
from pathlib import Path

import requests
from requests.models import Response
from rich import print

from cli.utils.arguments.day import Day
from cli.utils.command_base import CommandBase
from cli.utils.context import ContextObject


@dataclass
class InitCommand(CommandBase):
    day: Day

    @property
    def solution_dir_path(self) -> Path:
        """Return path to solutions."""
        return self.get_solution_dir_path(self.day)

    def __init__(self, context: ContextObject, day: Day):
        super().__init__(context=context)
        self.day = day

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
        shutil.copy(self._context.template_file, self.solution_dir_path / "solution.py")

    def _post_request(self) -> Response:
        """Post request for getting input data."""
        url = f"https://adventofcode.com/{self.year}/day/{self.day}/input"
        return requests.get(url, cookies={"session": self._context.session_token})

    def _export_input_data(self, input_data: str) -> None:
        """Write input data to file."""
        input_file_path = self.solution_dir_path / "input.txt"
        with input_file_path.open("w") as file:
            file.writelines(input_data)
