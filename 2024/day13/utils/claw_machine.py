from dataclasses import dataclass
from typing import Any, ClassVar, Self

import numpy as np
import numpy.typing as npt

from day13.utils.augmented_matrix import Augmented2x2Matrix
from day13.utils.linear_diophantine_equation import LinearDiophantineEquation

A_BUTTON_TOKEN_COST = 3
B_BUTTON_TOKEN_COST = 1


@dataclass
class ButtonBase:
    x_step: int
    y_step: int
    token_cost: ClassVar[int]

    def __init_subclass__(cls, /, *, token_cost: int, **kwargs: Any) -> None:
        cls.token_cost = token_cost
        return super().__init_subclass__(**kwargs)


class ButtonA(ButtonBase, token_cost=A_BUTTON_TOKEN_COST):
    pass


class ButtonB(ButtonBase, token_cost=B_BUTTON_TOKEN_COST):
    pass


@dataclass
class XYPosition:
    x: int
    y: int

    @classmethod
    def from_array(cls, arr: npt.NDArray[np.int64]) -> Self:
        """Create XYPosition from numpy array."""
        if arr.shape != (2,):
            raise ValueError("array must be of shape (2,)")
        return cls(x=int(arr[0]), y=int(arr[1]))

    def to_array(self) -> npt.NDArray[np.int64]:
        """Return numpy array of position."""
        return np.array([self.x, self.y])


@dataclass
class ClawMachine:
    a_button: ButtonBase
    b_button: ButtonBase
    prize_position: XYPosition

    @property
    def x_equation(self) -> LinearDiophantineEquation:
        """Get equation for x position."""
        return LinearDiophantineEquation(a=self.a_button.x_step, b=self.b_button.x_step, c=self.prize_position.x)

    @property
    def y_equation(self) -> LinearDiophantineEquation:
        """Get equation for y position."""
        return LinearDiophantineEquation(a=self.a_button.y_step, b=self.b_button.y_step, c=self.prize_position.y)

    def is_solveable(self) -> bool:
        """Return True if prize position can be reached by a combination of A and B button presses."""
        return self.x_equation.is_solveable() and self.y_equation.is_solveable()

    def get_solution(self) -> tuple[int, int]:
        """Return solution to claw machine or raise error if no solution exists."""
        equation_system = Augmented2x2Matrix.from_equations(self.x_equation, self.y_equation)
        reduced_equation_system = equation_system.transpose().reduce_first_column().transpose()
        solution = np.dot(
            reduced_equation_system.right,
            _solve_reduced_system(
                reduced_coefficients=reduced_equation_system.left, prize_position=self.prize_position
            ),
        )
        return int(solution[0]), int(solution[1])

    def is_solution(self, x: int, y: int) -> bool:
        """Check if given input is a solution."""
        return self.x_equation.is_solution(x, y) and self.y_equation.is_solution(x, y)

    def get_token_cost(self, a_button_count: int, b_button_count: int) -> int:
        """Return total token cost for the given number of button presses."""
        return self.a_button.token_cost * a_button_count + self.b_button.token_cost * b_button_count


def _solve_reduced_system(reduced_coefficients: np.ndarray, prize_position: XYPosition) -> npt.NDArray[np.int64]:
    k0, r = np.divmod(prize_position.x, reduced_coefficients[0, 0])
    if r != 0:
        raise ValueError("no integer solution exist")
    k1, r = np.divmod(prize_position.y - reduced_coefficients[1, 0] * k0, reduced_coefficients[1, 1])
    if r != 0:
        raise ValueError("no integer solution exist")
    return np.array([k0, k1])
