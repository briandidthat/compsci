from __future__ import annotations
from typing import List, Optional
from utils.generic_search import bfs, Node, node_to_path

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
