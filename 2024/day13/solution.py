import re
from itertools import groupby

from day13.utils.claw_machine import ButtonA, ButtonB, ClawMachine, XYPosition
from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    machines_part_a: list[ClawMachine]
    machines_part_b: list[ClawMachine]

    @staticmethod
    def _to_int_tuple(number_string: str) -> tuple[int, int]:
        """Extract numbers from string containing two numbers."""
        numbers = tuple(map(int, re.findall(r"\d+", number_string)))
        if len(numbers) != 2:
            raise ValueError("Expected input string to only contain two numbers")
        return numbers

    def _parse_input(self):
        """Parse input from self.raw_data."""
        machine_data_list = [list(g) for is_machine_data, g in groupby(self.raw_data, key=bool) if is_machine_data]

        # Create machines for part a:
        self.machines_part_a = []
        for machine_data in machine_data_list:
            self.machines_part_a.append(
                ClawMachine(
                    a_button=ButtonA(*self._to_int_tuple(machine_data[0])),
                    b_button=ButtonB(*self._to_int_tuple(machine_data[1])),
                    prize_position=XYPosition(*self._to_int_tuple(machine_data[2])),
                )
            )

        # Create machines for part b with modified prize position:
        self.machines_part_b = []
        for machine in self.machines_part_a:
            self.machines_part_b.append(
                ClawMachine(
                    a_button=machine.a_button,
                    b_button=machine.b_button,
                    prize_position=XYPosition.from_array(machine.prize_position.to_array() + int(1e13)),
                )
            )

    def part_a(
        self,
        max_a_button_press_count: int = 100,
        max_b_button_press_count: int = 100,
    ) -> int:
        """Solve part a."""
        total_token_cost = 0
        for machine in self.machines_part_a:
            if not machine.is_solveable():
                continue
            try:
                solution = machine.get_solution()
            except ValueError:
                continue
            if solution[0] > max_a_button_press_count or solution[1] > max_b_button_press_count:
                continue
            total_token_cost += machine.get_token_cost(*solution)

        return total_token_cost

    def part_b(self) -> int:
        """Solve part b."""
        total_token_cost = 0
        for machine in self.machines_part_b:
            if not machine.is_solveable():
                continue
            try:
                solution = machine.get_solution()
            except ValueError:
                continue
            total_token_cost += machine.get_token_cost(*solution)

        return total_token_cost
