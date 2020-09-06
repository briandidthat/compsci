from utils.csp import Constraint, CSP
from typing import Dict, List, Optional


class QueensConstraint(Constraint[int, int]):
    def __init__(self, columns: List[int]) -> None:
        super().__init__(columns)
        self.columns: List[int] = columns

    def satisfied(self, assignment: Dict[int, int]) -> bool:
        for q1c, q1r in assignment.items():  # q1c = queen1 column, q1r = queen1 row
            for q2c in range(q1c + 1, len(self.columns) + 1):  # q2c = queen2 column, for comparison with q1
                if q2c in assignment:  # if q2s column is in assignment already
                    q2r: int = assignment[q2c]  # q2r = queen 2 row
                    if q1r == q2r:  # if two queens are in the same row
                        return False
                    if abs(q1r - q2r) == abs(q1c - q2c):  # if two queens are in the same diagonal
                        return False
        return True


if __name__ == "__main__":
    columns: List[int] = [1, 2, 3, 4, 5, 6, 7, 8]
    rows: Dict[int, List[int]] = {}

    for column in columns:
        rows[column] = [1, 2, 3, 4, 5, 6, 7, 8]

    csp: CSP[int, int] = CSP(columns, rows)
    csp.add_constraint(QueensConstraint(columns))
    solution: Optional[Dict[int, int]] = csp.backtracking_search()

    if solution is None:
        print("No solution found!")
    else:
        print(solution)