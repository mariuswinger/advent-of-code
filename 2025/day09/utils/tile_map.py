from dataclasses import dataclass
from typing import Generator, Self

import numpy as np
from rich.progress import track

from utilities.map_base import Map2DBase
from utilities.types import Index2D


@dataclass
class TileMap(Map2DBase):
    red_tile_indices: list[Index2D]
    is_red_tile: np.ndarray
    is_green_tile: np.ndarray

    @classmethod
    def create_from_red_tile_indices(cls, red_tile_indices: list[Index2D]) -> Self:
        """Create a Map instance from 2d indices."""
        red_tile_indices_array = np.array(red_tile_indices)
        height, width = red_tile_indices_array.max(axis=0) + 2
        map_base = Map2DBase(values=np.zeros((height, width)))

        is_red_tile = np.zeros(map_base.shape, dtype=bool)
        is_red_tile[(red_tile_indices_array[:, 0], red_tile_indices_array[:, 1])] = True

        is_green_tile = np.zeros(map_base.shape, dtype=bool)

        return cls(
            values=map_base.values,
            red_tile_indices=red_tile_indices,
            is_red_tile=is_red_tile,
            is_green_tile=is_green_tile,
        )

    def fill_green_tiles(self):
        # create the boundary
        green_outline = np.zeros(self.shape, dtype=bool)
        red_tile_pairs = list(_iterate_pairs_as_cycle(self.red_tile_indices))
        for i in track(range(len(red_tile_pairs)), description="Adding green border..."):
            current_red_tile, next_red_tile = red_tile_pairs[i]
            vertical_distance, horizontal_distance = np.abs(
                np.diff(np.array([current_red_tile, next_red_tile]), axis=0)[0]
            )
            if vertical_distance == 0:
                current_row = current_red_tile[0]
                start_column = min(current_red_tile[1], next_red_tile[1]) + 1
                green_outline[
                    (
                        np.zeros((horizontal_distance - 1,), dtype=np.intp) + current_row,
                        np.arange(horizontal_distance - 1, dtype=np.intp) + start_column,
                    )
                ] = True
                continue
            if horizontal_distance == 0:
                current_column = current_red_tile[1]
                start_row = min(current_red_tile[0], next_red_tile[0]) + 1
                green_outline[
                    (
                        np.arange(vertical_distance - 1, dtype=np.intp) + start_row,
                        np.zeros((vertical_distance - 1,), dtype=np.intp) + current_column,
                    )
                ] = True
                continue
            raise ValueError("invalid red tiling")

        # fill the interior
        is_red_or_green_tile = self.is_red_tile | green_outline
        row_has_true = np.any(is_red_or_green_tile, axis=1)
        first_true = np.argmax(is_red_or_green_tile, axis=1)
        last_true = is_red_or_green_tile.shape[1] - np.argmax(is_red_or_green_tile[:, ::-1], axis=1) - 1
        cols = np.arange(is_red_or_green_tile.shape[1])
        self.is_green_tile = (cols >= first_true[:, None]) & (cols <= last_true[:, None]) & row_has_true[:, None]


def _iterate_pairs_as_cycle[T](l: list[T]) -> Generator[tuple[T, T]]:
    element_count = len(l)
    index_pairs = ((i, (i + 1) % element_count) for i in range(element_count))
    for current_index, next_index in index_pairs:
        yield l[current_index], l[next_index]
