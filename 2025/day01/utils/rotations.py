from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Direction(StrEnum):
    LEFT = "L"
    RIGHT = "R"


@dataclass
class Rotation:
    direction: Direction
    clicks: int

    @property
    def is_left(self) -> bool:
        return self.direction == Direction.LEFT

    @property
    def revolution_count(self) -> int:
        revolution_count, _ = divmod(self.clicks, 100)
        return revolution_count

    @property
    def signed_clicks(self) -> int:
        if self.direction == Direction.LEFT:
            return -self.clicks
        return self.clicks

    def to_modulated(self) -> Rotation:
        return Rotation(direction=self.direction, clicks=(self.clicks % 100))

    def apply(self, current: int) -> int:
        return (current + self.signed_clicks) % 100
