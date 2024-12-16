from typing import NamedTuple

from day06.utils.direction import Direction
from day06.utils.position import Position


class Guard(NamedTuple):
    position: Position
    direction: Direction


def step_guard(guard: Guard) -> Guard:
    """Make guard take a step in the currently facing direction."""
    match guard.direction:
        case Direction.NORTH:
            return Guard(position=(guard.position[0] - 1, guard.position[1]), direction=Direction.NORTH)
        case Direction.EAST:
            return Guard(position=(guard.position[0], guard.position[1] + 1), direction=Direction.EAST)
        case Direction.SOUTH:
            return Guard(position=(guard.position[0] + 1, guard.position[1]), direction=Direction.SOUTH)
        case Direction.WEST:
            return Guard(position=(guard.position[0], guard.position[1] - 1), direction=Direction.WEST)
