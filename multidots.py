"""
Solutions for multi-dots traversal
"""
from copy import deepcopy

import itertools

from astar_base import expand, a_star
from frontier import Frontier
from heuristic import multidots_distance, MSTEstimator, estimate
from utilities import read_maze, get_position, START, GOAL, draw_path_on_maze, print_maze, get_goals, node_count, \
    reconstruct_path

__author__ = 'Zhengdai Hu'


def expand_multidots(current, edges):
    neighbors = edges[current[0:2]]
    return map(lambda x: x + current[2:], neighbors)


def init_state(position, goals):
    return position + tuple(0 for _ in goals)


def add_visited(this_goal: tuple, goals_to_indices: dict, original):
    """

    :param this_goal: a dot coordinates
    :param goals_to_indices: a dictionary mapping goal position to tuple index
    :param original: original state tuple
    :return:
    """
    pos = goals_to_indices[this_goal]
    return original[0:pos] + (1, ) + original[pos + 1:]


def a_star_multidots(edges, start: tuple, goals: tuple, estimate=multidots_distance):
    """
    Find the path from begin to the goal using Greedy Best-first Search Algorithm
    The algorithm is implemented based on the description on Wikipedia:
    https://en.wikipedia.org/wiki/Best-first_search#Greedy_BFS
    Notice: GBFS is suboptimal algorithm, so the solution MAY NOT BE OPTIMAL!
    :param estimate: Heuristics used in a_star search
    :param edges: Search space, as a 2D list
    :param start: Start point, as a tuple
    :param goals: Goal points, as a set of all dots
    :return: The path (if found) from begin to goal, or None
    """
    print('Analytics: begin node ' + str(start) +
          ', dots node ' + str(goals))

    goals_to_indices = {g: i for i, g in enumerate(goals, 2)}

    start = init_state(start, goals)
    if start[0:2] in goals:
        start = add_visited(start[0:2], goals_to_indices, start)

    # The set of nodes already evaluated
    visited = set()

    # For each node, the cost of getting from the begin node to that node.
    # The cost of going from begin to begin is zero.
    g_score = {start: 0}

    # For each node, the total cost of getting from the begin node to the dots
    # by passing by that node. That value is partly known, partly heuristic.
    # For the first node, that value is completely heuristic.
    # f_score = {begin: estimate(begin, dots_visited[begin], goals)}
    f_score = {start: estimate(start, goals)}

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
        if current[2:].count(1) == len(current) - 2:
            print('Analytics: ' + str(len(visited)) + ' expanded nodes, out of ' +
                  str(len(edges) * (2 ** (len(current) - 2))) + ' nodes')
            # draw_expanded_nodes(edges, visited)
            return reconstruct_path(came_from, current)

        visited.add(current)
        for neighbor in expand_multidots(current, edges):
            is_dot = False
            if neighbor[0:2] in goals:
                new_neighbor = add_visited(neighbor[0:2], goals_to_indices, neighbor)
                if new_neighbor != neighbor:
                    is_dot = True
                    neighbor = new_neighbor

            if neighbor in visited:  # revisit a node only if eating more dots, also more expensive
                # if not has_more(current, neighbor, dots_visited):
                #     continue
                # neighbor = (neighbor[0], neighbor[1], neighbor[2] + 1)
                continue

            g_through_current = g_score[current] + len(edges[current[0:2]][neighbor[0:2]])

            if (neighbor not in frontier or
                    g_through_current < g_score[neighbor]):
                # Discover a new node or a better path
                # dots_visited[neighbor] = deepcopy(dots_visited[current])
                # if neighbor[0:2] in goals:
                #     dots_visited[neighbor].add(neighbor[0:2])

                came_from[neighbor] = current
                g_score[neighbor] = g_through_current

                f_score[neighbor] = (g_score[neighbor] +
                                     # estimate(neighbor, dots_visited[neighbor], goals))
                                     estimate(neighbor, goals))
                frontier.add(neighbor, f_score[neighbor])

    return None


def build_goals_graph(start, nodes: tuple, matrix):
    nodes = nodes + (start, )
    edge_map = {node: {} for node in nodes}
    edges = itertools.combinations(nodes, 2)
    for edge in edges:
        u = edge[0]
        v = edge[1]
        shortest_path = a_star(maze, u, v)
        # maze_solution = deepcopy(matrix)
        # draw_path_on_maze(maze_solution, shortest_path)
        # print_maze(maze_solution)
        # print(shortest_path)
        edge_map[v][u] = edge_map[u][v] = shortest_path
    return edge_map


def expand_path(compressed, details):
    connected = [(u[0:2], v[0:2]) for u, v in zip(compressed[:-1], compressed[1:])]
    expanded = []
    total_length = 0
    for edge in connected:
        u = edge[0]
        v = edge[1]
        detail = details[u][v]
        total_length += len(detail) - 1
        if detail[0] != u:
            expanded.extend(reversed(detail))
        else:
            expanded.extend(detail)
        expanded.pop()
    print(expanded)
    print(len(expanded))
    return expanded


if __name__ == '__main__':
    maze = read_maze('mediumSearch.txt')
    # print(np.matrix(maze))

    begin = get_position(maze, START)
    dots = get_goals(maze)

    sub_paths = build_goals_graph(begin, dots, maze)
    # print(dots)
    path = a_star_multidots(sub_paths, begin, dots, estimate=estimate)
    full_path = expand_path(path, sub_paths)
    path = full_path
    if path:
        print('\n'.join(map(str, path)))
        draw_path_on_maze(maze, path)
        print('Total path length: ' + str(len(path) - 1))
        print_maze(maze)
    else:
        print('No possible path!')
