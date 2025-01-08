from dataclasses import dataclass
from math import gcd


@dataclass
class LinearDiophantineEquation:
    """Represents the linear diophantine equation ax + by = c."""

    a: int
    b: int
    c: int

    def __str__(self) -> str:
        return f"{self.a}x + {self.b}y = {self.c}"

    @property
    def gcd(self) -> int:
        """Return greatest common divisor between a and b."""
        return gcd(self.a, self.b)

    @property
    def is_coprime(self) -> bool:
        """Return True if a and b are coprime."""
        return self.gcd == 1

    def is_solveable(self) -> bool:
        """Return True if the equation has a solution."""
        return self.c % self.gcd == 0

    def is_solution(self, x: int, y: int) -> bool:
        """Return True if (x, y) is a solution to the equation."""
        return self.a * x + self.b * y == self.c

    def get_particular_solution(self) -> tuple[int, int]:
        """Return a particular solution to the equation.

        This particular solution satisfies the property that the solution (x, y)
        has the smallest positive x solving the equation.
        """
        if not self.is_solveable():
            raise ValueError
        if not self.is_coprime:
            coprime_equation = LinearDiophantineEquation(
                a=self.a // self.gcd, b=self.b // self.gcd, c=self.c // self.gcd
            )
            return coprime_equation.get_particular_solution()
        # can assume that equation is coprime from here on
        # Then a solution for x can be  found by solving ax ≡ c (mod b)
        x = pow(self.a, -1, self.b) * self.c % self.b
        return (x, (self.c - self.a * x) // self.b)


@dataclass
class SolutionSet:
    equation: LinearDiophantineEquation
    particular_solution: tuple[int, int]

    def __init__(self, equation: LinearDiophantineEquation) -> None:
        if not equation.is_solveable():
            raise ValueError(f"Equation {self.equation} has no solutions")
        self.equation = equation
        self.particular_solution = self.equation.get_particular_solution()

    @property
    def x_solution_offset(self) -> int:
        return self.equation.b // self.equation.gcd

    @property
    def y_solution_offset(self) -> int:
        return -self.equation.a // self.equation.gcd

    def get_solution(self, k: int) -> tuple[int, int]:
        """Return a general solution for a given integer multiple k."""
        return (
            self.particular_solution[0] + k * self.x_solution_offset,
            self.particular_solution[1] + k * self.y_solution_offset,
        )
