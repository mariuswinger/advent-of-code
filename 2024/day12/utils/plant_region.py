from dataclasses import dataclass

import numpy as np

from utilities.direction import Direction
from utilities.map_base import Map2DBase
from utilities.types import Index2D


@dataclass
class PlantRegionMask(Map2DBase):
    plant_type: str
    indices: set[Index2D]

    @classmethod
    def create(cls, indices: set[Index2D], shape: tuple[int, int], plant_type: str):
        """Create a PlantRegionMask instance from indices."""
        index_array = np.array(list(indices))
        region_mask = np.zeros(shape, dtype=bool)
        region_mask[tuple([index_array[:, 0], index_array[:, 1]])] = True
        return cls(values=region_mask, plant_type=plant_type, indices=indices)

    def get_area(self) -> int:
        """Return area of the region."""
        return self.values.sum()

    def get_perimeter(self) -> int:
        """Return perimeter of the region."""
        # extend original map with one and invert self.values
        border_map = Map2DBase(values=~np.pad(self.values, (1,), constant_values=False))
        perimeter = 0
        for i, j in self.indices:
            # i and j are indices in unpadded region, so add 1
            neighbours = border_map.get_neighbour_indices(i + 1, j + 1)
            for neighbour in neighbours:
                perimeter += int(border_map.values[neighbour])
        return perimeter

    def get_side_count(self) -> int:
        """Return the number of sides of the region."""
        # just need to count number of disconnected graphs of each face
        border_map = Map2DBase(values=~np.pad(self.values, (1,), constant_values=False))
        faces = _get_faces(border_map, self.indices)

        side_counts = {Direction.NORTH: 1, Direction.EAST: 1, Direction.SOUTH: 1, Direction.WEST: 1}
        for direction in faces.keys():
            direction_indices = faces[direction]
            if direction_indices.shape[0] == 1:
                continue

            if direction in {Direction.NORTH, Direction.SOUTH}:
                # ordering works for north/south
                sorting_indices = np.lexsort((direction_indices[:, 1], direction_indices[:, 0]))
                sorted_indices = np.array([(direction_indices[i, 0], direction_indices[i, 1]) for i in sorting_indices])
            else:
                sorting_indices = np.lexsort((direction_indices[:, 0], direction_indices[:, 1]))
                sorted_indices = np.array([(direction_indices[i, 1], direction_indices[i, 0]) for i in sorting_indices])

            is_neighbour = np.abs(np.diff(sorted_indices, axis=0)).sum(axis=1) == 1
            # count number of not neighbouring faces:
            side_counts[direction] += np.sum(~is_neighbour)

        side_count = 0
        for direction in faces.keys():
            side_count += side_counts[direction]
        return side_count

    def get_fence_price(self) -> int:
        """Return the price for fencing the region."""
        return self.get_area() * self.get_perimeter()

    def get_bulk_discount_fence_price(self) -> int:
        """Return the price for fencing the region."""
        return self.get_area() * self.get_side_count()


def _get_faces(border_map: Map2DBase, unpadded_indices: set[Index2D]) -> dict[Direction, np.ndarray]:
    faces = {Direction.NORTH: [], Direction.EAST: [], Direction.SOUTH: [], Direction.WEST: []}
    # unpadded indices are offset by 1 to fit border map:
    for i, j in np.array(list(unpadded_indices)) + 1:
        if border_map.values[i - 1, j]:
            faces[Direction.NORTH].append([i, j])
        if border_map.values[i, j + 1]:
            faces[Direction.EAST].append([i, j])
        if border_map.values[i + 1, j]:
            faces[Direction.SOUTH].append([i, j])
        if border_map.values[i, j - 1]:
            faces[Direction.WEST].append([i, j])
    return {
        Direction.NORTH: np.array(faces[Direction.NORTH]),
        Direction.EAST: np.array(faces[Direction.EAST]),
        Direction.SOUTH: np.array(faces[Direction.SOUTH]),
        Direction.WEST: np.array(faces[Direction.WEST]),
    }
