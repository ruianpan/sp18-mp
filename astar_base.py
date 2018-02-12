"""
MP1 Greedy Best-first Search, CS440 SP18
"""
__author__ = 'Zhengdai Hu'

from frontier import Frontier
from heuristic import manhattan_dist
from utilities import read_maze, draw_path_on_maze, get_position_with_symbol, START, GOAL, count_nodes, \
    print_maze, reconstruct_path, expand


def a_star(matrix, start, goal, estimate=manhattan_dist):
    """
    Find the path from start to the goal using Greedy Best-first Search Algorithm
    The algorithm is implemented based on the description on Wikipedia:
    https://en.wikipedia.org/wiki/Best-first_search#Greedy_BFS
    Notice: GBFS is suboptimal algorithm, so the solution MAY NOT BE OPTIMAL!
    :param estimate: Heuristics used in a_star search
    :param matrix: Search space, as a 2D list
    :param start: Start point, as a tuple
    :param goal: Goal point, as a tuple
    :return: The path (if found) from start to goal, or None
    """
    print('Analytics: start node ' + str(start) +
          ', goal node ' + str(goal))

    # The set of nodes already evaluated
    visited = set()

    # For each node, the cost of getting from the start node to that node.
    # The cost of going from start to start is zero.
    g_score = {start: 0}

    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    # For the first node, that value is completely heuristic.
    f_score = {start: estimate(start, goal)}

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
        if current == goal:
            print('Analytics: ' + str(len(visited)) + ' expanded nodes, out of ' +
                  str(count_nodes(matrix)) + ' nodes')
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
    maze = read_maze('bg.txt')
    # print(np.matrix(maze))

    path = a_star(maze, get_position_with_symbol(maze, START), get_position_with_symbol(maze, GOAL))
    if path:
        draw_path_on_maze(maze, path)
        print('Total path length: ' + str(len(path)))
        print_maze(maze)
    else:
        print('No possible path!')
