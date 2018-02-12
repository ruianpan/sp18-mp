'''
MP1 Greedy Best-first Search, CS440 SP18
'''
from frontier import Frontier
import numpy as np

from heuristic import manhattan_dist, euclidean_distance
from utilities import read_maze, draw_path_on_maze, get_position, START, GOAL, node_count, draw_expanded_nodes, \
    print_maze, reconstruct_path

__author__ = 'Zhengdai Hu'


def is_illegal(point, matrix):
    '''
    Check if point is outside the matrix or is wall.
    :param point: point as a tuple
    :param matrix: current matrix
    :return: if the point is outside the matrix or is wall
    '''
    return not (0 <= point[0] < len(matrix) and 0 <= point[1] < len(matrix[0])) or \
           matrix[point[0]][point[1]] == '%'


__edge_map = {}


def expand(node, matrix):
    if node not in __edge_map:
        transitions = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        neighbors = []
        for t in transitions:
            neighbor = tuple(np.add(node, t))
            if not is_illegal(neighbor, matrix):
                neighbors.append(neighbor)
        neighbors=tuple(neighbors)
        __edge_map[node] = neighbors

    return __edge_map[node]


def a_star(matrix, start, goal, estimate=manhattan_dist):
    """
    Find the path from begin to the goal using Greedy Best-first Search Algorithm
    The algorithm is implemented based on the description on Wikipedia:
    https://en.wikipedia.org/wiki/Best-first_search#Greedy_BFS
    Notice: GBFS is suboptimal algorithm, so the solution MAY NOT BE OPTIMAL!
    :param estimate: Heuristics used in a_star search
    :param matrix: Search space, as a 2D list
    :param start: Start point, as a tuple
    :param goal: Goal point, as a tuple
    :return: The path (if found) from begin to goal, or None
    """
    print('Analytics: begin node ' + str(start) +
          ', goal node ' + str(goal))

    # The set of nodes already evaluated
    visited = set()

    # For each node, the cost of getting from the begin node to that node.
    # The cost of going from begin to begin is zero.
    g_score = {start: 0}

    # For each node, the total cost of getting from the begin node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    # For the first node, that value is completely heuristic.
    f_score = {start: estimate(start, goal)}

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the begin node is known.
    # frontier is implemented as a priority queue
    frontier = Frontier()
    frontier.add(start, f_score[start])

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, came_from will eventually contain the
    # most efficient previous step.
    came_from = {}

    while frontier:
        current, current_f_score = frontier.pop_nearest()
        if current == goal:
            print('Analytics: ' + str(len(visited)) + ' expanded nodes, out of ' +
                  str(node_count(matrix)) + ' nodes')
            # draw_expanded_nodes(matrix, visited)
            return reconstruct_path(came_from, current)

        visited.add(current)
        for neighbor in expand(current, matrix):
            if neighbor not in visited:
                g_through_current = g_score[current] + 1  # every neighbor has distance 1

                if (neighbor not in frontier or
                        g_through_current < g_score[neighbor]):
                    # Discover a new node or a better path
                    came_from[neighbor] = current
                    g_score[neighbor] = g_through_current
                    f_score[neighbor] = (g_score[neighbor] +
                                         estimate(neighbor, goal))
                    frontier.add(neighbor, f_score[neighbor])

    return None


if __name__ == '__main__':
    maze = read_maze('om.txt')
    # print(np.matrix(maze))

    path = a_star(maze, get_position(maze, START), get_position(maze, GOAL))
    if path:
        draw_path_on_maze(maze, path)
        print('Total path length: ' + str(len(path)))
        print_maze(maze)
    else:
        print('No possible path!')
