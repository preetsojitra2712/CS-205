import numpy as np

class Node:

    def __init__(self, board):
        self.board = board.copy()
        self.parent = None
        self.depth = 0
        self.cost = 0

    def is_goal(self, goal):
        """Return True if current board matches goal."""
        return np.array_equal(self.board, goal)

    def expand(self):
        """
        Generate all valid successor Nodes by sliding the blank (0).
        Returns a list of child Node objects.
        """
        # find the blank
        x0, y0 = np.argwhere(self.board == 0)[0]
        swaps = [(x0-1,y0),(x0+1,y0),(x0,y0-1),(x0,y0+1)]
        children = []

        for x,y in swaps:
            if 0 <= x < 3 and 0 <= y < 3:
                newb = self.board.copy()
                newb[x0,y0], newb[x,y] = newb[x,y], newb[x0,y0]
                child = Node(newb)
                child.parent = self
                child.depth = self.depth + 1
                children.append(child)

        return children

def misplaced_tiles(board, goal):
    """Number of tiles out of place (excluding blank)."""
    return int(((board != goal) & (board != 0)).sum())

def manhattan_distance(board, goal):
    """Sum of Manhattan distances of tiles from their goal positions."""
    dist = 0
    # map value→(row,col) in goal
    loc = { val:(i,j)
            for i,row in enumerate(goal)
            for j,val in enumerate(row) }
    for i in range(3):
        for j in range(3):
            v = board[i,j]
            if v != 0:
                gi,gj = loc[v]
                dist += abs(gi - i) + abs(gj - j)
    return dist

