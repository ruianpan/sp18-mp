"""
Heuristics functions
"""
from functools import reduce

import numpy as np

__author__ = 'Zhengdai Hu'


def manhattan_distance(current: tuple, goal: tuple):
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


def multidots_distance(curr, dot_visited, goals):
    """

    :param dot_visited: dots visited upon hitting current nodes
    :param curr: Current node, as a tuple of x-axis, y-axis, visited times
    :param goals: set of all dots
    :return: estimated distance
    """
    remaining = goals - dot_visited
    return reduce(lambda est, dot: est + manhattan_distance(curr[0:2], dot), remaining, 0)
