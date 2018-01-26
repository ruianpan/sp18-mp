def preparemaze(fname):               # take the file name as input and return the maze matrix
    import numpy as np
    print('preparing the maze')
    infile = open(fname, 'r')
    height = 0
    for line in infile:
        width=len(line)
        height = height + 1
    Matrix = [[0 for x in range(width)] for y in range(height)]
    infile = open(fname,'r')
    w=0
    h=0
    for line in infile:
        w=0
        for c in line:
            if w<width:
                Matrix[h][w]=c
            w+=1
        h+=1
    return Matrix

# code for printing the maze solved
#end is the reached goal
#Matrix is the matrix to change
#parent is the matrix that records the parent of the node
#position=end
#while position != start:
#    Matrix [position/width][position%width]= '.'
#    position=parent[position/width][position%width]
#a=''
#for h in range(height):
#    for w in range(width):
#        a=a+Matrix[h][w]
#    a=a+'\n'
#print(a)