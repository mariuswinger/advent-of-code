from copy import deepcopy
from dataclasses import dataclass
from typing import Self

import numpy as np
import numpy.typing as npt

from day13.utils.linear_diophantine_equation import LinearDiophantineEquation

type IntegerMatrix = npt.NDArray[np.int64]


@dataclass
class Augmented2x2Matrix:
    values: IntegerMatrix

    @property
    def left(self) -> IntegerMatrix:
        return self.values[:, :2]

    @property
    def right(self) -> IntegerMatrix:
        return self.values[:, 2:]

    @property
    def first_column(self) -> IntegerMatrix:
        """Return the first column in right matrix."""
        return self.get_column(0)

    def __str__(self) -> str:
        return str(self.values)

    @classmethod
    def create(cls, left_matrix: IntegerMatrix) -> Self:
        """Create new Augmented2x2Matrix object."""
        return cls(values=_combine_matrices(left_matrix, np.eye(2, dtype=np.int64)))

    @classmethod
    def from_equations(cls, equation_1: LinearDiophantineEquation, equation_2: LinearDiophantineEquation) -> Self:
        """Create Augmented2x2Matrix from two linear diophantine equations."""
        return cls.create(
            left_matrix=np.array([[equation_1.a, equation_1.b], [equation_2.a, equation_2.b]], dtype=np.int64)
        )

    def copy(self) -> "Augmented2x2Matrix":
        """Make a copy of self."""
        return Augmented2x2Matrix(deepcopy(self.values))

    def get_column(self, column_index: int) -> IntegerMatrix:
        """Return column."""
        return self.values[:, column_index]

    def get_row(self, row_index: int) -> IntegerMatrix:
        """Return row."""
        return self.values[row_index]

    def transpose(self) -> "Augmented2x2Matrix":
        """Transpose the left side of the augmented matrix."""
        return Augmented2x2Matrix(_combine_matrices(self.left.T, self.right.T)).copy()

    def swap_rows(self) -> "Augmented2x2Matrix":
        """Swap rows."""
        return Augmented2x2Matrix(self._swap_rows(self.values))

    def invert_row_sign(self, row_index: int) -> "Augmented2x2Matrix":
        """Invert the sign of the given row."""
        return Augmented2x2Matrix(self._invert_row_sign(self.values, row_index))

    def subtract_row_multiple_from_row(
        self, subtrahend_index: int, multiple: int, minuend_index: int
    ) -> "Augmented2x2Matrix":
        """Subtract a multiple of a row from the other."""
        return Augmented2x2Matrix(
            self._subtract_row_multiple_from_row(
                self.values, subtrahend_index=subtrahend_index, multiple=multiple, minuend_index=minuend_index
            ),
        )

    def reduce_first_column(self) -> "Augmented2x2Matrix":
        """Return echelon form of matrix."""
        reduced_system = self.copy()
        column = reduced_system.first_column
        while np.count_nonzero(column) != 1:
            subtrahend_index = int(np.argmin(np.abs(column)))
            minuend_index = (subtrahend_index + 1) % 2
            reduced_system = reduced_system.subtract_row_multiple_from_row(
                subtrahend_index=subtrahend_index,
                multiple=np.abs(column[minuend_index] // column[subtrahend_index]),
                minuend_index=minuend_index,
            )
            if subtrahend_index == 1:
                reduced_system = reduced_system.swap_rows()
            column = reduced_system.first_column
        return reduced_system

    @staticmethod
    def _swap_rows(arr: IntegerMatrix) -> IntegerMatrix:
        return deepcopy(arr)[[1, 0]]

    @staticmethod
    def _invert_row_sign(arr: IntegerMatrix, row_index: int) -> IntegerMatrix:
        new_arr = deepcopy(arr)
        new_arr[row_index] = -new_arr[row_index]
        return new_arr

    @staticmethod
    def _subtract_row_multiple_from_row(
        arr: IntegerMatrix, subtrahend_index: int, multiple: int, minuend_index: int
    ) -> IntegerMatrix:
        """Return array where a multiple of row at subtrahend_index is subtracted from row at minuend_index."""
        new_arr = deepcopy(arr)
        new_arr[minuend_index] = new_arr[minuend_index] - multiple * new_arr[subtrahend_index]
        return new_arr


def _combine_matrices(left: IntegerMatrix, right: IntegerMatrix) -> IntegerMatrix:
    """Combine left and right matrix into single matrix along the rows."""
    if not (left.shape[0] == right.shape[0]):
        raise ValueError("matrices must have the same number of rows.")
    return np.hstack((left, right))
