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
