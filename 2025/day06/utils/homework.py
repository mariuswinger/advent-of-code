from dataclasses import dataclass
from typing import Literal

import numpy as np


@dataclass
class Problem:
    raw_data: np.ndarray
    operation: Literal["+", "*"]

    def to_integer_array(self, transposed: bool = False) -> np.ndarray:
        integers = ["".join(l) for l in (self.raw_data if not transposed else self.raw_data.T)]
        return np.array(integers, dtype=np.int64)

    def solve(self, transposed: bool = False) -> int:
        integer_array = self.to_integer_array(transposed)
        if self.operation == "+":
            return integer_array.sum()
        return integer_array.prod()
