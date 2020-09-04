from problems.maze import Maze, manhattan_distance
from utils.generic_search import node_to_path, dfs, bfs, astar

if __name__ == "__main__":
    maze = Maze()

    dfs_solution = dfs(maze.start, maze.goal_test, maze.successors)
    bfs_solution = bfs(maze.start, maze.goal_test, maze.successors)

    distance = manhattan_distance(maze.goal)  # distance for astar solution
    astar_solution = astar(maze.start, maze.goal_test, maze.successors, distance)

    if astar_solution is None:
        print("There is no solution to this maze.")
    else:
        # print("Depth First Solution:")
        # path = node_to_path(dfs_solution)
        # maze.mark(path)
        # print(maze)
        # maze.clear(path)
        # print("================================")
        # print("Breadth First Solution:")
        # path = node_to_path(bfs_solution)
        # maze.mark(path)
        # print(maze)
        # maze.clear(path)
        path = node_to_path(astar_solution)
        maze.mark(path)
        print(maze)