from maze import Maze
from search.generic_search import node_to_path, dfs, bfs

if __name__ == "__main__":
    maze = Maze()

    dfs_solution = dfs(maze.start, maze.goal_test, maze.successors)
    bfs_solution = bfs(maze.start, maze.goal_test, maze.successors)

    if dfs_solution is None:
        print("There is no solution to this maze.")
    else:
        print("Depth First Solution:")
        path = node_to_path(dfs_solution)
        maze.mark(path)
        print(maze)
        maze.clear(path)
        print("================================")
        print("Breadth First Solution:")
        path = node_to_path(bfs_solution)
        maze.mark(path)
        print(maze)
        maze.clear(path)
