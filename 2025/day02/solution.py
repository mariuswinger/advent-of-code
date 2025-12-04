import numpy as np
from day02.utils.id_range import IdNumber, IdRange

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    id_ranges: list[IdRange]

    def _parse_input(self):
        """Parse input from self.raw_data."""
        id_ranges = []
        for ranges in self.raw_data[0].split(","):
            id_ranges.append(IdRange.from_string(ranges))
        self.id_ranges = id_ranges

    def part_a(self) -> int:
        """Solve part a."""
        valid_ids = {}
        for i, id_range in enumerate(self.id_ranges):
            valid_ids[i] = list(filter(lambda x: IdNumber.from_int(x).is_valid_a(), id_range.range))

        valid_id_sum = 0
        for ids in valid_ids.values():
            valid_id_sum += np.sum(ids)

        return int(valid_id_sum)

    def part_b(self) -> int:
        """Solve part b."""
        valid_ids = {}
        for i, id_range in enumerate(self.id_ranges):
            valid_ids[i] = list(filter(lambda x: IdNumber.from_int(x).is_valid_b(), id_range.range))

        valid_id_sum = 0
        for ids in valid_ids.values():
            valid_id_sum += np.sum(ids)

        return int(valid_id_sum)
