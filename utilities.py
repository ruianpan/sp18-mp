"""
Helper functions module
"""
__author__ = 'Zhengdai Hu'

import numpy as np

START = 'P'
GOAL = '.'
WALL = '%'


def read_maze(filename):  # take the file name as input and return the maze matrix
    print('Reading the maze')
    with open(filename) as file:
        matrix = [list(line.strip('\n ')) for line in file]
        print('Read complete')
        return matrix


def reconstruct_path(came_from, current):
    '''
    Reconstruct path from a map into a list
    :param came_from: Dictionary recording the predecessor of each node in path
    :param current: Start position
    :return: A path consisting a list of connecting points
    '''
    totalPath = [current]
    while current in came_from:
        current = came_from[current]
        totalPath.append(current)

    return totalPath


__order = '0123456789abcdefghijklmnopqr'


def draw_path_on_maze(matrix, path):
    '''
    Draw out path on the matrix. Notice that this function MODIFIES THE ORIGINAL MATRIX!!!
    :param matrix: The matrix the path to be drawn on
    :param path: A path consisting a list of connecting points
    '''
    order = (char for char in __order)
    for point in reversed(path):
        if matrix[point[0]][point[1]] == GOAL:
            matrix[point[0]][point[1]] = next(order)
        elif matrix[point[0]][point[1]] != START:
            matrix[point[0]][point[1]] = '+'


def print_maze(maze):
    print('\n'.join(' '.join(maze[i]) for i in range(len(maze))))


def get_position_with_symbol(maze, symbol):
    '''
    Helper function for getting start and goal positions
    :param maze: Current maze
    :param symbol: Symbol that designates either start('p') or goal('.') position
    :return: The requested position, in a tuple
    '''
    for row in range(len(maze)):
        for column in range(len(maze[0])):
            if maze[row][column] == symbol:
                return row, column


def get_goals(maze):
    goals = []
    for row in range(len(maze)):
        for column in range(len(maze[0])):
            if maze[row][column] == '.':
                goals.append((row, column))

    return tuple(goals)


def count_nodes(maze):
    from functools import reduce
    return sum([reduce(lambda x, y: x + 1 if y == ' ' else x, row, 0) for row in maze])


def is_illegal(point, matrix):
    '''
    Check if point is outside the matrix or is wall.
    :param point: point as a tuple
    :param matrix: current matrix
    :return: if the point is outside the matrix or is wall
    '''
    return (not (0 <= point[0] < len(matrix) and 0 <= point[1] < len(matrix[0])) or
            matrix[point[0]][point[1]] == WALL)


__edge_map = {}  # Provided astar is only applied in the same graph


def expand(node, matrix):
    if node not in __edge_map:
        transitions = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        neighbors = []
        for t in transitions:
            neighbor = tuple(np.add(node, t))
            if not is_illegal(neighbor, matrix):
                neighbors.append(neighbor)
        neighbors = tuple(neighbors)
        __edge_map[node] = neighbors

    return __edge_map[node]
