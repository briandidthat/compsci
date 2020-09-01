from maze import Maze
from search.generic_search import binary_contains, linear_contains

if __name__ == "__main__":
    # maze = Maze()
    # print(maze)

    print(linear_contains(['anthony', 'george', 'kevin', 'durk', 'brian'], "durk"))  # True
    print(linear_contains(['anthony', 'george', 'kevin', 'durk', 'brian'], "mark"))  # False
    print(binary_contains(["a", "b", "c", "d", "e", "f"], "l"))  # False
    print(binary_contains([1, 2, 3, 4, 5, 6], 4))  # True
