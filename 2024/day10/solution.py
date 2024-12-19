from day10.utils.height_map import HeightMap
from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    height_map: HeightMap

    def _parse_input(self):
        """Parse input from self.raw_data."""
        map_l = []
        for row in self.raw_data:
            row_l = ["-9" if c == "." else c for c in row]
            map_l.append([int(c) for c in row_l])
        self.height_map = HeightMap.create(map_l)

    def part_a(self) -> int:
        """Solve part a."""
        trail_graph = self.height_map.get_neighbour_graph()

        score = 0
        for start_index in self.height_map.get_start_indices():
            score += self.height_map.get_trailhead_score(
                trail_graph=trail_graph,
                start_index=start_index,
            )
        return score

    def part_b(self) -> int:
        """Solve part b."""
        trail_graph = self.height_map.get_neighbour_graph()

        score = 0
        for start_index in self.height_map.get_start_indices():
            score += self.height_map.get_trailhead_rating(
                trail_graph=trail_graph,
                start_index=start_index,
            )
        return score
