import numpy as np

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    data: np.ndarray

    def _parse_input(self):
        """Parse input from self.raw_data."""
        self.data = np.loadtxt(self.raw_data, dtype=np.int32)

    def part_a(self) -> int:
        """Solve part a."""
        sorted_a = np.sort(self.data[:, 0])
        sorted_b = np.sort(self.data[:, 1])
        differences = np.abs(sorted_a - sorted_b)
        return np.sum(differences)

    def part_b(self) -> int:
        """Solve part b."""
        unique, counts = np.unique(self.data[:, 1], return_counts=True)
        table = dict(zip(unique, counts))
        similarity_score = 0
        for loc_id in self.data[:, 0]:
            if loc_id in table:
                similarity_score += table[loc_id] * loc_id
        return similarity_score
