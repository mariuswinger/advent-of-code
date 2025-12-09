from day07.utils.tachyon_map import TachyonMap

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    tachyon_map: TachyonMap

    def _parse_input(self):
        """Parse input from self.raw_data."""
        map_list = []
        for row in self.raw_data:
            map_list.append([c for c in row])
        self.tachyon_map = TachyonMap.create(map_list=map_list)

    def part_a(self) -> int:
        """Solve part a."""
        return self.tachyon_map.get_split_count()

    def part_b(self) -> int:
        """Solve part b."""
        return self.tachyon_map.get_timeline_count()
