"""
MP1 Greedy Best-first Search, CS440 SP18
"""
__author__ = 'Zhengdai Hu'

from frontier import Frontier
from heuristic import manhattan_dist
from utilities import read_maze, draw_path_on_maze, get_position_with_symbol, START, GOAL, print_maze, reconstruct_path, \
    expand


def greedy(matrix, start, goal):
    """
    Find the path from begin to the goal using Greedy Best-first Search Algorithm
    The algorithm is implemented based on the description on Wikipedia:
    https://en.wikipedia.org/wiki/Best-first_search#Greedy_BFS
    Notice: GBFS is suboptimal algorithm, so the solution MAY NOT BE OPTIMAL!
    :param matrix: Search space, as a 2D list
    :param start: Start point, as a tuple
    :param goal: Goal point, as a tuple
    :return: The path (if found) from begin to goal, or None
    """
    print('Analytics: begin node ' + str(start) +
          ', goal node ' + str(goal))

    # The set of nodes already evaluated
    visited = set()
    partially_expanded = set()

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the begin node is known.
    # frontier is implemented as a priority queue
    frontier = Frontier()
    frontier.add(start, manhattan_dist(start, goal))

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, came_from will eventually contain the
    # most efficient previous step.
    came_from = {}

    while frontier:
        current, current_distance = frontier.nearest
        if current == goal:
            print('Analytics: ' + str(len(partially_expanded)) + ' expanded nodes, ' +
                  'among which ' + str(len(visited)) +
                  ' are fully expanded (all successors evaluated)')
            return reconstruct_path(came_from, current)

        partially_expanded.add(current)
        is_interrupted = False
        for neighbor in expand(current, matrix):
            if neighbor not in visited:
                neighbor_distance = manhattan_dist(neighbor, goal)
                if neighbor not in frontier:  # Discover a new node
                    came_from[neighbor] = current
                    frontier.add(neighbor, neighbor_distance)
                    if current_distance > neighbor_distance:
                        is_interrupted = True
                        break

        if not is_interrupted:
            frontier.pop_nearest()
            visited.add(current)

    return None


if __name__ == '__main__':
    maze = read_maze('bg.txt')
    # print(np.matrix(maze))

    path = greedy(maze, get_position_with_symbol(maze, START), get_position_with_symbol(maze, GOAL))
    if path:
        draw_path_on_maze(maze, path)
        print('Total path length: ' + str(len(path)))
        print_maze(maze)
    else:
        print('No possible path!')
