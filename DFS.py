fname=raw_input("name of the mazefile :  ")
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
            if c=='P':
                startw=w
                starth=h
            elif c=='.':
                endw=w
                endh=h
        w+=1
    h+=1

Visited = [[0 for x in range(width)] for y in range(height)]
parent = [[0 for x in range(width)] for y in range(height)]
#ch=sh
#cw=sw
print('startexecution')

s=[]
#Visited[starth][startw]=1
end= endh * width + endw
start = starth * width + startw
s.append(starth*width+startw)
loop=0
while len(s)!=0:
    loop+=1
    curr=s.pop()
    currh=curr/width
    currw=curr%width

    if curr==end:
        print('complete')
        break
    if Visited[currh][currw]==0  :

        Matrix[currh][currw]=='2'
        Visited[currh][currw]=1

        #up
        if currh>0:
            if Visited[currh-1][currw]==0 and Matrix[currh-1][currw] !='%':
                #Visited[currh-1][currw]=1
                s.append( (currh-1) * width + currw )
                parent[currh-1][currw]=curr

        #down
        if currh<height-1:
            if Visited[currh+1][currw]==0 and Matrix[currh+1][currw] !='%':
                #Visited[currh+1][currw]=1
                s.append( (currh+1) * width + currw )
                parent[currh+1][currw]=curr

        #left
        if currw>0:
            if Visited[currh][currw-1]==0 and Matrix[currh][currw-1] !='%':
                #Visited[currh][currw-1]=1
                s.append( (currh) * width + currw-1 )
                parent[currh][currw-1]=curr

        #right
        if currw < width-1:
            if Visited[currh][currw+1]==0 and Matrix[currh][currw+1] !='%':
                #print('right')
                #Visited[currh][currw+1]=1
                s.append( (currh) * width + currw+1 )
                parent[currh][currw+1]=curr
#print(parent[end/width][end%width])
position=end
while position != start:
    Matrix [position/width][position%width]= '.'
    position=parent[position/width][position%width]
a=''
for h in range(height):
    for w in range(width):
        a=a+Matrix[h][w]
    a=a+'\n'
print(a)
