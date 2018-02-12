"""
This class implements the A*.
"""
import sys

def findStart(maze):
    """
    Find the begin position of the maze
    """
    start_Position = 0
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == 'P':
                start_Position = i * len(maze[0]) + j
                return start_Position
    return -1

def findEnd(maze):
    """
    Find the end position of the maze
    """
    final_Position = 0
    for i in range(0, len(maze)):
        for j in range(0, len(maze[0])):
            if maze[i][j] == '.':
                final_Position = i * len(maze[0]) + j
                return final_Position
    return -1


def distance(currX, currY, targetX, targetY):
    """
    Get the distance between two positions
    """
    return abs(currX - targetX) + abs(currY - targetY)


def findMin(list, t_value):
    """
    Get the min f_value of a list
    """
    currMin = sys.maxsize
    result = 0
    for index in list:
        if t_value[index] < currMin:
            currMin = t_value[index]
            result = index
    return result

def findPath(maze):
    """
    Find the solution of the maze(A*)
    """
    #Get the width, height and size of maze
    width = len(maze[0])
    height = len(maze)
    size = width * height

    #Start position
    start_Position = findStart(maze)
    startX = start_Position % width
    startY = start_Position / width
    #End position
    end_Position = findEnd(maze)
    endX = end_Position % width
    endY = end_Position / width

    #Mark visited place
    visited = [0 for x in range(size)]

    #distance value
    f_value = [sys.maxsize for x in range(size)]
    #total value
    t_value = [sys.maxsize for x in range(size)]

    #Keep track of the position of parent node
    parent_Position = [0 for x in range(size)]

    #Keep track of the number of node expanded
    node_expanded = 0

    list = []
    list.append(start_Position)
    f_value[start_Position] = 0
    t_value[start_Position] = distance(startX, startY, endX, endY)

    while len(list) != 0:
        #find current best
        curr = findMin(list, t_value)

        list.remove(curr)
        currY = curr / width
        currX = curr % width
        visited[curr] = 1

        #Target Position finded
        if maze[currY][currX] == '.':
            break

        #Increase the node expanded
        node_expanded += 1

        #Left
        if currX - 1 >= 0 and maze[currY][currX - 1] != '%':
            if visited[curr - 1] != 1:
                if curr - 1 not in list:
                    list.append(curr - 1)
                curr_val = f_value[curr] + 1
                if curr_val < f_value[curr - 1]:
                    f_value[curr - 1] = curr_val
                    t_value[curr - 1] = f_value[curr - 1] + distance((curr - 1) % width, (curr - 1) / width, endX, endY)
                    parent_Position[curr - 1] = curr


        #Right
        if currX + 1 < width and maze[currY][currX + 1] != '%':
            if curr + 1 < size and visited[curr + 1] != 1:
                if curr + 1 not in list:
                    list.append(curr + 1)
                curr_val = f_value[curr] + 1
                if curr_val < f_value[curr + 1]:
                    f_value[curr + 1] = curr_val
                    t_value[curr + 1] = f_value[curr + 1] + distance((curr + 1) % width, (curr + 1) / width, endX, endY)
                    parent_Position[curr + 1] = curr

        #Up
        if currY - 1 >= 0 and maze[currY - 1][currX] != '%':
            if visited[curr - width] != 1:
                if curr - width not in list:
                    list.append(curr - width)
                curr_val = f_value[curr] + 1
                if curr_val < f_value[curr - width]:
                    f_value[curr - width] = curr_val
                    t_value[curr - width] = f_value[curr - width] + distance((curr - width) % width, (curr - width) / width, endX, endY)
                    parent_Position[curr - width] = curr

        #Down
        if currY + 1 < height and maze[currY + 1][currX] != '%':
            if visited[curr + width] != 1:
                if curr + width not in list:
                    list.append(curr + width)
                    curr_val = f_value[curr] + 1
                    if curr_val < f_value[curr + width]:
                        f_value[curr + width] = curr_val
                        t_value[curr + width] = f_value[curr + width] + distance((curr + width) % width, (curr + width) / width, endX, endY)
                        parent_Position[curr + width] = curr


    step_cost = 0
    #Generate solution path
    position = end_Position
    while parent_Position[position] != start_Position:
        coordinate = parent_Position[position]
        maze[coordinate / width][coordinate % width] = '.'
        position = parent_Position[position]
        step_cost += 1

    #Convert to String
    result = ""
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            result = result + maze[i][j]
        result = result + '\n'

    #Print the solution
    print(result)

    cost = [step_cost, node_expanded]
    return cost

###########################################

#Initialize maze
width = 0
height = 0
infile = open('open.txt', 'r')
for line in infile:
    width = len(line)
    height = height + 1

maze = [[0 for x in range(width)] for y in range(height)]
infile = open('open.txt', 'r')
w = 0
h = 0
for line in infile:
    w = 0
    for c in line:
        if w < width:
            maze[h][w] = c
        w += 1
    h += 1

#Call function
cost = findPath(maze)

#number of steps
print(cost[0])

#number of node expanded
print(cost[1])

###########################################
