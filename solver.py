#!/usr/bin/env python3
"""
Eight-Puzzle Solver

This script implements:
  - Uniform-Cost Search (UCS)
  - A* with Misplaced-Tile heuristic
  - A* with Manhattan-Distance heuristic
States are flat 9-tuples, 0 is the blank.
"""

import heapq
import time
import sys

# Goal configuration as a flat tuple
GOAL_STATE = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)

# Node class for search tree
class PuzzleNode:
    """
    state: flat tuple
    parent: PuzzleNode
    move: str that generated this node
    g: path cost
    h: heuristic cost
    """
    def __init__(self, state, parent=None, move=None, g=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g
        self.h = 0

    def f(self):
        # Total cost f = g + h.
        return self.g + self.h
