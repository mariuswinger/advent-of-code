from typing import Protocol


class SupportsComparison(Protocol):
    def __lt__(self, other, /) -> bool: ...
    def __le__(self, other, /) -> bool: ...
    def __gt__(self, other, /) -> bool: ...
    def __ge__(self, other, /) -> bool: ...


def argmax[T: SupportsComparison](
    t: tuple[T, ...],
    start_index: int = 0,
    end_index: int | None = None,
) -> tuple[T, int]:
    maximum = max(t[start_index:end_index])
    idx = t.index(maximum, start_index)
    return maximum, idx
