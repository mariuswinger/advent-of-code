from collections import defaultdict
from dataclasses import dataclass

import numpy as np

from utilities.map_base import Map2DBase
from utilities.types import Index2D


@dataclass
class TachyonMap(Map2DBase):
    is_splitter: np.ndarray
    start: Index2D

    @classmethod
    def create(cls, map_list: list[list[str]]):
        """Create a Map instance from a list of lists."""
        map_base = Map2DBase.from_list(map_list)

        is_splitter = np.zeros(map_base.shape, dtype=bool)
        is_splitter[map_base.values == "^"] = True

        start_index = np.where(map_base.values == "S")
        return cls(values=map_base.values, is_splitter=is_splitter, start=(start_index[0][0], start_index[1][0]))

    def get_split_count(self) -> int:
        current_row_beam = [self.start]
        split_count = 0
        for _ in range(self.height - 1):
            next_row_beam = set()
            for beam in current_row_beam:
                if self.is_splitter[(beam[0] + 1, beam[1])]:
                    split_count += 1
                    next_row_beam.add((beam[0] + 1, beam[1] - 1))
                    next_row_beam.add((beam[0] + 1, beam[1] + 1))
                else:
                    next_row_beam.add((beam[0] + 1, beam[1]))
            current_row_beam = list(next_row_beam)
        return split_count

    def get_children(self, current_position: Index2D) -> tuple[Index2D, Index2D] | None:
        try:
            # relative index from current position height
            splitter_depth = np.where(self.is_splitter[current_position[0] + 1 :, current_position[1]])[0][0]
        except IndexError:
            return None
        return (
            (splitter_depth + 1 + current_position[0], current_position[1] - 1),
            (splitter_depth + 1 + current_position[0], current_position[1] + 1),
        )

    def get_timeline_count(self) -> int:
        current_row_beam_count = {self.start: 1}
        for _ in range(self.height - 1):
            next_row_beam_count = defaultdict(int)
            for beam, beam_count in current_row_beam_count.items():
                current_y, current_x = beam

                next_row_beam = (current_y + 1, current_x)
                if not self.is_splitter[next_row_beam]:
                    next_row_beam_count[next_row_beam] += beam_count
                    continue

                next_row_beam_count[(current_y + 1, current_x - 1)] += beam_count
                next_row_beam_count[(current_y + 1, current_x + 1)] += beam_count

            current_row_beam_count = next_row_beam_count
        return sum(current_row_beam_count.values())
