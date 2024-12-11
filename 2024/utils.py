import os
from abc import ABC, abstractmethod
from enum import Enum
from importlib import import_module
from pathlib import Path
from typing import Any, Callable
from rich import print

import numpy as np
from timeit import default_timer as timer
import requests
from bs4 import BeautifulSoup


class Part(str, Enum):
    A = "a"
    B = "b"

    def to_level(self) -> int:
        return 1 if self == Part.A else 2


def is_valid_day(day: int) -> bool:
    """Return True if day is in valid range."""
    return int(day) in range(1, 26)


class SolutionAbstract(ABC):
    _current_day_path: Path
    raw_data: list[str]

    def __init__(self, day: int, use_sample_input: bool):
        input_file_name = "sample_input" if use_sample_input else "input"
        input_file_path = get_day_dir_path(day) / f"{input_file_name}.txt"
        if not input_file_path.exists() and use_sample_input:
            raise ValueError("could not find sample input")
        if not input_file_path.exists() and not use_sample_input:
            request_input_data(day, input_file_path)
        self.raw_data = self._read_input(input_file_path)
        self._parse_input()

    def _read_input(self, input_file_path: Path) -> list[str]:
        with input_file_path.open("r") as file:
            data = [line.strip("\r\n") for line in file.readlines()]
        return data

    @abstractmethod
    def _parse_input(self) -> Any:
        pass

    @abstractmethod
    def part_a(self) -> Any:
        pass

    @abstractmethod
    def part_b(self) -> Any:
        pass


def request_input_data(day: int, input_path: Path) -> None:
    """Download input data from AoC."""
    year = get_year()
    print(f"... downloading input data for AoC-{year} day {day} into '{input_path}'")
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, cookies={"session": os.environ["SESSION_TOKEN"]})
    if response.status_code != 200:
        raise ValueError(f"error downloading input: {response.status_code}")
    with input_path.open("w") as file:
        file.writelines(response.text)


def get_solution_function(day: int, part: Part, /, use_sample_input: bool = False) -> Callable[[], int]:
    """Return requested solution function."""
    solution_module = import_module(f"day{day:0>2}.solution")
    solution_class = getattr(solution_module, "Solution")
    solution_instance = solution_class(day, use_sample_input)
    solution_function = getattr(solution_instance, f"part_{part.value}")

    return solution_function


def submit_solution(day: int, part: Part, answer: int) -> None:
    """Submit solution to AoC and parse response"""
    year = get_year()
    print(f"... submitting {answer} for AoC-{year} day {day} part {part.value}")
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    data = {"level": str(part.to_level()), "answer": str(answer)}
    response = requests.post(url, cookies={"session": os.environ["SESSION_TOKEN"]}, data=data)
    parsed_response = _parse_response(response)
    if "That's the right answer!" in parsed_response:
        print(f"[green]{parsed_response}[/green]")
    elif "You don't seem to be solving the right level." in parsed_response:
        print(f"[yellow]{parsed_response}[/yellow]")
    elif "You gave an answer too recently" in parsed_response:
        print(f"[yellow]{parsed_response}[/yellow]")
    else:
        print(f"[red]{parsed_response}[/red]")


def _parse_response(response: requests.Response) -> str:
    """Parse response from AoC."""
    if response.status_code != 200:
        raise ValueError(f"error submitting solution: {response.status_code}")
    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.main
    if main is None:
        raise ValueError("could not find main tag in response")
    article = main.article
    if article is None:
        raise ValueError("could not find main.article tag in response")
    output = article.p
    if output is None:
        raise ValueError("could not find main.article.p tag in response")
    return output.text


def profile_solution(solution_function: Callable[[], int], runcount: int) -> np.ndarray:
    """Profile the solutions."""
    times = []
    for _ in range(runcount):
        start = timer()
        solution_function()
        end = timer()
        times.append(end - start)
    return np.array(times)


def get_year() -> int:
    """Return the year of the AoC to solve."""
    return int(Path(__file__).resolve().parent.name)


def get_day_dir_path(day: int) -> Path:
    """Return path to the directory for the requested day."""
    return Path(__file__).resolve().parent / f"day{day:0>2}"
