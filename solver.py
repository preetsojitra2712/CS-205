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

