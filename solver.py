#!/usr/bin/env python3
"""
Eight-Puzzle Solver: UCS & A* (Misplaced + Manhattan)
"""
import heapq
import time
import sys

GOAL_STATE = (1,2,3,4,5,6,7,8,0)

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, g=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g
        self.h = 0

    def f(self):
        return self.g + self.h

def get_neighbors(state):
    zero = state.index(0)
    row, col = divmod(zero, 3)
    out = []
    if row > 0:
        lst = list(state); lst[zero], lst[zero-3] = lst[zero-3], lst[zero]
        out.append(('Up', tuple(lst)))
    if row < 2:
        lst = list(state); lst[zero], lst[zero+3] = lst[zero+3], lst[zero]
        out.append(('Down', tuple(lst)))
    if col > 0:
        lst = list(state); lst[zero], lst[zero-1] = lst[zero-1], lst[zero]
        out.append(('Left', tuple(lst)))
    if col < 2:
        lst = list(state); lst[zero], lst[zero+1] = lst[zero+1], lst[zero]
        out.append(('Right', tuple(lst)))
    return out
