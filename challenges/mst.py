from typing import TypeVar, List, Optional, Set
from utils.generic_search import PriorityQueue
from utils.weighted_graph import WeightedGraph, WeightedPath, V, print_weighted_path


def mst(wg: WeightedGraph[V], start: int = 0) -> Optional[WeightedPath]:
    if start > wg.vertex_count or start < 0:
        return None

    result: WeightedPath = []
    queue: PriorityQueue = PriorityQueue()
    visited: Set[int] = {start}  # mark the start as visited

    def visit(index: int):
        visited.add(index)  # mark as visited
        for edge in wg.edges_for_index(index):
            # add all edges coming from here to the priority queue
            if edge.v not in visited:
                queue.push(edge)

    # visit the first vertex
    visit(start)

    while not queue.empty:
        edge = queue.pop()  # pop off the edge with the highest priority (lowest weight)
        if edge.v in visited:
            continue  # if visited, don't ever revisit this vertex

        result.append(edge)  # this is the current smallest, so add it to the solution
        visit(edge.v)

    return result


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

    result: Optional[WeightedPath] = mst(city_graph)

    if result is None:
        print("No solution!")
    else:
        print("GRAPH:")
        print(city_graph)
        print("=================================================")
        print("MINIMUM SPANNING TREE")
        print_weighted_path(city_graph, result)
