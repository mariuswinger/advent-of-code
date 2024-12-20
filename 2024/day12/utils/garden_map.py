from dataclasses import dataclass

import numpy as np

from utilities.map_base import Map2DBase


@dataclass
class GardenMap(Map2DBase):
    plants: set[str]

    @classmethod
    def create(cls, input: list[str]):
        """Create a GardenMap instance from a list of lists."""
        map_list = []
        plants = set()
        for row in input:
            row_list = [c for c in row]
            plants = plants.union(set(row_list))
            map_list.append(row_list)
        map_base = Map2DBase.from_list(map_list)
        return cls(values=map_base.values, plants=plants)

    def get_plant_mask(self, plant_type: str) -> np.ndarray:
        """Return boolean mask of where the given plant type is planted."""
        return self.values == plant_type
