from day03.utils.battery_bank import BatteryBank

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    banks: list[BatteryBank]

    def _parse_input(self):
        """Parse input from self.raw_data."""
        banks = []
        for line in self.raw_data:
            banks.append(BatteryBank(joltages=tuple(int(c) for c in line)))
        self.banks = banks

    def part_a(self) -> int:
        """Solve part a."""
        total_joltage = 0
        for bank in self.banks:
            total_joltage += bank.get_largest_joltage()
        return total_joltage

    def part_b(self) -> int:
        """Solve part b."""
        total_joltage = 0
        for bank in self.banks:
            total_joltage += bank.get_largest_joltage(battery_count=12)
        return total_joltage
