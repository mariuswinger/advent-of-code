from day04.utils.paper_roll_map import PaperRollMap

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    paper_roll_map: PaperRollMap

    def _parse_input(self):
        """Parse input from self.raw_data."""
        map_list = []
        for row in self.raw_data:
            map_list.append([c for c in row])
        self.paper_roll_map = PaperRollMap.create(map_list=map_list)

    def part_a(self) -> int:
        """Solve part a."""
        return len(self.paper_roll_map.get_accessible_paper_roll_indices())

    def part_b(self) -> int:
        """Solve part b."""
        removed_paper_roll_count = 0
        state = self.paper_roll_map
        accessible_paper_roll_indices = state.get_accessible_paper_roll_indices()
        while len(accessible_paper_roll_indices) > 0:
            # update state based on accessible paper rolls
            for row, col in accessible_paper_roll_indices:
                state.remove_paper_roll(row, col)
            removed_paper_roll_count += len(accessible_paper_roll_indices)
            accessible_paper_roll_indices = state.get_accessible_paper_roll_indices()

        return removed_paper_roll_count
