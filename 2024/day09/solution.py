import numpy as np
from rich.progress import track

from day09.utils.disk_map import DiskMap
from utilities.rolling_window import rolling_window
from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    disk_map: DiskMap

    def _parse_input(self):
        """Parse input from self.raw_data."""
        # odd ints are file size, even are free space
        values = []
        current_file_id = 0
        for i, x in enumerate(self.raw_data[0]):
            if i % 2 == 0:
                # file
                values += list((current_file_id,) * int(x))
                current_file_id += 1
            else:
                # space
                values += list((-1,) * int(x))
        self.disk_map = DiskMap(np.stack((np.arange(len(values)), values), axis=-1).astype(np.int32))

    def part_a(self) -> int:
        """Solve part a."""
        is_space_to_fill = np.logical_and(
            self.disk_map.values < 0, self.disk_map.indices < self.disk_map.file_block_count
        )
        is_file_block_to_move = np.logical_and(
            self.disk_map.values >= 0, self.disk_map.indices >= self.disk_map.file_block_count
        )
        spaces_to_fill_indices = self.disk_map.indices[is_space_to_fill]
        file_block_indices_to_move = self.disk_map.indices[is_file_block_to_move]
        if not len(spaces_to_fill_indices) == len(file_block_indices_to_move):
            raise ValueError
        for i, j in zip(spaces_to_fill_indices, file_block_indices_to_move[::-1]):
            self.disk_map.switch_value(i, j)
        return self.disk_map.get_checksum()

    def part_b(self) -> int:
        """Solve part b."""
        all_file_ids = np.arange(self.disk_map.file_count)
        for current_file_id in track(all_file_ids[::-1]):
            # not ideal, but ok
            current_file_indices = self.disk_map.get_file_indices(current_file_id)
            current_file_size = current_file_indices.size
            max_free_index = current_file_indices[0]

            suitable_indices = self.disk_map.indices < max_free_index
            free_space_mask = np.logical_and(self.disk_map.values < 0, suitable_indices)
            space_indices = self.disk_map.indices[free_space_mask]
            if space_indices.size == 0:
                continue

            if current_file_size == 1:
                self.disk_map.switch_value(current_file_indices[0], space_indices[0])
                continue

            for i, chunk in enumerate(rolling_window(free_space_mask[:max_free_index], size=current_file_size)):
                if not chunk[0]:
                    continue
                if not chunk.all():
                    continue
                free_space_start_index = i
                new_indices = np.arange(start=free_space_start_index, stop=free_space_start_index + current_file_size)
                self.disk_map.switch_values(current_file_indices, new_indices)
                break

        return self.disk_map.get_checksum()
