from copy import deepcopy

import numpy as np

from utilities.solution_abstract import SolutionAbstract


class Solution(SolutionAbstract):
    word_matrix: np.ndarray

    def _parse_input(self):
        """Parse input from self.raw_data."""
        matrix = []
        for s in self.raw_data:
            matrix.append([c for c in s])
        self.word_matrix = np.array(matrix, dtype=np.str_)

    def part_a(self) -> int:
        """Solve part a."""
        xmas_count = 0
        xmas_count += _row_count(self.word_matrix)
        xmas_count += _column_count(self.word_matrix)
        # diagonal left->right
        xmas_count += _diagonal_lr_count(self.word_matrix)
        # diagonal right->left
        xmas_count += _diagonal_rl_count(self.word_matrix)
        return xmas_count

    def part_b(self) -> int:
        """Solve part b."""
        count = 0
        for i in range(self.word_matrix.shape[0] - 2):
            for j in range(self.word_matrix.shape[1] - 2):
                submatrix = self.word_matrix[i : i + 3, j : j + 3]
                if submatrix[1, 1] != "A":
                    continue
                if "".join(np.diag(submatrix)) not in {"MAS", "SAM"}:
                    continue
                if "".join(np.diag(np.fliplr(submatrix))) not in {"MAS", "SAM"}:
                    continue
                count += 1
        return count


def _row_count(matrix: np.ndarray) -> int:
    """Count occurences forwards and backwards across rows."""
    count = 0
    for w in matrix:
        count += _substring_count(w, "XMAS")
        count += _substring_count(w, "SAMX")
    return count


def _column_count(matrix: np.ndarray) -> int:
    """Count occurences forwards and backwards across columns."""
    # transpose = columns
    count = 0
    for w in matrix.T:
        count += _substring_count(w, "XMAS")
        count += _substring_count(w, "SAMX")
    return count


def _diagonal_lr_count(matrix: np.ndarray) -> int:
    """Count occurences forwards and backwards diagonally from left to right."""
    count = 0
    for i in range(matrix.shape[0] - 3):
        submatrix = _get_straightened_submatrix(matrix, i)
        count += _column_count(submatrix)
    return count


def _diagonal_rl_count(matrix: np.ndarray) -> int:
    """Count occurences forwards and backwards diagonally from right to left."""
    count = 0
    for i in range(matrix.shape[0] - 3):
        submatrix = _get_straightened_submatrix(np.flip(matrix, axis=1), i)
        count += _column_count(submatrix)
    return count


def _get_straightened_submatrix(matrix: np.ndarray, start_index: int) -> np.ndarray:
    """Return submatrix where rows are shifted.

    Gives the next four rows from current start_index and shifts the rows so that diagonals becomes columns.
    """
    stop_index = start_index + 4
    submatrix = deepcopy(matrix[start_index:stop_index])
    submatrix[1:] = np.roll(submatrix[1:], -1, axis=1)
    submatrix[2:] = np.roll(submatrix[2:], -1, axis=1)
    submatrix[3:] = np.roll(submatrix[3:], -1, axis=1)
    # remove unreachable words
    submatrix = submatrix[:, :-3]
    return submatrix


def _substring_count(arr: np.ndarray, substring: str) -> int:
    """Return number of occurences of substring in arr."""
    return "".join(arr).count(substring)
