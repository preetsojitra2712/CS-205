# eight_puzzle_solver.py

import numpy as np
import time

# --- some preset puzzles at various depths ---
START_D0 = np.array([[1,2,3],
                     [4,5,6],
                     [7,8,0]])

START_D2 = np.array([[1,2,3],
                     [4,5,6],
                     [0,7,8]])

START_D4 = np.array([[1,2,3],
                     [5,0,6],
                     [4,7,8]])

START_D8  = np.array([[1,3,6],
                     [5,0,2],
                     [4,7,8]])

START_D12 = np.array([[1,3,6],
                     [5,0,7],
                     [4,8,2]])

START_D16 = np.array([[1,6,7],
                     [5,0,3],
                     [4,8,2]])

START_D20 = np.array([[7,1,2],
                     [4,8,5],
                     [6,3,0]])

START_D24 = np.array([[0,7,2],
                     [4,6,1],
                     [3,5,8]])

GOAL_STATE = np.array([[1,2,3],
                       [4,5,6],
                       [7,8,0]])
class PuzzleNode:
    """
    A node in the search tree, wrapping a puzzle configuration.
    """
    def __init__(self, config):
        self.config       = config
        self.parent       = None
        self.depth        = 0
        self.expand_count = 0
        self.max_frontier = 0
        self.score        = 0  # g + h

    def is_goal(self):
        return np.array_equal(self.config, GOAL_STATE)

    def successors(self):
        # locate blank (0)
        size = len(self.config)
        x, y = next((i,j)
                    for i in range(size)
                    for j in range(size)
                    if self.config[i][j]==0)

        # helper to swap blank with neighbor
        def swap(a,b,c,d):
            new = self.config.copy()
            new[a][b], new[c][d] = new[c][d], new[a][b]
            return new

        moves = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        children = []
        for nx,ny in moves:
            if 0 <= nx < size and 0 <= ny < size:
                child = PuzzleNode(swap(x,y,nx,ny))
                child.parent = self
                child.depth  = self.depth + 1
                children.append(child)
        return children

