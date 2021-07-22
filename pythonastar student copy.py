from os import system, name
import numpy as np
import turtle
import time
from random import randrange
from PIL import Image
from typing import NamedTuple
array = np.random.randint(1,2, size=(30, 30))

class Move(NamedTuple):
    Y: int
    X: int
    

startx = randrange(30)
starty = randrange(30)


endx = 0
endy = 0
pos = Move(starty, startx)

MoveArray = [Move(-1,0),
             Move(-1,1),
             Move(0,1),
             Move(1,1),
             Move(1,0),
             Move(1,-1),
             Move(0,-1),
             Move(-1,-1)]

array[starty,startx] = 0




i = 0
while(i < 200):
    move = randrange(7)
    if (pos.Y + MoveArray[move].Y >= 0 and pos.Y + MoveArray[move].Y  < 30 ):
            if (pos.X + MoveArray[move].X >= 0 and pos.X + MoveArray[move].X < 30 ):
        
                if (array[pos.Y + MoveArray[move].Y, pos.X + MoveArray[move].X] == 1):
                    num = 0
                    for y in range(7):
                        if (pos.Y + MoveArray[move].Y + MoveArray[y].Y >= 0 and pos.Y + MoveArray[move].Y + MoveArray[y].Y  < 30 ):
                            if (pos.X + MoveArray[move].X + MoveArray[y].X >= 0 and pos.X + MoveArray[move].X + MoveArray[y].X  < 30 ):
                                if (array[(pos.Y + MoveArray[move].Y + MoveArray[y].Y), (pos.X + MoveArray[move].X + MoveArray[y].X)] == 0):
                                    num = num + 1
                    if(num <= 1):        
                        array[pos.Y + MoveArray[move].Y, pos.X + MoveArray[move].X] = 0
                        pos = Move((pos.Y + MoveArray[move].Y), (pos.X + MoveArray[move].X))
        
    
    if(i == 199):
        array[pos.Y, pos.X] = 0
        endx = pos.X
        endy = pos.Y

    i = i+1

w, h = 600, 600
data = np.zeros((h, w, 3), dtype=np.uint8)
for y in range(30):
    for x in range(30):
        if (array[y,x] == 1):
            rand = randrange(2)
            if(rand == 1):
                array[y,x] = 0
                

for y in range(30):
    for x in range(30):
        if (y == starty and x == startx):
            for a in range(20):
                   for b in range(20):
                       data[y*20 +b,x*20 +a] = [0,255,0]
        elif (y == endy and x == endx):
            for a in range(20):
                   for b in range(20):
                       data[y*20 +b,x*20 +a] = [255,0,0]
        elif (array[y,x] == 0):
               for a in range(20):
                   for b in range(20):
                       data[y*20 +b,x*20 +a] = [255,255,255]
                

                
img = Image.fromarray(data, 'RGB')
img.save('my.png')
print(startx)
print(starty)
turtle.penup()
turtle.goto((startx - 15) * 20 +10, (-1*starty+15) * 20 -10)
turtle.showturtle()
turtle.shape("turtle")
# load the appropriate image
turtle.pendown()
turtle.bgpic('my.png')
turtle.penup()
turtle.colormode(255)
turtle.pencolor((0,0,255))
turtle.pendown()






class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both the open and closed list arrays
      ### ENTER your open_list code here
    open_list = []
	  ### ENTER your closed_list code here
    closed_list = []
    

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        

        # Generate children
        children = []
        for new_position in [(-1,0),
             (-1,1),
             (0,1),
             (1,1),
             (1,0),
             (1,-1),
             (0,-1),
             (-1,-1)]: 

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            
           
            
            
                    
            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                
                continue
                 

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)
            
            
        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            
            

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
            
            



def main():
          
    maze = array

    start = (starty,startx) 
    end = (endy,endx)    

    path = astar(maze, start, end)
    print(path)
    for f in path:
        turtle.goto((f[1] - 15) * 20 +10, (-1*f[0]+15) * 20 -10)


if __name__ == '__main__':
    main()
