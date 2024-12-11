from utils import SolutionAbstract
import re
import numpy as np


class Solution(SolutionAbstract):
    memory: str

    def _parse_input(self):
        """Parse input from self.raw_data."""
        self.memory = "".join(self.raw_data)

    def part_a(self) -> int:
        """Solve part a."""
        numbers = _get_instruction_numbers(self.memory)
        return np.sum(np.prod(numbers, axis=1))

    def part_b(self) -> int:
        """Solve part b."""
        enabled = {0: True}
        for match in re.finditer(r"do\(\)", self.memory):
            enabled[match.span()[0]] = True
        for match in re.finditer(r"don\'t\(\)", self.memory):
            enabled[match.span()[0]] = False
        sorted_enabled = dict(sorted(enabled.items()))

        sorted_conditional_indices = list(sorted_enabled.keys())
        sum = 0
        for start, end in zip(sorted_conditional_indices[:-1], sorted_conditional_indices[1:]):
            if not enabled[start]:
                continue
            numbers = _get_instruction_numbers(self.memory[start:end])
            sum += np.sum(np.prod(numbers, axis=1))

        # continue from the last if the last is a do:
        if enabled[sorted_conditional_indices[-1]]:
            numbers = _get_instruction_numbers(self.memory[sorted_conditional_indices[-1] :])
            sum += np.sum(np.prod(numbers, axis=1))
        return sum


def _get_instruction_numbers(memory_segment: str) -> np.ndarray:
    """Return instruction tuples for the given memory segment."""
    valid_instructions = re.findall(r"mul\(\d{1,3},\d{1,3}\)", memory_segment)
    numbers = []
    for instruction in valid_instructions:
        numbers.append(tuple(map(int, instruction[4:-1].split(","))))
    return np.array(numbers)
