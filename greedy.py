'''
MP1 Greedy Best-first Search, CS440 SP18
'''

__author__ = 'Zhengdai Hu'

from heapq import heappush, heappop
import numpy as np
from utilities import prepareMaze, drawPath, getPosition, START, GOAL


def distence(current, goal):
    '''
    Calculate Manhattan distance between current point and goal point
    :param current: current point as a tuple
    :param goal: goal point as a tuple
    :return: distance in Manhattan distance
    '''
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


def isIllegal(point, matrix):
    '''
    Check if point is outside the matrix or is wall.
    :param point: point as a tuple
    :param matrix: current matrix
    :return: if the point is outside the matrix or is wall
    '''
    return not (0 <= point[0] < len(matrix) and 0 <= point[1] < len(matrix[0])) or \
           matrix[point[0]][point[1]] == '%'


def greedy(matrix, start, goal):
    '''
    Find the path from start to the goal using Greedy Best-first Search Algorithm
    The algorithm is implemented based on the description on Wikipedia:
    https://en.wikipedia.org/wiki/Best-first_search#Greedy_BFS
    Notice: GBFS is suboptimal algorithm, so the solution MAY NOT BE OPTIMAL!
    :param matrix: Search space, as a 2D list
    :param start: Start point, as a tuple
    :param goal: Goal point, as a tuple
    :return: The path (if found) from start to goal, or None
    '''
    print(start, goal)

    # The set of nodes already evaluated
    closedSet = set()

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    # openQueue is implemented as a priority queue
    openQueue = []
    heappush(openQueue, (distence(start, goal), start))

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, cameFrom will eventually contain the
    # most efficient previous step.
    cameFrom = {}

    transitions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    while openQueue:
        currentNode = openQueue[0]
        currentDistance = currentNode[0]
        current = currentNode[1]
        if current == goal:
            return reconstructPath(cameFrom, current)

        isInterrupted = False
        for t in transitions:
            neighbor = tuple(np.add(current, t))
            if isIllegal(neighbor, matrix) or (neighbor in closedSet):
                continue

            neighborDistance = distence(neighbor, goal)
            if (neighborDistance, neighbor) not in openQueue:  # Discover a new node
                cameFrom[neighbor] = current
                heappush(openQueue, (neighborDistance, neighbor))
                if currentDistance > neighborDistance:
                    isInterrupted = True
                    break

        if not isInterrupted:
            heappop(openQueue)
            closedSet.add(current)

    return None


def reconstructPath(cameFrom, current):
    '''
    Reconstruct path from a map into a list
    :param cameFrom: Dictionary recording the predecessor of each node in path
    :param current: Start position
    :return: A path consisting a list of connecting points
    '''
    totalPath = [current]
    while current in cameFrom:
        current = cameFrom[current]
        totalPath.append(current)

    return totalPath


if __name__ == '__main__':
    maze = prepareMaze('bg.txt')
    # print(np.matrix(maze))

    path = greedy(maze, getPosition(maze, START), getPosition(maze, GOAL))
    if path:
        drawPath(maze, path)
        print(len(path))
        print(np.matrix([''.join(maze[i]) for i in range(len(maze))]))
    else:
        print('No possible path!')

