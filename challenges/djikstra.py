from __future__ import annotations
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass
from utils.weighted_graph import WeightedEdge, WeightedGraph, print_weighted_path, V, WeightedPath
from utils.generic_search import PriorityQueue


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


# takes a dictionary of edges to reach each vertex and returns a list of edges that goes from start to return
def dict_to_path(start: int, end: int, path_dict: Dict[int, WeightedEdge]) -> WeightedPath:
    if len(path_dict) == 0:
        return []

    edge_path: WeightedPath = []
    edge: WeightedEdge = path_dict[end]
    edge_path.append(edge)

    while edge.u != start:
        edge = path_dict[edge.u]
        edge_path.append(edge)

    return list(reversed(edge_path))


if __name__ == "__main__":
    city_graph: WeightedGraph[str] = WeightedGraph(
        ["Seattle", "San Francisco", "Los Angeles", "Riverside", "Phoenix", "Chicago",
         "Boston", "New York", "Atlanta", "Miami", "Dallas", "Houston", "Detroit",
         "Philadelphia", "Washington"])

    city_graph.add_edge_by_vertices("Seattle", "Chicago", 1737)
    city_graph.add_edge_by_vertices("Seattle", "San Francisco", 678)
    city_graph.add_edge_by_vertices("San Francisco", "Riverside", 386)
    city_graph.add_edge_by_vertices("San Francisco", "Los Angeles", 348)
    city_graph.add_edge_by_vertices("Los Angeles", "Riverside", 50)
    city_graph.add_edge_by_vertices("Los Angeles", "Phoenix", 357)
    city_graph.add_edge_by_vertices("Riverside", "Phoenix", 307)
    city_graph.add_edge_by_vertices("Riverside", "Chicago", 1704)
    city_graph.add_edge_by_vertices("Phoenix", "Dallas", 887)
    city_graph.add_edge_by_vertices("Phoenix", "Houston", 1015)
    city_graph.add_edge_by_vertices("Dallas", "Chicago", 805)
    city_graph.add_edge_by_vertices("Dallas", "Atlanta", 721)
    city_graph.add_edge_by_vertices("Dallas", "Houston", 225)
    city_graph.add_edge_by_vertices("Houston", "Atlanta", 702)
    city_graph.add_edge_by_vertices("Houston", "Miami", 968)
    city_graph.add_edge_by_vertices("Atlanta", "Chicago", 588)
    city_graph.add_edge_by_vertices("Atlanta", "Washington", 543)
    city_graph.add_edge_by_vertices("Atlanta", "Houston", 604)
    city_graph.add_edge_by_vertices("Miami", "Washington", 923)
    city_graph.add_edge_by_vertices("Chicago", "Detroit", 238)
    city_graph.add_edge_by_vertices("Detroit", "Boston", 613)
    city_graph.add_edge_by_vertices("Detroit", "Washington", 396)
    city_graph.add_edge_by_vertices("Detroit", "New York", 482)
    city_graph.add_edge_by_vertices("Boston", "New York", 190)
    city_graph.add_edge_by_vertices("New York", "Philadelphia", 81)
    city_graph.add_edge_by_vertices("Philadelphia", "Washington", 123)

    distances, paths = dijkstra(city_graph, "Los Angeles")
    name_distance: Dict[str, Optional[int]] = distance_array_to_vertex_dict(city_graph, distances)
    print("Distances from Los Angeles:")
    for key, val in name_distance.items():
        print(f"{key} : {val}")
    print("")

    print("Shortest path from Los Angeles to New York:")
    path: WeightedPath = dict_to_path(city_graph.index_of("Los Angeles"), city_graph.index_of("New York"), paths)
    print_weighted_path(city_graph, path)
