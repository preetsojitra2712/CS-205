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

# Define the goal state for the puzzle
GOAL_STATE = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)

# Node class represents each state in the search tree
class Node:
    def __init__(self, state, parent=None, move=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = path_cost  # Path cost
        self.h = 0          # Heuristic value (default 0)

    def f(self):
        return self.g + self.h  # Total cost = path + heuristic

    def __lt__(self, other):
        return self.f() < other.f()

# Check if the current state is the goal
def goal_test(state):
    return state == GOAL_STATE

# Create a new node with the given initial state
def make_node(initial_state):
    return Node(initial_state)

# Create a priority queue initialized with the start node
def make_queue(start_node):
    queue = []
    heapq.heappush(queue, (start_node.f(), 0, start_node))
    return queue

# Remove and return the node with the lowest cost from the queue
def remove_front(queue):
    return heapq.heappop(queue)[2]

# Generate all valid successor states from a node
def expand(node):
    children = []
    zero_index = node.state.index(0)
    row, col = divmod(zero_index, 3)
    directions = {
        'Up': -3, 'Down': 3, 'Left': -1, 'Right': 1
    }

    for move, delta in directions.items():
        new_index = zero_index + delta
        # Skip invalid moves based on position
        if move == 'Up' and row == 0: continue
        if move == 'Down' and row == 2: continue
        if move == 'Left' and col == 0: continue
        if move == 'Right' and col == 2: continue

        # Swap the blank with the target tile
        new_state = list(node.state)
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        child = Node(tuple(new_state), parent=node, move=move, path_cost=node.g + 1)
        children.append(child)

    return children

# Heuristic: count of misplaced tiles
def h_misplaced(state):
    return sum(1 for i, t in enumerate(state) if t != 0 and t != GOAL_STATE[i])

# Heuristic: sum of Manhattan distances
def h_manhattan(state):
    return sum(abs(i // 3 - GOAL_STATE.index(t) // 3) + abs(i % 3 - GOAL_STATE.index(t) % 3)
               for i, t in enumerate(state) if t != 0)

# General search algorithm with heuristic-aware queueing function
def general_search(problem_initial_state, queueing_function):
    nodes = make_queue(make_node(problem_initial_state))
    explored = set()
    in_frontier = {problem_initial_state}
    tie = 1
    max_queue_size = 1
    nodes_expanded = 0

    while True:
        if not nodes:
            return None, nodes_expanded, max_queue_size

        node = remove_front(nodes)
        in_frontier.remove(node.state)

        if goal_test(node.state):
            return node, nodes_expanded, max_queue_size

        explored.add(node.state)
        nodes_expanded += 1
        expanded_nodes = expand(node)
        nodes = queueing_function(nodes, expanded_nodes, in_frontier, explored, tie)
        tie += len(expanded_nodes)
        max_queue_size = max(max_queue_size, len(nodes))

# Queueing function that pushes children into the priority queue with heuristic
def queueing_function(nodes, children, in_frontier, explored, tie_start):
    tie = tie_start
    for child in children:
        # Assign heuristic value depending on selected algorithm
        if heuristic_option == 'misplaced':
            child.h = h_misplaced(child.state)
        elif heuristic_option == 'manhattan':
            child.h = h_manhattan(child.state)
        else:
            child.h = 0

        if child.state not in explored and child.state not in in_frontier:
            heapq.heappush(nodes, (child.f(), tie, child))
            in_frontier.add(child.state)
            tie += 1
    return nodes

# Reconstruct path from goal node to start
def reconstruct_path(goal_node):
    path = []
    while goal_node:
        path.append(goal_node)
        goal_node = goal_node.parent
    return list(reversed(path))

# Print the path from start to goal
def print_solution(path):
    for i, node in enumerate(path):
        print(f"\nStep {i}: {node.move or 'Start'}")
        for r in range(3):
            print(" ", node.state[3*r : 3*r+3])

# Allow user to input a custom puzzle state
def read_custom_state():
    print("Enter your puzzle (0 = blank):")
    vals = []
    for r in range(3):
        row = input(f" Row {r+1}: ").split()
        vals.extend(int(x) for x in row)
    return tuple(vals)

# Main function for user interaction and execution
def main():
    global heuristic_option
    print("Eight-Puzzle Solver")
    print(" 1) Default puzzle")
    print(" 2) Enter your own")
    choice = input("> ").strip()

    # Choose initial state
    if choice == '1':
        start = (8, 6, 7, 2, 5, 4, 3, 0, 1)
    elif choice == '2':
        start = read_custom_state()
    else:
        print("Invalid choice."); sys.exit(1)

    # Choose algorithm
    print("\nSelect algorithm:")
    print("  1) UCS")
    print("  2) A* Misplaced-Tile")
    print("  3) A* Manhattan")
    algo = input("> ").strip()

    heuristic_option = None
    if algo == '2':
        heuristic_option = 'misplaced'
    elif algo == '3':
        heuristic_option = 'manhattan'
    elif algo != '1':
        print("Invalid selection."); sys.exit(1)

    # Execute general search
    start_time = time.time()
    goal_node, expanded, max_q = general_search(start, queueing_function)
    end_time = time.time()

    # Output results
    if goal_node:
        path = reconstruct_path(goal_node)
        print_solution(path)
        print(f"\nDepth: {len(path) - 1}")
        print(f"Cost: {goal_node.g}")
        print(f"Expanded: {expanded}")
        print(f"Max queue size: {max_q}")
    else:
        print("No solution found.")

    print(f"Elapsed time: {(end_time - start_time)*1000:.1f} ms")

# Entry point
if __name__ == "__main__":
    main()

