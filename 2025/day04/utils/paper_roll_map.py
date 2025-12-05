from dataclasses import dataclass
from itertools import product

import numpy as np

from utilities.map_base import Map2DBase
from utilities.types import Index2D


@dataclass
class PaperRollMap(Map2DBase):
    is_paper_roll: np.ndarray

    @classmethod
    def create(cls, map_list: list[list[str]]):
        """Create a Map instance from a list of lists."""
        map_base = Map2DBase.from_list(map_list)
        is_paper_roll = np.zeros(map_base.shape, dtype=bool)
        is_paper_roll[map_base.values == "@"] = True
        return cls(values=map_base.values, is_paper_roll=is_paper_roll)

    def remove_paper_roll(self, row: int, col: int):
        if self.is_paper_roll[row, col]:
            self.values[row, col] = "."
            self.is_paper_roll[row, col] = False

    def get_neighbouring_paper_rolls(self, row: int, col: int) -> set[Index2D]:
        neighbouring_paper_rolls = []
        for i, j in product((row - 1, row, row + 1), (col - 1, col, col + 1)):
            if not self.is_position_inside_map(row=i, col=j):
                continue
            if not self.is_paper_roll[i, j]:
                continue
            neighbouring_paper_rolls.append((i, j))
        return set(neighbouring_paper_rolls).difference({(row, col)})

    def get_accessible_paper_roll_indices(self) -> set[Index2D]:
        accessible_paper_roll_indices = set()
        for row, col in self.get_indices(self.is_paper_roll):
            neighbouring_paper_rolls = self.get_neighbouring_paper_rolls(row, col)
            if len(neighbouring_paper_rolls) < 4:
                accessible_paper_roll_indices.add((row, col))
        return accessible_paper_roll_indices
