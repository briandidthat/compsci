from typing import TypeVar, Generic, List, Optional
from .edge import Edge

# Define TypeVar V to represent vertices in the graph
V = TypeVar("V")


class Graph(Generic[V]):
    def __init(self, vertices: List[V] = []) -> None:
        self._vertices = vertices
        self._edges = [[] for _ in vertices]

    @property
    def vertices_count(self) -> int:
        return len(self._vertices)

    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges))

    # This is an undirected graph so we will add edges in both directions
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)
        self._edges[edge.v].append(edge.reversed())

    # add an edge by using vertices index
    def add_edge_by_indices(self, u: int, v: int) -> None:
        edge: Edge = Edge(u, v)
        self.add_edge(edge)

    # add an edge by looking up vertices index first (convenience method)
    def add_edge_by_vertices(self, first: V, second: V) -> None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v)