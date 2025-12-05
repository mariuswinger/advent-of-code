import numpy as np
from day05.utils.pantry import IdRange, Pantry

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    ingredient_ids: list[int]
    pantry: Pantry

    def _parse_input(self):
        """Parse input from self.raw_data."""
        data_iterator = (l for l in self.raw_data)

        fresh_ingredient_ranges = []
        for line in data_iterator:
            if line == "":
                break
            start, end = line.split("-")
            fresh_ingredient_ranges.append(IdRange(start=int(start), stop=int(end)))

        self.pantry = Pantry.build_from_ingredient_ranges(fresh_ingredient_ranges)
        self.ingredient_ids = [int(line) for line in data_iterator]

    def part_a(self) -> int:
        """Solve part a."""
        is_fresh = np.zeros(len(self.ingredient_ids), dtype=bool)
        for i, ingredient_id in enumerate(self.ingredient_ids):
            is_fresh[i] = ingredient_id in self.pantry
        return is_fresh.sum()

    def part_b(self) -> int:
        """Solve part b."""
        return len(self.pantry)
