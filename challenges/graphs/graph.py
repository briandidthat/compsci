from typing import TypeVar, Generic, List, Optional
from .edge import Edge

# Define TypeVar V to represent vertices in the graph
V = TypeVar("V")


class Graph(Generic[V]):
    def __init(self, vertices: List[V] = []) -> None:
        self._vertices = vertices
        self._edges = [[] for _ in vertices]

    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges))
