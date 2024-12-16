from enum import Enum


class Direction(int, Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def get_symbol(self) -> str:
        """Return symbol used to represent the direction."""
        match self:
            case Direction.NORTH:
                return "^"
            case Direction.EAST:
                return ">"
            case Direction.SOUTH:
                return "v"
            case Direction.WEST:
                return "<"

    def next(self) -> "Direction":
        """Return next direction (rotated 90 degrees)."""
        match self:
            case Direction.NORTH:
                return Direction.EAST
            case Direction.EAST:
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.WEST
            case Direction.WEST:
                return Direction.NORTH


def direction_from_symbol(symbol: str) -> Direction:
    """Return direction from symbol."""
    match symbol:
        case "^":
            return Direction.NORTH
        case ">":
            return Direction.EAST
        case "v":
            return Direction.SOUTH
        case "<":
            return Direction.WEST
        case _:
            raise ValueError
