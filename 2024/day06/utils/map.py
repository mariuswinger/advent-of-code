from dataclasses import dataclass

import numpy as np

from day06.utils.guard import Guard, step_guard
from day06.utils.position import Position


@dataclass
class Map:
    _map: np.ndarray
    _map_size: tuple[int, int]
    is_obstacle: np.ndarray

    @classmethod
    def from_list(cls, map_list: list[list[str]]):
        """Create a Map instance from a list of lists."""
        map = np.array(map_list, dtype=np.dtype("U1"))
        map_size = map.shape
        is_obstacle = np.zeros(map.shape, dtype=bool)
        is_obstacle[map == "#"] = True
        return cls(_map=map, _map_size=map_size, is_obstacle=is_obstacle)

    @property
    def map_size(self) -> tuple[int, int]:
        """Return size of the map (width, height)."""
        return self._map_size

    def is_position_inside_map(self, pos: Position) -> bool:
        """Return True if the given position is inside the bounds of the map."""
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= self.map_size[0]:
            return False
        if pos[1] >= self.map_size[1]:
            return False
        return True

    def move_guard(self, guard: Guard) -> tuple[Guard, bool]:
        """Move guard a step.

        Returns new guard along with a boolean flag indicating if the new guard is valid (not on an obstacle).
        """
        new_guard = step_guard(guard)
        if not self.is_position_inside_map(new_guard.position):
            raise IndexError
        if self.is_obstacle[new_guard.position]:
            return Guard(position=guard.position, direction=guard.direction.next()), False
        return Guard(position=new_guard.position, direction=guard.direction), True

    def get_potential_obstacles(self, is_visited: np.ndarray) -> np.ndarray:
        """Return array masking potential spots to put a new obstacle."""
        is_potential_obstacle = np.zeros(self.map_size, dtype=bool)
        for row in range(self.map_size[0]):
            for col in range(self.map_size[1]):
                # skip if obstacle already:
                if self.is_obstacle[row, col]:
                    continue
                # check if neighbours are visited, else skip
                if not is_visited[row, max(col - 1, 0) : min(col + 2, self.map_size[1])].any():
                    continue
                is_potential_obstacle[row, col] = True
        return is_potential_obstacle
