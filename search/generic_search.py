from __future__ import annotations
from heapq import heappop, heappush
from collections import deque
from typing import TypeVar, Protocol, Iterable, Sequence, Generic, List, Set, Dict, Optional, Callable, Deque

# Define TypeVar for generic arguments
T = TypeVar("T")

# Define TypeVar C for arguments bound to the comparable class
C = TypeVar("C", bound="Comparable")


# Comparable class to use for object comparison
class Comparable(Protocol):
    def __eq__(self, other) -> bool:
        return self == other

    def __lt__(self: C, other: C) -> bool:
        return self < other and self != other

    def __gt__(self, other: C) -> bool:
        return self > other and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return self > other or self == other


# Generic Node class to represent any current state in the stack
class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: float = 0.0, heuristic: float = 0.0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other: Node):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

    def __gt__(self, other):
        return (self.cost + self.heuristic) > (other.cost + other.heuristic)


# Generic Stack class for depth first searches
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not will be true for an empty container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()  # LIFO by default

    def __repr__(self) -> str:
        return repr(self._container)


# Generic Queue class for breadth first searches
class Queue(Generic[T]):
    def __init__(self):
        self._container: Deque[T] = deque()

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    # The advantage of using a deque: O(1) pops. Lists can efficiently pop from the right, but not from the left.
    def pop(self) -> T:
        return self._container.popleft()

    def __repr__(self):
        return repr(self._container)


# Generic Priority Queue for A*Star searches
class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        heappush(self._container, item)  # in by priority ( priority = lowest f(n). f(n) = g(n) + h(n) )

    def pop(self) -> T:
        return heappop(self._container)  # out by priority

    def __repr__(self) -> str:
        return repr(self._container)


# Traditional linear search (o(n))
def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


# Traditional iterative binary search  (O(log n))
def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:
        # define dynamic mid point for evaluating the middle of the array at any point in time
        mid: int = (low + high) // 2
        if sequence[mid] < key:  # If the middle of the array is less than key: discard the right half.
            low = mid + 1
        elif sequence[mid] > key:  # If the middle of the array is greater than key: discard left half
            high = mid - 1
        else:  # Otherwise, we have found our element so return true
            return True
    return False


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # work back-words from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()  # Reverse the list
    return path


# Depth First Search using Stack class
def dfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node]:
    """
    :param initial: initial node we will be starting from.
    :param goal_test: function that will check if we have found a path to the goal.
    :param successors: function that will return a list of the current nodes children.
    :return: Node if there is a path, otherwise None.
    """
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))  # add the first node with no parents since it is the starting place
    visited: Set[T] = {initial}  # add the initial node into the visited set since we'll start there

    # While there is more to explore, keep exploring
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we've found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where to go next based on what we haven't explored
        for child in successors(current_state):
            if child in visited:  # Check if the current cell has been visited
                continue  # skip children since we've already explored them
            visited.add(child)
            frontier.push(Node(child, current_node))

    return None


# Breadth first search using the Queue class
def bfs(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]) -> Optional[Node]:
    """
    :param initial: initial node we will be starting from.
    :param goal_test: function that will check if we have found a path to the goal.
    :param successors: function that will return a list of the current nodes children.
    :return: Node if there is a path, otherwise None.
    """
    frontier: Queue[T] = Queue()
    frontier.push(Node(initial, None))  # add the first node with no parents since it is the starting place
    visited: Set[T] = {initial}  # add the initial node into the visited set since we'll start there

    # While there is more to explore, keep exploring
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we've found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where to go next based on what we haven't explored
        for child in successors(current_state):
            if child in visited:  # Check if the current cell has been visited
                continue  # skip children since we've already explored them
            visited.add(child)
            frontier.push(Node(child, current_node))

    return None


# A*Star search using PriorityQueue class
def astar(initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]],
          heuristic: Callable[[T], float]) -> Optional[Node[T]]:
    """
    :param heuristic:
    :param initial: initial node we will be starting from.
    :param goal_test: function that will check if we have found a path to the goal.
    :param successors: function that will return a list of the current nodes children.
    :return: Node if there is a path, otherwise None.
    """

    frontier: PriorityQueue[T] = PriorityQueue()
    frontier.push(Node(initial, None, heuristic=heuristic(initial)))  # add the first node with no parents
    visited: Dict[T, float] = {initial: 0.0}  # add initial to the visited set with no cost

    # While there are more nodes to explore, continue exploring
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if we've found the goal, we're done
        if goal_test(current_state):
            return current_node
        # check where we can go next and haven't visited yet
        for child in successors(current_state):
            new_cost: float = current_node.cost + 1  # 1 assumes a grid so one move in any direction
            if child not in visited or visited[child] > new_cost:
                # we have now found a shorter path since it has a lesser cost. update dictionary
                visited[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))

    return None
