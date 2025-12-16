from collections import defaultdict
from dataclasses import dataclass
from typing import Self

import numpy as np


@dataclass(frozen=True)
class State:
    indicators: tuple[bool, ...]

    def __len__(self) -> int:
        return len(self.indicators)

    def __add__(self, other: "State") -> "State":
        if len(self) != len(other):
            raise TypeError("incompatible lengths")
        return State(tuple(a ^ b for a, b in zip(self.indicators, other.indicators)))

    @classmethod
    def default(cls, length: int) -> Self:
        return cls(indicators=(False,) * length)


@dataclass
class Button:
    effect: State

    @classmethod
    def from_input(cls, text: str, light_count: int) -> Self:
        indices = list(map(int, text.strip("(").strip(")").split(",")))
        return cls(effect=State(indicators=tuple([i in indices for i in range(light_count)])))

    def __len__(self) -> int:
        return len(self.effect)

    def __add__(self, other: "Button") -> "Button":
        return Button(effect=other.effect + self.effect)


@dataclass
class Machine:
    target_indicator_lights: State
    buttons: list[Button]
    joltages: tuple[int, ...]

    def get_distances(self) -> dict[State, float]:
        starting_state = State.default(len(self.target_indicator_lights))
        distances: dict[State, float] = defaultdict(lambda: float("inf"))
        distances[starting_state] = 0
        queue = [starting_state]
        while queue:
            current_node = queue.pop(0)
            for next_node in (current_node + button.effect for button in self.buttons):
                distance = distances[current_node] + 1
                if distance < distances[next_node]:
                    distances[next_node] = distance
                    queue.append(next_node)
        return distances

    def get_button_matrix(self) -> np.ndarray:
        return np.array([[int(x) for x in button.effect.indicators] for button in self.buttons]).T
