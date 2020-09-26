from __future__ import annotations
from dataclasses import dataclass
from typing import TypeVar, Generic, List, Tuple
from utils.graph import Edge, Graph

# Define TypeVar V to represent vertices in the graph
V = TypeVar("V")


@dataclass
class WeightedEdge(Edge):
    weight: float

    def reversed(self) -> WeightedEdge:
        return WeightedEdge(self.v, self.u, self.weight)

    # override less than function to compare and find the minimum weighted edge
    def __lt__(self, other: WeightedEdge) -> bool:
        return self.weight < other.weight

    def __str__(self) -> str:
        return f"{self.u} {self.weight} > {self.v}"


class WeightedGraph(Generic[V], Graph[V]):
    def __init__(self, vertices: List[V] = []) -> None:
        self._vertices: List[V] = vertices
        self._edges: List[List[WeightedEdge]] = [[] for _ in vertices]

    def add_edge_by_indices(self, u: int, v: int, weight: float):
        edge: WeightedEdge = WeightedEdge(u, v, weight)
        self.add_edge(edge)  # this is a call to the graph class add edge

    def add_edge_by_vertices(self, first: V, second: V, weight: float) -> None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v, weight)

    def neighbors_for_index_with_weights(self, index: int) -> List[Tuple[V, float]]:
        distance_tuples: List[Tuple[V, float]] = []
        for edge in self.edges_for_index(index):
            distance_tuples.append((self.vertex_at(edge.v), edge.weight))
        return distance_tuples

    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"{self.vertex_at(i)} -> {self.neighbors_for_index_with_weights(i)}\n"
        return desc


WeightedPath = List[WeightedEdge]  # define type alias for the path


def total_weight(wp: WeightedPath):
    return sum([e.weight for e in wp])


def print_weighted_path(wg: WeightedGraph, wp: WeightedPath) -> None:
    for edge in wp:
        print(f"{wg.vertex_at(edge.u)}  {edge.weight}> {wg.vertex_at(edge.v)}")

    print(f"Total Weight: {total_weight(wp)}")
