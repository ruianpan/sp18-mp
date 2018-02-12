import numpy as np
from utilities import prepareMaze, drawPath, getPosition
import copy



def findp(maze):
    width = len(maze[0])
    height = len(maze)
    ret=0
    for i in range(height):
        for j in range(width):
            if maze[i][j]== 'P':
                ret=i*width+j
    return ret

def printmaze(maze):
    result = ''
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            result = result + maze[i][j]
        result = result + '\n'

    print(result)
    return result




def end(maze):
    width = len(maze[0])
    height = len(maze)
    for i in range(height):
        for j in range(width):
            if maze[i][j]== 'b':
                return 0
    return 1

def move(maze, a, d, dots):
    width = len(maze[0])
    height = len(maze)
    if d==0:                #left
        if maze[a/width][a%width-1] ==' ' or maze[a/width][a%width-1] =='.':          #left side is space
            maze[a/width][a%width-1] = 'P'
            if a in dots:
                maze[a/width][a%width]='.'
            else:
                maze[a/width][a%width]=' '
            return 1
        elif maze[a/width][a%width-1] =='b' or maze[a/width][a%width-1] =='B':
            if maze[a/width][a%width-2] ==' ' or maze[a/width][a%width-2] =='.':     #left box, left two space


                if maze[a/width][a%width-3] == '%' and maze[a/width][a%width-2] !='.':
                    if maze[a/width-1][a%width-2] == '%' or maze[a/width+1][a%width-2] == '%':
                        return 0


                maze[a/width][a%width-1] = 'P'
                if a in dots:
                    maze[a/width][a%width]='.'
                else:
                    maze[a/width][a%width]=' '
                if a-2 in dots:
                    maze[a/width][a%width-2] ='B'
                else:
                    maze[a/width][a%width-2] ='b'
                return 1

    elif d==1:                #right
        if maze[a/width][a%width+1] ==' ' or maze[a/width][a%width+1] =='.':          #right side is space
            maze[a/width][a%width+1] = 'P'
            if a in dots:
                maze[a/width][a%width]='.'
            else:
                maze[a/width][a%width]=' '
            return 1
        elif maze[a/width][a%width+1] =='b' or maze[a/width][a%width+1] =='B':
            if maze[a/width][a%width+2] ==' ' or maze[a/width][a%width+2] =='.':


                if maze[a/width][a%width+3] == '%' and maze[a/width][a%width+2] !='.':
                    if maze[a/width-1][a%width+2] == '%' or maze[a/width+1][a%width+2] == '%':
                        return 0


                maze[a/width][a%width+1] = 'P'
                if a in dots:
                    maze[a/width][a%width]='.'
                else:
                    maze[a/width][a%width]=' '
                if a+2 in dots:
                    maze[a/width][a%width+2] ='B'
                else:
                    maze[a/width][a%width+2] ='b'
                return 1




    elif d==2:                #up
        if maze[a/width-1][a%width] ==' ' or maze[a/width-1][a%width] =='.':          #left side is space
            maze[a/width-1][a%width] = 'P'
            if a in dots:
                maze[a/width][a%width]='.'
            else:
                maze[a/width][a%width]=' '
            return 1
        elif maze[a/width-1][a%width] =='b' or maze[a/width-1][a%width] =='B':
            if maze[a/width-2][a%width] ==' ' or maze[a/width-2][a%width] =='.':


                if maze[a/width-3][a%width] == '%' and maze[a/width-2][a%width] !='.':
                    if maze[a/width-2][a%width-1] == '%' or maze[a/width-2][a%width+1] == '%':
                        return 0


                maze[a/width-1][a%width] = 'P'
                if a in dots:
                    maze[a/width][a%width]='.'
                else:
                    maze[a/width][a%width]=' '
                if a-2*width in dots:
                    maze[a/width-2][a%width] ='B'
                else:
                    maze[a/width-2][a%width] ='b'
                return 1




    elif d==3:                #down
        if maze[a/width+1][a%width] ==' ' or maze[a/width+1][a%width] =='.':          #left side is space
            maze[a/width+1][a%width] = 'P'
            if a in dots:
                maze[a/width][a%width]='.'
            else:
                maze[a/width][a%width]=' '
            return 1
        elif maze[a/width+1][a%width] =='b' or maze[a/width+1][a%width] =='B':
            if maze[a/width+2][a%width] ==' ' or maze[a/width+2][a%width] =='.':


                if maze[a/width+3][a%width] == '%' and maze[a/width+2][a%width] !='.':
                    if maze[a/width+2][a%width-1] == '%' or maze[a/width+2][a%width+1] == '%':
                        return 0


                maze[a/width+1][a%width] = 'P'
                if a in dots:
                    maze[a/width][a%width]='.'
                else:
                    maze[a/width][a%width]=' '
                if a+2*width in dots:
                    maze[a/width+2][a%width] ='B'
                else:
                    maze[a/width+2][a%width] ='b'
                return 1
    return 0

def finddest(maze):
    width = len(maze[0])
    height = len(maze)
    ret=[]
    for i in range(height):
        for j in range(width):
            if maze[i][j]== '.' or maze[i][j]=='B':
                ret.append(i*width+j)
    return ret



def solve(maze):
    width = len(maze[0])
    height = len(maze)


    dots=finddest(maze)
    queue = []
    lengthqueue = []
    visited = [maze]
    queue.append(maze)
    lengthqueue.append(0)
    printmaze(maze)
    length=0
    while len(queue) != 0:
        cost=lengthqueue[0]
        lengthqueue.pop(0)
        length+=1
        currmaze=queue[0]
        queue.pop(0)
        #printmaze(currmaze)
        if end(currmaze):
            print('Success')
            printmaze(currmaze)
            print(cost)
            print(length)
            return currmaze
        for d in range(4):
            mazecopy=copy.deepcopy(currmaze)
            original= findp(mazecopy)
            if move(mazecopy, findp(mazecopy), d, dots):

                if mazecopy not in visited:
                    visited.append(mazecopy)
                    queue.append(mazecopy)
                    lengthqueue.append(cost+1)















if __name__ == '__main__':
    result = ''
    maze = prepareMaze('t3.txt')
    solve(maze)
