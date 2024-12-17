import numpy as np

from day08.utils.antenna_map import AntennaMap
from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    frequencies: set[str]
    map: AntennaMap

    def _parse_input(self):
        """Parse input from self.raw_data."""
        self.frequencies = set()
        map_l = []
        for row in self.raw_data:
            self.frequencies = self.frequencies.union(set(row).difference({"."}))
            map_l.append([c for c in row])
        self.map = AntennaMap.from_list(map_l)

    def part_a(self) -> int:
        """Solve part a."""
        # note: all antenna pairs create antinodes!
        has_antinode = np.zeros((self.map.shape), dtype=bool)
        for frequency in list(self.frequencies):
            has_antinode += self.map.get_antinode_mask_array(frequency)
        return has_antinode.sum()

    def part_b(self) -> int:
        """Solve part b."""
        has_antinode = np.zeros((self.map.shape), dtype=bool)
        for frequency in list(self.frequencies):
            has_antinode += self.map.get_resonant_antinode_mask_array(frequency)
        return has_antinode.sum()
