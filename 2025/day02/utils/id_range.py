from __future__ import annotations

from dataclasses import dataclass
from typing import Self


@dataclass
class IdNumber:
    number: str

    @property
    def has_even_digit_count(self) -> bool:
        return len(self) % 2 == 0

    def to_int(self) -> int:
        return int(self.number)

    def __len__(self) -> int:
        return len(self.number)

    @classmethod
    def from_int(cls, number: int) -> Self:
        return cls(number=str(number))

    def is_valid_a(self, partition_count: int = 2) -> bool:
        if not self.has_even_digit_count and partition_count == 2:
            return False
        partitions = partition_string(self.number, partition_length=len(self) // partition_count)
        return is_partitions_valid(partitions)

    def is_valid_b(self) -> bool:
        for partition_count in range(2, len(self) + 1):
            if len(self) % partition_count != 0:
                continue
            partitions = partition_string(self.number, partition_length=len(self) // partition_count)
            if is_partitions_valid(partitions):
                return True
        return False


@dataclass
class IdRange:
    start: IdNumber
    end: IdNumber

    @property
    def range(self) -> range:
        return range(self.start.to_int(), self.end.to_int() + 1)

    def __str__(self) -> str:
        return f"{self.start.number}-{self.end.number}"

    def __contains__(self, number: IdNumber) -> bool:
        return number.to_int() in self.range

    @classmethod
    def from_string(cls, input: str) -> Self:
        start, end = input.split("-")
        return cls(start=IdNumber(number=start), end=IdNumber(number=end))

    @classmethod
    def from_ints(cls, start: int, end: int) -> Self:
        return cls(start=IdNumber.from_int(start), end=IdNumber.from_int(end))


def partition_string(string: str, partition_length: int) -> list[str]:
    # print(f"partition_string({string}, {partitions})")
    str_length = len(string)
    if str_length % partition_length != 0:
        return []
    if str_length == 2:
        return [string[0], string[1]]
    return [string[0 + i : partition_length + i] for i in range(0, str_length, partition_length)]


def is_partitions_valid(partitions: list[str]) -> bool:
    if len(partitions) <= 1:
        return False
    return len(set(partitions)) == 1
