import numpy as np
from utilities import prepareMaze, drawPath, getPosition
import copy
def findbox(maze):
    width = len(maze[0])
    height = len(maze)
    ret=[]
    for i in range(height):
        for j in range(width):
            if maze[i][j]== 'b' or maze[i][j]=='B':
                ret.append(i*width+j)
    return ret

def manhatten(a,b,maze):
    width = len(maze[0])
    curra1= a/width
    curra2= a%width
    currb1= b/width
    currb2= b%width
    return abs(curra1-currb1)+abs(curra2-currb2)



def smallestf(queue):
    ret=0
    value=9999
    for a in range(len(queue)):
        if hue(queue[a])<value:
            value=hue(queue[a])
            ret=a
    return ret

def hue(maze):
    boxes=findbox(maze)
    dots=finddest(maze)
    ret=0
    for b in boxes:
        index=0
        value=999
        for d in dots:
            if manhatten(b,d,maze)<value:
                value=manhatten(b,d,maze)
        ret+=value


    return ret


def printmaze(maze):
    result = ''
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            result = result + maze[i][j]
        result = result + '\n'

    print(result)
    return result

def stringmaze(maze):
    result = ''
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            result = result + maze[i][j]
        result = result + '\n'
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

def findp(maze):
    width = len(maze[0])
    height = len(maze)
    ret=0
    for i in range(height):
        for j in range(width):
            if maze[i][j]== 'P':
                ret=i*width+j
    return ret

def solve(maze):
    length=0
    closedSet=[]
    dots=finddest(maze)
    openSet = [maze]
    lengthopenSet = [0]
    visited = []
    printmaze(maze)
    while len(openSet) != 0:
        length+=1
        index=smallestf(openSet)
        cost=lengthopenSet[index]
        lengthopenSet.pop(index)
        currmaze=openSet[index]
        openSet.pop(index)
        closedSet.append(currmaze)
        if end(currmaze):
            print('Success')
            printmaze(currmaze)
            print(length)
            print(cost)
            return currmaze
        #printmaze(currmaze)

        for d in range(4):
            mazecopy=copy.deepcopy(currmaze)
            original= findp(mazecopy)
            if move(mazecopy, findp(mazecopy), d, dots):
                if mazecopy in closedSet:
                    continue
                if mazecopy not in openSet:
                    openSet.append(mazecopy)
                    lengthopenSet.append(cost+1)
                tentative_gScore=hue(currmaze)+1
                if tentative_gScore>=hue(mazecopy):
                    continue















if __name__ == '__main__':
    result = ''
    maze = prepareMaze('t3.txt')
    solve(maze)
