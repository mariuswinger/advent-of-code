import numpy as np
from day08.utils.junction_boxes import JunctionBoxes

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    points: np.ndarray

    def _parse_input(self):
        """Parse input from self.raw_data."""
        points = []
        for line in self.raw_data:
            points.append(np.array(line.split(","), dtype=np.float64))
        self.points = np.array(points)

    def part_a(self) -> int:
        """Solve part a."""
        CONNECTION_COUNT = 10

        junction_boxes = JunctionBoxes.from_points(self.points)
        for _ in range(CONNECTION_COUNT):
            box_1_index, box_2_index = junction_boxes.get_nearest_pair_indices()
            junction_boxes.connect_boxes(box_1_index, box_2_index)
        circuit_lengths = sorted(junction_boxes.circuit_lengths, reverse=True)
        return int(np.prod(circuit_lengths[:3]))

    def part_b(self) -> int:
        """Solve part b."""
        junction_boxes = JunctionBoxes.from_points(self.points)
        while len(junction_boxes.circuits) > 1:
            box_1_index, box_2_index = junction_boxes.get_nearest_pair_indices()
            junction_boxes.connect_boxes(box_1_index, box_2_index)
            if len(junction_boxes.circuits) == 1:
                return int(junction_boxes.points[box_1_index, 0] * junction_boxes.points[box_2_index, 0])
        return 0
