import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NamedTuple, Self

import numpy as np

from cli.utils.day import Day
from cli.utils.part import Part

_prefix = {
    "n": 1e-9,  # nano
    "u": 1e-6,  # micro
    "m": 1e-3,  # mili
}


@dataclass
class PartProfileResults:
    part: Part
    run_count: int
    times: list[float]

    @property
    def np_times(self) -> np.ndarray:
        """Return numpy array of times."""
        return np.array(self.times)

    @property
    def average(self) -> float:
        """Return average run time."""
        return self.np_times.mean()

    @property
    def min(self) -> float:
        """Return min run time."""
        return self.np_times.min()

    @property
    def max(self) -> float:
        """Return max run time."""
        return self.np_times.max()

    def to_json_dict(self) -> dict[str, Any]:
        """Return json dict."""
        return {
            "part": self.part.value,
            "runCount": self.run_count,
            "times": self.times,
        }

    def to_table_row(self) -> tuple[str, str, str, str, str]:
        """Return row for rich.Table."""
        return (
            str(self.part),
            str(self.run_count),
            self.format_time(self.average),
            self.format_time(self.min),
            self.format_time(self.max),
        )

    @staticmethod
    def format_time(seconds: float, precision: int = 3) -> str:
        """Use suitable SI prefix for time."""
        if seconds <= _prefix["n"]:
            nano_seconds = seconds / _prefix["n"]
            return f"{nano_seconds:.{precision}f} ns"
        elif seconds <= _prefix["u"]:
            micro_seconds = seconds / _prefix["u"]
            return f"{micro_seconds:.{precision}f} μs"
        elif seconds <= _prefix["m"] * 100:
            mili_seconds = seconds / _prefix["m"]
            return f"{mili_seconds:.{precision}f} ms"
        else:
            return f"{seconds:.{precision}f} s"


class ProfileResults(NamedTuple):
    day: Day
    a: PartProfileResults
    b: PartProfileResults

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        """Create ProfileResults from file."""
        with file_path.open("r") as file:
            contents = json.loads(file.read())
        try:
            a_dict = contents["a"]
            b_dict = contents["b"]
            return cls(
                day=contents["day"],
                a=PartProfileResults(part=Part(a_dict["part"]), run_count=a_dict["runCount"], times=a_dict["times"]),
                b=PartProfileResults(part=Part(b_dict["part"]), run_count=b_dict["runCount"], times=b_dict["times"]),
            )
        except KeyError:
            raise ValueError("invalid file format!")

    def to_json(self) -> str:
        """Convert ProfileResults to json string."""
        out = {
            "day": self.day,
            "a": self.a.to_json_dict(),
            "b": self.b.to_json_dict(),
        }
        return json.dumps(out)
