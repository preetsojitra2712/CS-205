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

# Successor function: valid slides of the blank
def get_neighbors(state):
    zero = state.index(0)
    row, col = divmod(zero, 3)
    neighbors = []

    if row > 0:
        lst = list(state)
        lst[zero], lst[zero-3] = lst[zero-3], lst[zero]
        neighbors.append(('Up', tuple(lst)))

    if row < 2:
        lst = list(state)
        lst[zero], lst[zero+3] = lst[zero+3], lst[zero]
        neighbors.append(('Down', tuple(lst)))

    if col > 0:
        lst = list(state)
        lst[zero], lst[zero-1] = lst[zero-1], lst[zero]
        neighbors.append(('Left', tuple(lst)))

    if col < 2:
        lst = list(state)
        lst[zero], lst[zero+1] = lst[zero+1], lst[zero]
        neighbors.append(('Right', tuple(lst)))

    return neighbors



# Heuristics for A*


def h_misplaced(state):
    """Count of tiles not in goal position (excludes blank)."""
    return sum(1 for i, t in enumerate(state)
               if t != 0 and t != GOAL_STATE[i])

def h_manhattan(state):
    """Sum of Manhattan distances of tiles to their goal positions."""
    dist = 0
    for i, t in enumerate(state):
        if t == 0: continue
        gi = GOAL_STATE.index(t)
        dist += abs(i//3 - gi//3) + abs(i%3 - gi%3)
    return dist

# General search: UCS or A* depending on heuristic argument

def general_search(start, heuristic=None):
    root = PuzzleNode(start, g=0)
    if start == GOAL_STATE:
        return root, 0, 1

    frontier = []
    tie = 0
    heapq.heappush(frontier, (root.f(), tie, root))
    in_frontier = {start}
    explored = set()
    nodes_expanded = 0
    max_frontier = 1

    while frontier:
        _, _, current = heapq.heappop(frontier)
        in_frontier.remove(current.state)

        if current.state == GOAL_STATE:
            return current, nodes_expanded, max_frontier

        explored.add(current.state)
        nodes_expanded += 1

        for move, succ in get_neighbors(current.state):
            if succ in explored:
                continue
            child = PuzzleNode(succ, parent=current, move=move, g=current.g+1)
            if heuristic == 'misplaced':
                child.h = h_misplaced(succ)
            elif heuristic == 'manhattan':
                child.h = h_manhattan(succ)
            else:
                child.h = 0

            if succ not in in_frontier:
                tie += 1
                heapq.heappush(frontier, (child.f(), tie, child))
                in_frontier.add(succ)
                max_frontier = max(max_frontier, len(frontier))

    return None, nodes_expanded, max_frontier

