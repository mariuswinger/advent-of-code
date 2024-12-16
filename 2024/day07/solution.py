from enum import Enum
from typing import NamedTuple

from rich.progress import track

from utilities.solution_abstract import SolutionAbstract


class Operation(Enum):
    ADD = "+"
    MULTIPLY = "*"
    CONCAT = "||"

    def run(self, a: int, b: int) -> int:
        """Run operation on input."""
        match self:
            case Operation.ADD:
                return a + b
            case Operation.MULTIPLY:
                return a * b
            case Operation.CONCAT:
                return int(str(a) + str(b))


class Equation(NamedTuple):
    result: int
    components: list[int]

    @property
    def component_count(self) -> int:
        return len(self.components)

    def is_possible(self, operations: list[Operation]) -> bool:
        """Recursive function to check if it is possible to obtain result."""
        if self.component_count == 2:
            a, b = self.components[0:2]
            for op in operations:
                if op.run(a, b) == self.result:
                    return True
            return False
        for op in operations:
            if self.reduce(op).is_possible(operations):
                return True
        return False

    def reduce(self, op: Operation) -> "Equation":
        """Reduce equation with given operation."""
        if self.component_count <= 1:
            raise ValueError
        temp = op.run(self.components[0], self.components[1])
        if self.component_count == 2:
            new_components = [temp]
        else:
            new_components = [temp, *self.components[2:]]
        return Equation(result=self.result, components=new_components)


class Solution(SolutionAbstract):
    equations: list[Equation]

    def _parse_input(self):
        """Parse input from self.raw_data."""
        self.equations = []
        for row in self.raw_data:
            res, comp = row.split(":")
            components = [int(x) for x in comp.strip().split(" ")]
            self.equations.append(Equation(result=int(res), components=components))

    def part_a(self) -> int:
        """Solve part a."""
        result = 0
        for eq in track(self.equations):
            if eq.is_possible([Operation.ADD, Operation.MULTIPLY]):
                result += eq.result
        return result

    def part_b(self) -> int:
        """Solve part b."""
        result = 0
        for eq in track(self.equations):
            if eq.is_possible([Operation.ADD, Operation.MULTIPLY, Operation.CONCAT]):
                result += eq.result
        return result
