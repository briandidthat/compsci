import random
from enum import Enum
from math import sqrt
from typing import NamedTuple, List, Callable, Optional


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    row: int
    col: int


class Maze:
    """
    Maze: Will internally keep track of a grid, (matrix) representing it's state. It will be randomly filled
    with blocked cells when created. Sparseness will be 0.2 by default representing a 20% blocked state on the
    grid.
    """
    def __init__(self, rows=10, columns=10, sparseness=0.2, start=MazeLocation(9, 9), goal=MazeLocation(9, 9)):
        # initialize instant variables
        self._rows = rows
        self._columns = columns
        self.start = start
        self.goal = goal
        self._grid = [[Cell.EMPTY for c in range(columns)] for r in range(rows)]
        self._randomly_fill(rows, columns, sparseness)

    # populate the grid with blocked cells
    def _randomly_fill(self, rows, columns, sparseness):
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


