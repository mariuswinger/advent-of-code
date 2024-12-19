from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class Map2DBase:
    values: np.ndarray
    _map_size: tuple[int, int] = field(init=False)

    @classmethod
    def from_list(cls, map_list: list[list[Any]], dtype: np.dtype = np.dtype("U1")):
        """Create a MapBase instance from a list of lists."""
        return cls(values=np.array(map_list, dtype=dtype))

    def __post_init__(self) -> None:
        """Set remaining attributes."""
        self._map_size = self.values.shape

    @property
    def shape(self) -> tuple[int, int]:
        """Return size of the map (width, height)."""
        return self._map_size

    @property
    def height(self) -> int:
        """Return number of rows in the map."""
        return self.shape[0]

    @property
    def width(self) -> int:
        """Return number of columns in the map."""
        return self.shape[1]

    def is_position_inside_map(self, row: int, col: int) -> bool:
        """Return True if the given position is inside the bounds of the map."""
        if row < 0 or col < 0 or row >= self.height or col >= self.width:
            return False
        return True

    def get_indices(self, mask: np.ndarray) -> np.ndarray:
        """Return Nx2 array of indices where mask is True."""
        return np.stack(np.where(mask), axis=-1)
