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

