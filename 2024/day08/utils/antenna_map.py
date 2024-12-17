from dataclasses import dataclass

import numpy as np

from utilities.map_base import Map2DBase


@dataclass
class AntennaMap(Map2DBase):
    def antenna_indices(self, frequency: str) -> np.ndarray:
        """Return indices of the antennas with a given frequency."""
        return np.stack(np.where(self.values == frequency), axis=1)

    def filter_antinodes(self, antinodes: np.ndarray) -> bool:
        """Return True if antinode index is inside map bounds."""
        return self.is_position_inside_map(*antinodes)

    def get_all_antinode_indices(self, antenna_pairs: np.ndarray, n: int = 1) -> np.ndarray:
        antenna_distances = np.subtract.reduce(antenna_pairs, axis=1)

        antenna_pair_count = antenna_pairs.shape[0]
        all_antinode_indices = np.zeros((antenna_pair_count * 2, 2), dtype=np.int32)
        all_antinode_indices[:antenna_pair_count] = antenna_pairs[:, 0] + n * antenna_distances
        all_antinode_indices[antenna_pair_count:] = antenna_pairs[:, 1] - n * antenna_distances

        return all_antinode_indices

    def get_antinode_mask_array(self, frequency: str) -> np.ndarray:
        """Return boolean mask of where the given frequency creates antinodes."""
        all_antenna_indices = self.antenna_indices(frequency)
        antenna_count = all_antenna_indices.shape[0]

        has_antinode = np.zeros(self.shape, dtype=bool)
        for i in range(antenna_count - 1):
            antenna_pairs = np.stack(
                (
                    all_antenna_indices[i + 1 :],
                    np.repeat(all_antenna_indices[i][np.newaxis, :], antenna_count - (i + 1), axis=0),
                ),
                axis=1,
            )

            new_antinode_indices = self.get_all_antinode_indices(antenna_pairs)
            allowed_antinode_indices = np.apply_along_axis(self.filter_antinodes, axis=1, arr=new_antinode_indices)
            allowed_antinodes = new_antinode_indices[allowed_antinode_indices]
            has_antinode[allowed_antinodes[:, 0], allowed_antinodes[:, 1]] = True

        return has_antinode

    def get_resonant_antinode_mask_array(self, frequency: str) -> np.ndarray:
        """Return boolean mask of where the given frequency creates antinodes."""
        all_antenna_indices = self.antenna_indices(frequency)
        antenna_count = all_antenna_indices.shape[0]

        has_antinode = np.zeros(self.shape, dtype=bool)
        for i in range(antenna_count - 1):
            antenna_pairs = np.stack(
                (
                    all_antenna_indices[i + 1 :],
                    np.repeat(all_antenna_indices[i][np.newaxis, :], antenna_count - (i + 1), axis=0),
                ),
                axis=1,
            )

            n = 0
            while True:
                new_antinode_indices = self.get_all_antinode_indices(antenna_pairs, n=n)
                allowed_antinode_indices = np.apply_along_axis(self.filter_antinodes, axis=1, arr=new_antinode_indices)
                if not allowed_antinode_indices.any():
                    break

                allowed_antinodes = new_antinode_indices[allowed_antinode_indices]
                has_antinode[allowed_antinodes[:, 0], allowed_antinodes[:, 1]] = True
                n += 1

        return has_antinode
