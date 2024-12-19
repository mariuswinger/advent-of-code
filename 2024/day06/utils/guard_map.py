from dataclasses import dataclass

import numpy as np

from day06.utils.guard import Guard, step_guard
from utilities.map_base import Map2DBase


@dataclass
class GuardMap(Map2DBase):
    is_obstacle: np.ndarray

    @classmethod
    def create(cls, map_list: list[list[str]]):
        """Create a Map instance from a list of lists."""
        map_base = Map2DBase.from_list(map_list)
        is_obstacle = np.zeros(map_base.shape, dtype=bool)
        is_obstacle[map_base.values == "#"] = True
        return cls(values=map_base.values, is_obstacle=is_obstacle)

    def move_guard(self, guard: Guard) -> tuple[Guard, bool]:
        """Move guard a step.

        Returns new guard along with a boolean flag indicating if the new guard is valid (not on an obstacle).
        """
        new_guard = step_guard(guard)
        if not self.is_position_inside_map(*new_guard.position):
            raise IndexError
        if self.is_obstacle[new_guard.position]:
            return Guard(position=guard.position, direction=guard.direction.next()), False
        return Guard(position=new_guard.position, direction=guard.direction), True

    def get_potential_obstacles(self, is_visited: np.ndarray) -> np.ndarray:
        """Return array masking potential spots to put a new obstacle."""
        is_potential_obstacle = np.zeros(self.shape, dtype=bool)
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                # skip if obstacle already:
                if self.is_obstacle[row, col]:
                    continue
                # check if neighbours are visited, else skip
                if not is_visited[row, max(col - 1, 0) : min(col + 2, self.shape[1])].any():
                    continue
                is_potential_obstacle[row, col] = True
        return is_potential_obstacle
