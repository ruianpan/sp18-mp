"""
Heuristics functions
"""
__author__ = 'Zhengdai Hu'

import itertools


def manhattan_dist(current: tuple, goal: tuple):
    """
    Calculate Manhattan heuristic_distance between current point and goal point
    :param current: current point as a tuple
    :param goal: goal point as a tuple
    :return: heuristic_distance in Manhattan heuristic_distance
    """
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


def multidots_distance(curr, reverse_dict, goals):
    """

    :param dot_visited: dots visited upon hitting current nodes
    :param curr: Current node, as a tuple of x-axis, y-axis, visited times
    :param goals: set of all dots
    :return: estimated distance
    """
    # remaining = goals - dot_visited
    # return reduce(lambda s, i: s + manhattan_dist(curr[0:2], i), remaining, 0)
    # return reduce(lambda accu, i: manhattan_dist(curr, reverse_dict[curr[i]]), range(2, len(curr)), 0)
    return len(curr) - 2 - sum(curr[2:])


def naive_estimator(curr, goals):
    """

    :param curr: current state
    :param goals: All goals positions in a tuple
    :return:
    """
    curr_pos = curr[0:2]
    goals_reached = curr[2:]
    total = 0
    remains = 0
    minimum_travel = None
    for i, goal in zip(goals_reached, goals):
        if not i:
            dist = manhattan_dist(curr_pos, goal)
            total += dist
            if minimum_travel is None or minimum_travel > dist:
                minimum_travel = dist
            remains += 1
    if remains == 0:
        return -len(goals_reached)
    else:
        val = remains / total * minimum_travel - (len(goals_reached) - remains)
        return val


def __find(parent, vertex):
    if parent[vertex] != vertex:
        parent[vertex] = __find(parent, parent[vertex])
    return parent[vertex]


def __build_mst(remaining, edge_maps):
    edges = itertools.combinations(remaining, 2)
    sorted_edges = sorted(map(lambda e: (len(edge_maps[e[0]][e[1]]) - 1,) + e, edges))
    forests = {}
    total = 0
    counter = 0
    for edge in sorted_edges:
        u = edge[1]
        v = edge[2]
        if u in forests:
            u_parent = __find(forests, forests[u])
            if v in forests:
                v_parent = __find(forests, forests[v])
                if u_parent == v_parent:
                    continue
                else:
                    forests[v] = forests[v_parent] = u_parent
            else:  # v not in forest
                forests[v] = u_parent
        else:
            if v in forests:
                v_parent = __find(forests, forests[v])
                forests[u] = v_parent
            else:
                forests[u] = forests[v] = u
        total += edge[0]
        counter += 1
        if counter >= len(remaining) - 1:
            return total


def mst_estimator(curr, goals, edges):
    """

    :param edges:
    :param curr: current state
    :param goals: All goals positions in a tuple
    :return:
    """
    curr_pos = curr[0:2]
    goals_reached = curr[2:]
    remaining_goals = [curr_pos]
    num_remains = goals_reached.count(0)

    for i, goal in zip(goals_reached, goals):
        if not i:
            remaining_goals.append(goal)

    return __build_mst(remaining_goals, edges) if num_remains else 0
