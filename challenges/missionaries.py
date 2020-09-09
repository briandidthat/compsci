from __future__ import annotations
from typing import List, Optional
from utils.generic_search import bfs, Node, node_to_path

"""
MISSIONARIES AND CANNIBALS
"""


MAX_NUM: int = 3  # maximum number of cannibals or missionaries at any time


class MCState:
    def __init__(self, missionaries: int, cannibals: int, boat: bool) -> None:
        self.wm: int = missionaries  # this will represent the missionaries on the west bank at any time
        self.wc: int = cannibals  # this will represent the cannibals on the west bank at any time
        self.em: int = MAX_NUM - self.wm  # this will represent the east bank missionaries at any time
        self.ec: int = MAX_NUM - self.wc  # this will represent the east bank cannibals at any time
        self.boat: bool = boat  # West == True, East == False

    @property
    def is_legal(self) -> bool:
        if self.wm < self.wc and self.wm > 0:
            return False
        if self.em < self.ec and self.em > 0:
            return False
        return True

    def goal_test(self) -> bool:
        return self.is_legal and self.em == MAX_NUM and self.ec == MAX_NUM

    def __str__(self) -> str:
        return (f"On the west bank there are {self.wm} missionaries and {self.wc} cannibals.\n"
                f"On the east bank there are {self.em} missionaries and {self.ec} cannibals.\n"
                f"The boat is on the {'west' if self.boat else 'east'} bank.")

    # get list of successors and try every possible combination, then filter out the illegal moves
    def successors(self) -> List[MCState]:
        children: List[MCState] = []
        if self.boat:  # boat is on west bank
            if self.wm > 1:  # if there are more than one missionaries on west bank
                children.append(MCState(self.wm - 2, self.wc, not self.boat))
            if self.wm > 0:  # if there are at least one missionaries on west bank
                children.append(MCState(self.wm - 1, self.wc, not self.boat))
            if self.wc > 1:  # if there are more than one cannibals on west bank
                children.append(MCState(self.wm, self.wc - 2, not self.boat))
            if self.wc > 0:  # if there are at least one cannibals on west bank
                children.append(MCState(self.wm, self.wc - 1, not self.boat))
            if (self.wc > 0) and (self.wm > 0):  # if there are more than one missionary or cannibal on west bank
                children.append(MCState(self.wm - 1, self.wc - 1, not self.boat))
        else:  # boat is on east bank
            if self.em > 1:  # if there are more than one missionaries on east bank
                children.append(MCState(self.wm + 2, self.wc, not self.boat))
            if self.em > 0:  # if there are at least one missionaries on east bank
                children.append(MCState(self.wm + 1, self.wc, not self.boat))
            if self.ec > 1:  # if there are more than one cannibals on east bank
                children.append(MCState(self.wm, self.wc + 2, not self.boat))
            if self.ec > 0:  # if there are at least one cannibals on east bank
                children.append(MCState(self.wm, self.wc + 1, not self.boat))
            if (self.ec > 0) and (self.em > 0):  # if there are more than one missionary or cannibal on east bank
                children.append(MCState(self.wm + 1, self.wc + 1, not self.boat))

        return [x for x in children if x.is_legal]


# display the solution to the problem
def display_solution(path: List[MCState]) -> None:
    if len(path) == 0:
        return

    old_state = path[0]
    print(old_state)
    for current_state in path[1:]:  # start at second index to compare with old state
        if current_state.boat:  # if boat is on west
            statement = (
                f"{old_state.em - current_state.em} missionaries and {old_state.ec - current_state.ec} cannibals "
                f"moved from the east bank to west bank.\n"
            )
            print(statement)
        else:  # if boat is on east
            statement = (
                f"{old_state.wm - current_state.wm} missionaries and {old_state.wc - current_state.wc} cannibals "
                f"moved from the west bank to east bank.\n"
            )
            print(statement)
        print(current_state)
        old_state = current_state


if __name__ == "__main__":
    start: MCState = MCState(MAX_NUM, MAX_NUM, True)
    solution: Optional[Node[MCState]] = bfs(start, MCState.goal_test, MCState.successors)

    if solution is None:
        print("No solution found.")
    else:
        path: List[MCState] = node_to_path(solution)
        display_solution(path)

