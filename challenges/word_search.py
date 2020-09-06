from typing import NamedTuple, List, Dict, Optional
from random import choice
from string import ascii_uppercase
from utils.csp import CSP, Constraint, V, D

# Define Grid type alias to represent a 2d matrix
Grid = List[List[str]]


# class to represent any position in the grid
class GridLocation(NamedTuple):
    row: int
    col: int


def generate_grid(rows: int, cols: int) -> Grid:
    # generate grid with random letters
    return [[choice(ascii_uppercase) for _ in range(cols)] for r in range(rows)]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))


def generate_domain(word: str, grid: Grid) -> List[List[GridLocation]]:
    """
    The Domain of a word is is a list of lists of the possible locations of all it's letters. Words cannot just go
    anywhere though. They must stay within a row, column, or diagonal that is within the bounds of the grid.
    """

    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)

    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + length + 1)
            rows: range = range(row, row + length + 1)
            if col + length <= width:
                # left to right
                domain.append([GridLocation(row, c) for c in columns])
                # diagonal towards bottom right
                if row + length <= height:
                    domain.append([GridLocation(r, col + (r - row)) for r in rows])

            if row + length <= height:
                # top to bottom
                domain.append([GridLocation(r, col) for r in rows])
                # diagonal towards bottom left
                if col - length >= 0:
                    domain.append([GridLocation(r, col - (r - row)) for r in rows])
    return domain


class WordSearchConstraint(Constraint[str, List[GridLocation]]):
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        pass