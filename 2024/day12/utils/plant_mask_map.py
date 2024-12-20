from dataclasses import dataclass

import numpy as np

from day12.utils.dfs import run_dfs
from day12.utils.garden_map import GardenMap
from day12.utils.plant_region import PlantRegionMask
from utilities.map_base import Map2DBase
from utilities.types import Index2D


@dataclass
class PlantMaskMap(Map2DBase):
    plant_type: str

    @classmethod
    def create(cls, plant_mask: np.ndarray, plant_type: str):
        """Create a PlantMap instance from boolean mask."""
        return cls(values=plant_mask, plant_type=plant_type)

    @classmethod
    def from_garden_map(cls, garden_map: GardenMap, plant_type: str):
        """Create a PlantMap instance from GardenMap."""
        return cls(values=garden_map.get_plant_mask(plant_type), plant_type=plant_type)

    def get_plant_neighbours(self, row: int, col: int) -> set[Index2D]:
        """Return neighbours that have the same plant type."""
        return {(i, j) for i, j in self.get_neighbour_indices(row, col) if self.values[i, j]}

    def get_plant_neighbour_graph(self) -> dict[Index2D, set[Index2D]]:
        """Return graph of neighbouring indices of the same plant type.

        Note: Graph may be disconnected.
        """
        plant_neighbour_graph = {}
        for ind in self.get_indices(self.values):
            i, j = map(int, ind)
            if self.values[i, j]:
                plant_neighbour_graph[(i, j)] = self.get_plant_neighbours(i, j)
        return plant_neighbour_graph

    def get_plant_regions(self) -> dict[int, PlantRegionMask]:
        """Return dictionary of plant regions."""
        plant_neighbour_graph = self.get_plant_neighbour_graph()
        plant_regions = {}
        region_count = 0

        plant_index_set = set(plant_neighbour_graph.keys())
        while plant_index_set:
            current_region = run_dfs(start=_get_first(plant_index_set), plant_graph=plant_neighbour_graph)
            plant_regions[region_count] = PlantRegionMask.create(
                indices=current_region, shape=(self.height, self.width), plant_type=self.plant_type
            )
            region_count += 1

            # update index set
            plant_index_set = plant_index_set.difference(current_region)
        return plant_regions


def _get_first(s: set[Index2D]) -> Index2D:
    """Return first element in set."""
    for start in s:
        return start
    raise IndexError
