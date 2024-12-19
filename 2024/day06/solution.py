from copy import deepcopy

import numpy as np
from rich.progress import track

from day06.utils.direction import Direction, direction_from_symbol
from day06.utils.guard import Guard
from day06.utils.guard_map import GuardMap
from day06.utils.loop_exception import LoopException
from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    map: GuardMap
    guard_start: Guard

    def _parse_input(self):
        """Parse input from self.raw_data."""
        map_l = []
        direction_symbols = {d.get_symbol() for d in Direction}
        for i, row in enumerate(self.raw_data):
            row_list = [c for c in row]
            direction_symbol_in_row = set(row_list).intersection(direction_symbols)
            if len(direction_symbol_in_row) == 1:
                guard_start_direction = direction_from_symbol(direction_symbol_in_row.pop())
                self.guard_start = Guard(
                    position=(i, row_list.index(guard_start_direction.get_symbol())), direction=guard_start_direction
                )
            map_l.append(row_list)
        self.map = GuardMap.create(map_l)

    def get_guard_path(self) -> dict[Guard, bool]:
        """Return dictionary of guard positions."""
        current_guard = self.guard_start
        guard_path = {current_guard: True}
        while True:
            try:
                new_guard, is_valid = self.map.move_guard(current_guard)
            except IndexError:
                break
            if not is_valid:
                new_guard, is_valid = self.map.move_guard(new_guard)
            if new_guard in guard_path:
                raise LoopException(msg=f"loop detected at {new_guard}")
            guard_path[new_guard] = True
            current_guard = new_guard
        return guard_path

    def part_a(self) -> int:
        """Solve part a."""
        guard_path = self.get_guard_path()

        is_visited = np.zeros(self.map.shape, dtype=bool)
        for guard in guard_path:
            is_visited[guard.position] = True

        return is_visited.sum()

    def part_b(self) -> int:
        """Solve part b."""
        original_guard_path = self.get_guard_path()

        is_visited = np.zeros(self.map.shape, dtype=bool)
        for guard in original_guard_path:
            is_visited[guard.position] = True

        is_potential_obstacle = self.map.get_potential_obstacles(is_visited)
        potential_obstacle_indices = np.stack(np.where(is_potential_obstacle), axis=1)
        original_map = deepcopy(self.map)

        loop_count = 0
        for i, j in track(potential_obstacle_indices):
            self.map = original_map
            new_map = deepcopy(self.map)
            new_map.is_obstacle[i, j] = True
            self.map = new_map
            try:
                self.get_guard_path()
            except LoopException:
                loop_count += 1

        return loop_count
