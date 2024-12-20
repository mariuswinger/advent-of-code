from day12.utils.garden_map import GardenMap
from day12.utils.plant_mask_map import PlantMaskMap
from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    garden_map: GardenMap

    def _parse_input(self):
        """Parse input from self.raw_data."""
        self.garden_map = GardenMap.create(self.raw_data)

    def part_a(self) -> int:
        """Solve part a."""
        total_fence_price = 0
        for plant_type in self.garden_map.plants:
            plant_mask_map = PlantMaskMap.from_garden_map(garden_map=self.garden_map, plant_type=plant_type)
            for region in plant_mask_map.get_plant_regions().values():
                total_fence_price += region.get_fence_price()
        return total_fence_price

    def part_b(self) -> int:
        """Solve part b."""
        total_fence_price = 0
        for plant_type in self.garden_map.plants:
            plant_mask_map = PlantMaskMap.from_garden_map(garden_map=self.garden_map, plant_type=plant_type)
            for region in plant_mask_map.get_plant_regions().values():
                total_fence_price += region.get_bulk_discount_fence_price()
        return total_fence_price
