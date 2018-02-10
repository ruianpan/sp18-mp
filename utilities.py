START = 'P'
GOAL = '.'


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


def draw_path_on_maze(matrix, path):
    '''
    Draw out path on the matrix. Notice that this function MODIFIES THE ORIGINAL MATRIX!!!
    :param matrix: The matrix the path to be drawn on
    :param path: A path consisting a list of connecting points
    '''
    for point in path:
        if matrix[point[0]][point[1]] != 'P' and matrix[point[0]][point[1]] != '.':
            matrix[point[0]][point[1]] = '+'


def print_maze(maze):
    print('\n'.join(' '.join(maze[i]) for i in range(len(maze))))


def draw_expanded_nodes(matrix, nodes):
    for node in nodes:
        matrix[node[0]][node[1]] = '+'


def get_position(maze, symbol):
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
    goals = set()
    for row in range(len(maze)):
        for column in range(len(maze[0])):
            if maze[row][column] == '.':
                goals.add((row, column))

    return goals


def node_count(maze):
    from functools import reduce
    return sum(
        [reduce(lambda x, y: x + 1 if y == ' ' else x, row, 0) for row in maze]
    )
