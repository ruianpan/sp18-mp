START = 'P'
GOAL = '.'


def readMaze(filename):  # take the file name as input and return the maze matrix
    print('Reading the maze')
    with open(filename) as file:
        matrix = [list(line.strip('\n ')) for line in file]
        print('Read complete')
        return matrix


def drawPathOnMaze(matrix, path):
    '''
    Draw out path on the matrix. Notice that this function MODIFIES THE ORIGINAL MATRIX!!!
    :param matrix: The matrix the path to be drawn on
    :param path: A path consisting a list of connecting points
    '''
    for point in path:
        if matrix[point[0]][point[1]] != 'P':
            matrix[point[0]][point[1]] = '.'


def getPosition(maze, symbol):
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
