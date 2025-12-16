from day10.utils.machine import Button, Machine, State
from scipy.optimize import linprog

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    machines: list[Machine]

    def _parse_input(self):
        """Parse input from self.raw_data."""
        machines = []
        for row in self.raw_data:
            components = row.split(" ")
            target_indicator_lights = State(
                tuple(character == "#" for character in components[0].strip("[").strip("]"))
            )
            buttons = [
                Button.from_input(text=button_config, light_count=len(target_indicator_lights))
                for button_config in components[1:-1]
            ]
            joltages = tuple(int(x) for x in components[-1].strip("{").strip("}").split(","))
            machines.append(
                Machine(
                    target_indicator_lights=target_indicator_lights,
                    buttons=buttons,
                    joltages=joltages,
                )
            )
        self.machines = machines

    def part_a(self) -> int:
        """Solve part a."""
        total_button_presses = 0
        for machine in self.machines:
            distances = machine.get_distances()
            total_button_presses += distances[machine.target_indicator_lights]

        return int(total_button_presses)

    def part_b(self) -> int:
        """Solve part b."""
        total_button_presses = 0
        for machine in self.machines:
            minimizer = [1] * len(machine.buttons)
            button_matrix = machine.get_button_matrix()
            joltages_to_get = list(machine.joltages)
            solution = linprog(c=minimizer, A_eq=button_matrix, b_eq=joltages_to_get, integrality=1)
            total_button_presses += int(solution.x.sum())

        return total_button_presses
