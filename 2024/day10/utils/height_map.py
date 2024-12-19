from dataclasses import dataclass

import numpy as np

from day10.utils.dfs import DepthFirstSearch
from utilities.map_base import Map2DBase
from utilities.types import Index2D

type TrailGraph = dict[Index2D, list[Index2D]]


@dataclass
class HeightMap(Map2DBase):
    @classmethod
    def create(cls, map_list: list[list[int]]):
        """Create a Map instance from a list of lists."""
        map_base = Map2DBase.from_list(map_list, dtype=np.dtype(np.int32))
        return cls(values=map_base.values)

    def get_start_indices(self) -> list[Index2D]:
        """Return start indices as list of Index2D type."""
        start_indices = self.get_indices(self.values == 0)
        return [(int(i[0]), int(i[1])) for i in start_indices]

    def get_neighbour_graph(self) -> TrailGraph:
        """Return a dict containing neighbours of each node/key."""
        graph = {}
        for i in range(self.height):
            for j in range(self.width):
                graph[(i, j)] = self._get_neighbour_indices(i, j)
        return graph

    def _get_neighbour_indices(self, i: int, j: int, diff: int = 1) -> list[Index2D]:
        height = self.values[i, j]
        valid_next = []
        if self.is_position_inside_map(i - 1, j):
            if self.values[i - 1, j] - height == diff:
                valid_next.append((i - 1, j))
        if self.is_position_inside_map(i + 1, j):
            if self.values[i + 1, j] - height == diff:
                valid_next.append((i + 1, j))
        if self.is_position_inside_map(i, j - 1):
            if self.values[i, j - 1] - height == diff:
                valid_next.append((i, j - 1))
        if self.is_position_inside_map(i, j + 1):
            if self.values[i, j + 1] - height == diff:
                valid_next.append((i, j + 1))
        return valid_next

    def get_trailhead_score(self, trail_graph: TrailGraph, start_index: Index2D) -> int:
        """Return trailhead score for a given start index.

        The trailhead score is defined as the number of different tops that can be reached
        from the given starting position.
        """
        dfs = DepthFirstSearch(values=self.values, graph=trail_graph)
        dfs.run(start=start_index)
        return dfs.top_count

    def get_trailhead_rating(self, trail_graph: TrailGraph, start_index: Index2D) -> int:
        """Return trailhead score for a given start index.

        The trailhead rating is defined as the number of unique trails starting at the given position.
        """
        dfs = DepthFirstSearch(values=self.values, graph=trail_graph, remember_visited=False)
        dfs.run(start=start_index)
        return dfs.top_count
