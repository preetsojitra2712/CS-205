#!/usr/bin/env python3
"""
Eight-Puzzle Solver: UCS & A* (Misplaced + Manhattan)
"""
import heapq
import time
import sys

GOAL_STATE = (1,2,3,4,5,6,7,8,0)
