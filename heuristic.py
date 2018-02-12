"""
Heuristics functions
"""
from functools import reduce

import numpy as np
import itertools

__author__ = 'Zhengdai Hu'


def manhattan_dist(current: tuple, goal: tuple):
    """
    Calculate Manhattan heuristic_distance between current point and goal point
    :param current: current point as a tuple
    :param goal: goal point as a tuple
    :return: heuristic_distance in Manhattan heuristic_distance
    """
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


def euclidean_distance(current: tuple, goal: tuple):
    """
    Calculate Manhattan heuristic_distance between current point and goal point
    :param current: current point as a tuple
    :param goal: goal point as a tuple
    :return: heuristic_distance in Manhattan heuristic_distance
    """
    return np.linalg.norm(np.subtract(current, goal))


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
    return 0
    return len(curr) - 2 - sum(curr[2:])


def estimate(curr, goals):
    """

    :param curr: current state
    :param goals: All goals positions in a tuple
    :return:
    """
    curr_pos = curr[0:2]
    goals_reached = curr[2:]
    total = 0
    remains = 0
    for i, goal in zip(goals_reached, goals):
        if not i:
            total += manhattan_dist(curr_pos, goal)
            remains += 1
    if remains == 0:
        return -len(goals_reached)
    else:
        val = total / remains - (len(goals_reached) - remains)
        return val


class MSTEstimator:

    def __init__(self, nodes) -> None:
        super().__init__()
        self.nodes = nodes
        self.edges = itertools.combinations(nodes, 2)
        self.edges = sorted(map(lambda edge: (manhattan_dist(edge[0], edge[1]),) + edge,
                                self.edges))
        # self.mst = self.build_mst()

    @staticmethod
    def __find(parent, vertex):
        if parent[vertex] != vertex:
            parent[vertex] = MSTEstimator.__find(parent, parent[vertex])
        return parent[vertex]

    def build_mst(self, remaining):
        self.nodes = remaining
        self.edges = itertools.combinations(remaining, 2)
        self.edges = sorted(map(lambda edge: (manhattan_dist(edge[0], edge[1]),) + edge,
                                self.edges))
        # sorted_edges = sorted(self.edges)
        sorted_edges = self.edges
        forests = {}
        mst = set()
        total = 0
        for edge in sorted_edges:
            u = edge[1]
            v = edge[2]
            if v not in remaining or u not in remaining:
                continue
            if u in forests:
                if v in forests:
                    if (MSTEstimator.__find(forests, u) ==
                            MSTEstimator.__find(forests, v)):
                        continue
                    else:
                        forests[v] = MSTEstimator.__find(forests, u)
                else:
                    forests[v] = MSTEstimator.__find(forests, u)
            else:
                if v in forests:
                    forests[u] = MSTEstimator.__find(forests, v)
                else:
                    forests[u] = forests[v] = u
            # mst.add(edge)
            total += edge[0]
        return total
