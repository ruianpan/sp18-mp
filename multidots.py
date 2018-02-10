"""
Solutions for multi-dots traversal
"""
from copy import deepcopy

from astar_base import expand
from frontier import Frontier
from heuristic import multidots_distance
from utilities import read_maze, get_position, START, GOAL, draw_path_on_maze, print_maze, get_goals, node_count, \
    reconstruct_path

__author__ = 'Zhengdai Hu'


def expand_multidots(current, matrix, goals):
    neighbors = expand(current[0:2], matrix)
    return map(lambda x: x + current[2:], neighbors)


def has_more(current, neighbor, dots_visited):  # through current node we can visit more
    if neighbor[0:2] in dots_visited[current]:
        return len(dots_visited[current]) > len(dots_visited[neighbor])
    else:
        return len(dots_visited[current]) + 1 > len(dots_visited[neighbor])


def a_star_multidots(matrix, start, goals, estimate=multidots_distance):
    """
    Find the path from start to the goal using Greedy Best-first Search Algorithm
    The algorithm is implemented based on the description on Wikipedia:
    https://en.wikipedia.org/wiki/Best-first_search#Greedy_BFS
    Notice: GBFS is suboptimal algorithm, so the solution MAY NOT BE OPTIMAL!
    :param estimate: Heuristics used in a_star search
    :param matrix: Search space, as a 2D list
    :param start: Start point, as a tuple
    :param goals: Goal points, as a set of all dots
    :return: The path (if found) from start to goal, or None
    """
    print('Analytics: start node ' + str(start) +
          ', dots node ' + str(goals))

    start = start + (0, )  # start is now a tuple of x-axis, y-axis, and visited times

    # The set of nodes already evaluated
    visited = set()
    dots_visited = {start: set()}
    if start[0:2] in goals:
        dots_visited[start].add(start[0:2])

    # For each node, the cost of getting from the start node to that node.
    # The cost of going from start to start is zero.
    g_score = {start: 0}

    # For each node, the total cost of getting from the start node to the dots
    # by passing by that node. That value is partly known, partly heuristic.
    # For the first node, that value is completely heuristic.
    f_score = {start: estimate(start, dots_visited[start], goals)}

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    # frontier is implemented as a priority queue
    frontier = Frontier()
    frontier.add(start, f_score[start])

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, came_from will eventually contain the
    # most efficient previous step.
    came_from = {}

    while frontier:
        current, current_f_score = frontier.pop_nearest()
        if dots_visited[current] == goals:
            print('Analytics: ' + str(len(visited)) + ' expanded nodes, out of ' +
                  str(node_count(matrix)) + ' nodes')
            # draw_expanded_nodes(matrix, visited)
            return reconstruct_path(came_from, current)

        visited.add(current)
        for neighbor in expand_multidots(current, matrix, goals):
            if neighbor in visited:  # revisit a node only if eating more dots, also more expensive
                if not has_more(current, neighbor, dots_visited):
                    continue
                neighbor = (neighbor[0], neighbor[1], neighbor[2] + 1)

            g_through_current = g_score[current] + 1  # every neighbor has distance 1

            if (neighbor not in frontier or
                    g_through_current < g_score[neighbor]):
                # Discover a new node or a better path
                came_from[neighbor] = current
                g_score[neighbor] = g_through_current

                dots_visited[neighbor] = deepcopy(dots_visited[current])
                if neighbor[0:2] in goals:
                    dots_visited[neighbor].add(neighbor[0:2])

                f_score[neighbor] = (g_score[neighbor] +
                                     estimate(neighbor, dots_visited[neighbor], goals))
                frontier.add(neighbor, f_score[neighbor])

    return None


if __name__ == '__main__':
    maze = read_maze('tinySearch.txt')
    # print(np.matrix(maze))

    start_node = get_position(maze, START)
    dots = get_goals(maze)
    print(start_node, dots)

    path = a_star_multidots(maze, start_node, dots)
    if path:
        print(path)
        draw_path_on_maze(maze, path)
        print('Total path length: ' + str(len(path)))
        print_maze(maze)
    else:
        print('No possible path!')
