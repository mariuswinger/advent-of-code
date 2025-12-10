from dataclasses import dataclass, field
from typing import Self

import numpy as np
from scipy.spatial.distance import pdist, squareform

from utilities.graph import Graph


@dataclass
class JunctionBoxes:
    points: np.ndarray
    distances: np.ndarray
    circuits: list[Graph] = field(default_factory=list)

    @property
    def circuit_lengths(self) -> list[int]:
        return [len(circuit) for circuit in self.circuits]

    @classmethod
    def from_points(cls, points: np.ndarray) -> Self:
        distances = squareform(pdist(points, metric="euclidean"))
        return cls(
            points=points,
            # make everything below upper triangle large for argmin to work
            distances=distances + np.diag([np.inf] * distances.shape[0]) + np.tril([np.inf] * distances.shape[0]),
            circuits=[Graph(vertices={i}) for i in range(points.shape[0])],
        )

    def get_nearest_pair_indices(self) -> tuple[int, int]:
        indices = np.unravel_index(np.argmin(self.distances, axis=None), self.distances.shape)
        return (int(indices[0]), int(indices[1]))

    def connect_boxes(self, box_1_index: int, box_2_index: int) -> Self:
        self.distances[box_1_index, box_2_index] = np.inf

        # check if boxes is in a circuit already:
        box_1_circuit, box_2_circuit = None, None
        for circuit in self.circuits:
            if box_1_index in circuit:
                box_1_circuit = circuit
            if box_2_index in circuit:
                box_2_circuit = circuit

        edge = (box_1_index, box_2_index)
        if box_1_circuit is not None and box_2_circuit is not None:
            # both exist
            if box_1_circuit == box_2_circuit:
                box_1_circuit.add_edge(edge)
                return self
            # both exist, but in different circuits. Need to merge
            box_1_circuit.merge(box_2_circuit)
            box_1_circuit.add_edge(edge)
            self.circuits.remove(box_2_circuit)
            return self

        # exists in only one of
        if box_1_circuit is not None:
            box_1_circuit.add_edge(edge)
            return self

        if box_2_circuit is not None:
            box_2_circuit.add_edge(edge)
            return self

        # None exist: create new
        self.circuits.append(Graph().add_edge(edge))
        return self
