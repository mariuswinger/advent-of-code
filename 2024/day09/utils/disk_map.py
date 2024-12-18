from copy import deepcopy
from dataclasses import dataclass

import numpy as np


@dataclass
class DiskMap:
    layout: np.ndarray

    @property
    def file_count(self) -> int:
        """Return number of files on the disk."""
        return self.layout[:, 1].max(axis=0) + 1

    @property
    def indices(self) -> np.ndarray:
        """Return indices of disk."""
        return self.layout[:, 0]

    @property
    def values(self) -> np.ndarray:
        """Return values at disk."""
        return self.layout[:, 1]

    @property
    def file_block_count(self) -> int:
        """Return total index count occupied by files."""
        return (self.layout[:, 1] >= 0).sum()

    def switch_value(self, i: int, j: int) -> None:
        """Switch values at the given indices."""
        i_value = deepcopy(self.values[i])
        self.layout[i, 1] = deepcopy(self.values[j])
        self.layout[j, 1] = i_value

    def switch_values(self, i: np.ndarray, j: np.ndarray) -> None:
        """Switch values at the given array of indices."""
        if i.size != j.size:
            raise ValueError
        i_values = deepcopy(self.values[i])
        self.layout[i, 1] = deepcopy(self.values[j])
        self.layout[j, 1] = i_values

    def get_file_indices(self, file_id: int) -> np.ndarray:
        """Return indices of the file with the given id."""
        return self.indices[self.values == file_id]

    def get_checksum(self) -> int:
        """Return checksum for disk."""
        return np.prod(self.layout[self.values >= 0], axis=1).sum()
