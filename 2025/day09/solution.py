import numpy as np
from day09.utils.tile_map import TileMap
from rich.progress import track

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    tile_map: TileMap

    def _parse_input(self):
        """Parse input from self.raw_data."""
        red_tile_indices = []
        for line in self.raw_data:
            red_tile_indices.append(tuple(map(int, line.split(",")))[::-1])

        self.tile_map = TileMap.create_from_red_tile_indices(red_tile_indices)

    def part_a(self) -> int:
        """Solve part a."""
        red_tile_indices = np.array(self.tile_map.red_tile_indices)

        biggest_area = 0
        for i in track(range(red_tile_indices.shape[0] - 1)):
            point = red_tile_indices[i]
            areas_for_point = np.prod(np.abs(red_tile_indices[i + 1 :] - point) + 1, axis=1)
            point_biggest_area = areas_for_point.max()
            if point_biggest_area > biggest_area:
                biggest_area = point_biggest_area
        return biggest_area

    def part_b(self) -> int:
        """Solve part b."""
        self.tile_map.fill_green_tiles()

        biggest_area = 0
        for i in track(range(len(self.tile_map.red_tile_indices))):
            corner_1 = self.tile_map.red_tile_indices[i]
            for corner_2 in self.tile_map.red_tile_indices[i + 1 :]:
                min_row_index, max_row_index = min(corner_1[0], corner_2[0]), max(corner_1[0], corner_2[0])
                min_col_index, max_col_index = min(corner_1[1], corner_2[1]), max(corner_1[1], corner_2[1])
                line_1_is_green = self.tile_map.is_green_tile[min_row_index, min_col_index:max_col_index]
                if np.any(~line_1_is_green):
                    continue
                line_2_is_green = self.tile_map.is_green_tile[max_row_index, min_col_index:max_col_index]
                if np.any(~line_2_is_green):
                    continue
                line_3_is_green = self.tile_map.is_green_tile[min_row_index:max_row_index, min_col_index]
                if np.any(~line_3_is_green):
                    continue
                line_4_is_green = self.tile_map.is_green_tile[min_row_index:max_row_index, max_col_index]
                if np.any(~line_4_is_green):
                    continue

                area = np.prod(np.abs(np.diff(np.array([corner_1, corner_2]), axis=0)[0]) + 1)
                if area > biggest_area:
                    biggest_area = area

        return biggest_area
