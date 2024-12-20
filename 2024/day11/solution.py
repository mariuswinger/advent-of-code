from collections import defaultdict

from rich.progress import track

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    start_stones: list[int]

    def _parse_input(self):
        """Parse input from self.raw_data."""
        self.start_stones = list(map(int, self.raw_data[0].split()))

    def part_a(self, blink_count: int = 25) -> int:
        """Solve part a."""
        current_stone_count = {k: 1 for k in self.start_stones}
        for _ in track(range(blink_count)):
            current_stone_count = _get_blinked_stone_count(current_stone_count)
        return sum(current_stone_count.values())

    def part_b(self, blink_count: int = 75) -> int:
        """Solve part b."""
        current_stone_count = {k: 1 for k in self.start_stones}
        for _ in track(range(blink_count)):
            current_stone_count = _get_blinked_stone_count(current_stone_count)
        return sum(current_stone_count.values())


def _blink_stone(stone: int) -> list[int]:
    """Apply blink to stone."""
    if stone == 0:
        return [1]
    stone_str = str(stone)
    digit_count = len(stone_str)
    if digit_count % 2 == 0:
        split_index = digit_count // 2
        return [int(stone_str[:split_index]), int(stone_str[split_index:])]
    return [stone * 2024]


def _get_blinked_stone_count(current_stone_count: dict[int, int]) -> dict[int, int]:
    """Return bucketed collection of stones after one blink."""
    new_stone_count = defaultdict(int)
    for stone, count in current_stone_count.items():
        for new_stone in _blink_stone(stone):
            new_stone_count[new_stone] += count
    return new_stone_count
