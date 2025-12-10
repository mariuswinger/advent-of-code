from __future__ import annotations

from dataclasses import dataclass, field
from typing import Self

from utilities.types import Index2D


@dataclass
class Graph:
    """Class representing an undirected graph."""

    vertices: set[int] = field(default_factory=set)
    edges: set[Index2D] = field(default_factory=set)

    def __contains__(self, vertex: int) -> bool:
        """Return True if vertex is in graph."""
        return vertex in self.vertices

    def __len__(self) -> int:
        """Return number of vertices."""
        return len(self.vertices)

    def add_vertex(self, vertex: int) -> Self:
        """Add vertex to graph."""
        if vertex in self:
            return self
        self.vertices.add(vertex)
        return self

    def add_vertices(self, *vertices: int) -> Self:
        """Add vertices to graph."""
        for vertex in vertices:
            self.add_vertex(vertex)
        return self

    def has_edge(self, edge: Index2D) -> bool:
        """Return True if edge is in graph."""
        return edge in self.edges

    def add_edge(self, edge: Index2D) -> Self:
        """Add edge to graph."""
        if self.has_edge(edge):
            return self
        self.add_vertices(*edge)
        self.edges.add(edge)
        return self

    def merge(self, graph: Graph) -> Self:
        """Merge two graph objects."""
        self.vertices = {*self.vertices, *graph.vertices}
        self.edges = {*self.edges, *graph.edges}
        return self
