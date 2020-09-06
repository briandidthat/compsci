import random
from enum import Enum
from math import sqrt
from typing import NamedTuple, List, Callable, Optional


class Cell(str, Enum):
    """
    Cell: Will represent the current state of any cell in grid in string format.
    """
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    """
    Maze Location: Will keep track of any location on the maze (maze._grid[ml.row][ml.col])
    """
    row: int
    col: int


class Maze:
    """
    Maze: Will internally keep track of a grid, (matrix) representing it's state. It will be randomly filled
    with blocked cells when created. Sparseness will be 0.2 by default representing a 20% blocked state on the
    grid.
    """

    def __init__(self, rows=10, columns=10, sparseness=0.2, start=MazeLocation(0, 0), goal=MazeLocation(9, 9)):
        # initialize instant variables
        self._rows = rows
        self._columns = columns
        self.start = start
        self.goal = goal
        # Create 2d Matrix to represent the grid
        self._grid = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]
        self._randomly_fill(rows, columns, sparseness)
        # fill the start and goal locations
        self._grid[start.row][start.col] = Cell.START
        self._grid[goal.row][goal.col] = Cell.GOAL

    # populate the grid with blocked cells
    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    # override __str__ method and print maze
    def __str__(self):
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output

    # test whether we have reached our goal MazeLocation
    def goal_test(self, ml: MazeLocation):
        return ml == self.goal

    # find next possible location using successors. will look above, below, left, right
    def successors(self, ml: MazeLocation):
        locations = []
        # check the row above
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.col] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.col))
        # check the row below
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.col] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.col))
        # check the column to the left
        if ml.col - 1 >= 0 and self._grid[ml.row][ml.col - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.col - 1))
        # check the column to the right
        if ml.col + 1 < self._columns and self._grid[ml.row][ml.col + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.col + 1))

        return locations

    # mark up the grid with * where there is a path to the goal
    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.col] = Cell.PATH
        self._grid[self.start.row][self.start.col] = Cell.START
        self._grid[self.goal.row][self.goal.col] = Cell.GOAL

    # clear the grid
    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.col] = Cell.EMPTY
        self._grid[self.start.row][self.start.col] = Cell.START
        self._grid[self.goal.row][self.goal.col] = Cell.GOAL


# calculate the euclidean distance (as the crow flies so will be a straight line from start -> goal)
def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.col - goal.col)  # difference in x = difference in cols
        ydist: int = abs(ml.row - goal.row)  # difference in y = difference in rows
        return sqrt((xdist**2) + (ydist**2))  # distance = √((difference in x squared) + (difference in y squared)

    return distance


# calculate the manhattan distance (walking through a grid horizontally & vertically from start -> goal)
def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.col - goal.col)  # difference in x = difference in cols
        ydist: int = abs(ml.row - goal.row)  # difference in y = difference in rows
        return (xdist + ydist)  # manhattan distance = difference in x + difference in y

    return distance
