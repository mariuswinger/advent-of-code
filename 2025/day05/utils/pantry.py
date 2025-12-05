from __future__ import annotations

from dataclasses import dataclass, field
from typing import Self


@dataclass
class IdRange:
    """IncInc range."""

    start: int
    stop: int

    def __len__(self) -> int:
        return self.stop + 1 - self.start

    def __contains__(self, number: int) -> bool:
        return number >= self.start and number <= self.stop

    def __le__(self, other: IdRange) -> bool:
        """Return true if self is contained in other."""
        return self.start >= other.start and self.stop <= other.stop

    def intersects(self, other: IdRange) -> bool:
        if self <= other or other <= self:
            return True
        if self.start in other or self.stop in other:
            return True
        return False

    def merge(self, other: IdRange) -> IdRange:
        """Merge two ranges if they overlap."""
        if other <= self:
            return self
        if self <= other:
            return other
        if self.start in other:
            return IdRange(start=other.start, stop=self.stop)
        if self.stop in other:
            return IdRange(start=self.start, stop=other.stop)
        raise ValueError("ranges do not overlap")


@dataclass
class Pantry:
    ingredient_id_ranges: list[IdRange] = field(default_factory=list)

    @classmethod
    def build_from_ingredient_ranges(cls, ingredient_ranges: list[IdRange]) -> Self:
        pantry = cls()
        for ingredient_range in ingredient_ranges:
            pantry.add_ingredient(ingredient_range)
        return pantry

    def add_ingredient(self, ingredient_range: IdRange):
        # new ingredient can overlap several existing. Need to update
        updated_ranges = [ingredient_range]
        for id_range in self.ingredient_id_ranges:
            if not updated_ranges[0].intersects(id_range):
                updated_ranges.append(id_range)
                continue
            updated_ranges[0] = updated_ranges[0].merge(id_range)
        self.ingredient_id_ranges = updated_ranges

    def __len__(self) -> int:
        return sum(map(len, self.ingredient_id_ranges))

    def __contains__(self, ingredient_id: int) -> bool:
        for id_range in self.ingredient_id_ranges:
            if ingredient_id in id_range:
                return True
        return False
