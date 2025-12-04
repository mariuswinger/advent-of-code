from day01.utils.rotations import Direction, Rotation

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    rotations: list[Rotation]

    def _parse_input(self):
        """Parse input from self.raw_data."""
        rotations = []
        for x in self.raw_data:
            rotations.append(Rotation(direction=Direction(x[0]), clicks=int(x[1:])))
        self.rotations = rotations

    def part_a(self) -> int:
        """Solve part a."""
        positions = [50]
        for rotation in self.rotations:
            new_position = positions[-1] + rotation.signed_clicks
            positions.append(new_position % 100)
        return get_zeros(positions)

    def part_b(self) -> int:
        """Solve part b."""
        positions = [50]
        wrap_count = 0
        for rotation in self.rotations:
            wrap_count += rotation.revolution_count
            modulated_rotation = rotation.to_modulated()
            if rotation.is_left:
                intermediate_positions = [(positions[-1] - (i + 1)) % 100 for i in range(modulated_rotation.clicks)]
            else:
                intermediate_positions = [(positions[-1] + (i + 1)) % 100 for i in range(modulated_rotation.clicks)]
            wrap_count += get_zeros(intermediate_positions)
            positions.append(intermediate_positions[-1])
        return wrap_count


def get_zeros(positions: list[int]) -> int:
    zero_count = filter(lambda x: x == 0, positions)
    return len(list(zero_count))
