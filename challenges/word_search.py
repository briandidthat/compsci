from typing import NamedTuple, List, Dict, Optional
from random import choice
from string import ascii_uppercase
from utils.csp import CSP, Constraint, V, D

"""
WORD SEARCH PROBLEM
A word search is a grid of letters with hidden words placed across rows, columns and diagonals. A player of a word
search puzzle attempts to find the hidden words by carefully scanning through the grid. Finding places to put the words 
is a kind of constraint satisfaction problem. The variables are the words and the domains are the possible locations of 
those words.
"""


# Define Grid type alias to represent a 2d matrix
Grid = List[List[str]]


# class to represent any position in the grid
class GridLocation(NamedTuple):
    row: int
    col: int


def generate_grid(rows: int, cols: int) -> Grid:
    # generate grid with random letters
    return [[choice(ascii_uppercase) for _ in range(cols)] for _ in range(rows)]


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
    def __init__(self, words: List[str]) -> None:
        super().__init__(words)
        self.words: List[str] = words

    def satisfied(self, assignment: Dict[V, D]) -> bool:
        # if there are any duplicates across the grid, then there is an overlap
        all_locations = [locs for values in assignment.values() for locs in values]
        return len(set(all_locations)) == len(all_locations)


if __name__ == "__main__":
    grid: Grid = generate_grid(9, 9)
    words: List[str] = ["MATTHEW", "JOE", "MARY", "SARAH", "SALLY"]
    locations: Dict[str, List[GridLocation]] = {}

    for word in words:
        locations[word] = generate_domain(word, grid)

    csp: CSP[str, List[GridLocation]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))
    solution = csp.backtracking_search()

    if solution is None:
        print("No solution found!")
    else:
        for word, grid_locations in solution.items():
            if choice([True, False]):
                grid_locations.reverse()
            for index, letter in enumerate(word):
                (row, col) = (grid_locations[index].row, grid_locations[index].col)
                grid[row][col] = letter
        display_grid(grid)