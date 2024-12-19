from copy import deepcopy

import numpy as np

from utilities.types import Index2D


class DepthFirstSearch:
    values: np.ndarray
    graph: dict[Index2D, list[Index2D]]
    remember_visited: bool
    visited: set[Index2D]
    path: list[Index2D]
    splits: dict[Index2D, list[Index2D]]
    top_count: int

    def __init__(
        self,
        values: np.ndarray,
        graph: dict[Index2D, list[Index2D]],
        remember_visited: bool = True,
    ):
        self.values = values
        self.graph = graph
        self.remember_visited = remember_visited
        self.visited = set()
        self.path = []
        self.splits = {}
        self.top_count = 0

    def _main_loop(self, node: Index2D) -> None:
        if self.remember_visited:
            if node in self.visited:
                return
            self.visited.add(node)

        if node in self.splits:
            self.path = deepcopy(self.splits[node])
        self.path.append(node)

        neighbours = self.graph[node]
        if self.values[node] == 9:
            self.top_count += 1
        if len(neighbours) > 1:
            for x in neighbours:
                self.splits[x] = deepcopy(self.path)
        for neighbour in neighbours:
            self._main_loop(node=neighbour)

    def run(self, start: Index2D) -> None:
        """Run depth first search from the given start."""
        self._main_loop(node=start)
