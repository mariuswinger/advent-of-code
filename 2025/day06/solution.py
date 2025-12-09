from itertools import pairwise

import numpy as np
from day06.utils.homework import Problem

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    homework: list[Problem]

    def _parse_input(self):
        """Parse input from self.raw_data."""
        operations = self.raw_data[-1].split()
        numbers_raw_data = np.array([[c for c in row] for row in self.raw_data[:-1]], dtype="<U1")
        delimiters = [-1, *np.where((numbers_raw_data == " ").all(axis=0))[0], numbers_raw_data.shape[-1]]

        problems = []
        for i, (start, end) in enumerate(pairwise(delimiters)):
            problems.append(
                Problem(
                    raw_data=numbers_raw_data[:, start + 1 : end],
                    operation="+" if operations[i] == "+" else "*",
                )
            )
        self.homework = problems

    def part_a(self) -> int:
        """Solve part a."""
        sum = 0
        for problem in self.homework:
            sum += problem.solve()
        return sum

    def part_b(self) -> int:
        """Solve part b."""
        sum = 0
        for problem in self.homework:
            sum += problem.solve(transposed=True)
        return sum
