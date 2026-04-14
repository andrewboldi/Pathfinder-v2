import numpy as np
import tqdm
from datetime import datetime

from core.geo import distance


def astar_search(start: str, end: str, tree: dict, all_nodes) -> list:
    """A* search from start to end using the given adjacency tree.

    Args:
        start: 'lat,lon' string for start node
        end: 'lat,lon' string for end node
        tree: adjacency dict {node: [[adjacent_node, cost], ...]}
        all_nodes: iterable of all node keys (for heuristic precomputation)

    Returns:
        List of 'lat,lon' strings representing the optimal path.
    """
    print("Starting heuristic calculations...")
    starttime = datetime.now()
    heuristic = {}
    for coord in tqdm.tqdm(all_nodes, desc="Heuristic Calculations"):
        heuristic[coord] = distance(coord, end)
    endtime = datetime.now()
    print(f"Heuristic Calculations took {endtime - starttime}s!\n")

    cost = {start: 0}
    closed = []
    opened = [[start, heuristic[start]]]

    count = 0
    while True:
        fn = [i[1] for i in opened]
        if count % 1000 == 0:
            print(len(fn))
            print(heuristic[min(np.array(opened)[:, 0])])
            if count % 10000 == 2000:
                print(start, end)

        chosen_index = fn.index(min(fn))
        node = opened[chosen_index][0]
        closed.append(opened[chosen_index])
        del opened[chosen_index]

        if closed[-1][0] == end:
            break

        temparr = [closed_item[0] for closed_item in closed]
        for item in tree[node]:
            if item[0] in temparr:
                continue
            cost[item[0]] = cost[node] + item[1]
            fn_node = cost[node] + heuristic[item[0]]
            opened.append([item[0], fn_node])
        count += 1

    # Reconstruct optimal path
    trace_node = end
    optimal_sequence = [end]
    for i in range(len(closed) - 2, -1, -1):
        check_node = closed[i][0]
        if trace_node in [children[0] for children in tree[check_node]]:
            children_costs = [temp[1] for temp in tree[check_node]]
            children_nodes = [temp[0] for temp in tree[check_node]]
            if cost[check_node] + children_costs[children_nodes.index(trace_node)] == cost[trace_node]:
                optimal_sequence.append(check_node)
                trace_node = check_node

    optimal_sequence.reverse()
    return optimal_sequence


def astar_multi_endpoint(start: str, end: str, tree: dict, all_nodes) -> list:
    """A* variant that supports multi-endpoint heuristic (from Percolation/old.py).

    Same interface as astar_search but stores heuristics as lists for
    potential multi-endpoint extension.
    """
    print("Starting heuristic calculations...")
    starttime = datetime.now()
    heuristic = {}
    for coord in tqdm.tqdm(all_nodes, desc="Heuristic Calculations"):
        heuristic[coord] = [distance(coord, end)]
    endtime = datetime.now()
    print(f"Heuristic Calculations took {endtime - starttime}s!\n")

    cost = {start: 0}
    closed = []
    opened = [[start, heuristic[start]]]

    count = 0
    while True:
        fn = [i[1] for i in opened]
        if count % 1000 == 0:
            print(len(fn))
            if count % 10000 == 2000:
                print(start, end)

        chosen_index = fn.index(min(fn))
        node = opened[chosen_index][0]
        closed.append(opened[chosen_index])
        del opened[chosen_index]

        if closed[-1][0] == end:
            break

        temparr = [closed_item[0] for closed_item in closed]
        for item in tree[node]:
            if item[0] in temparr:
                continue
            cost[item[0]] = cost[node] + item[1]
            fn_node = cost[node] + heuristic[item[0]][0]
            opened.append([item[0], fn_node])
        count += 1

    trace_node = end
    optimal_sequence = [end]
    for i in range(len(closed) - 2, -1, -1):
        check_node = closed[i][0]
        if trace_node in [children[0] for children in tree[check_node]]:
            children_costs = [temp[1] for temp in tree[check_node]]
            children_nodes = [temp[0] for temp in tree[check_node]]
            if cost[check_node] + children_costs[children_nodes.index(trace_node)] == cost[trace_node]:
                optimal_sequence.append(check_node)
                trace_node = check_node

    optimal_sequence.reverse()
    return optimal_sequence
