from __future__ import annotations
from typing import TypeVar, List, Optional, Tuple, Dict
from dataclasses import dataclass
from .mst import WeightedPath, WeightedEdge, WeightedGraph, PriorityQueue

V = TypeVar("V")  # define TypeVar V to represent vertices in the graph


@dataclass
class DijkstraNode:
    vertex: int
    distance: float

    def __lt__(self, other: DijkstraNode) -> bool:
        return self.distance < other.distance

    def __eq__(self, other: DijkstraNode) -> bool:
        return self.distance == other.distance


def dijkstra(wg: WeightedGraph[V], root: V) -> Tuple[List[Optional[float]], Dict[int, WeightedEdge]]:
    first: int = wg.index_of(root)  # find index of root
    distances: List[Optional[float]] = [None] * wg.vertex_count  # since distances are unknown, populate with none
    distances[first] = 0  # the root is always 0 away from the root
    paths: Dict[int, WeightedEdge] = {}  # this dict will stores the path we took to each vertex
    queue: PriorityQueue[DijkstraNode] = PriorityQueue()
    queue.push(DijkstraNode(first, 0))  # add the starting node into the priority queue

    while not queue.empty:
        vertex: int = queue.pop().vertex  # explore the next closest vertex
        dist_u: float = distances[vertex]
        # check each edge/vertex from the vertex in question
        for we in wg.edges_for_index(vertex):
            # the old distance to this vertex
            dist_v: float = distances[we.v]

            # store current distance for brevity
            curr_dist = we.weight + dist_u

            # if there is no older distance or we have found a shorter path
            if dist_v is None or dist_v > curr_dist:
                # update distance to this vertex
                distances[we.v] = curr_dist
                paths[we.v] = we
                # push to priority queue to explore
                queue.push(DijkstraNode(we.v, curr_dist))

    return distances, paths


# helper function to access Dijkstra's results
def distance_array_to_vertex_dict(wg: WeightedGraph[V], distances: List[Optional[float]]) -> Dict[V, Optional[float]]:
    distance_dict: Dict[V, Optional[float]] = {}
    for i in range(len(distances)):
        distance_dict[wg.vertex_at(i)] = distances[i]
    return distance_dict


