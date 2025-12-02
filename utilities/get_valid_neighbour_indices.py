from utilities.types import Index2D


def get_valid_neighbour_indices(row: int, col: int, max_row: int, max_col: int) -> set[Index2D]:
    """Return neighbouring indices.

    Note: Does not include diagonal neighbours.
    """
    return {
        (max(row - 1, 0), col),
        (row, max(col - 1, 0)),
        (min(row + 1, max_row - 1), col),
        (row, min(col + 1, max_col - 1)),
    }.difference({(row, col)})
