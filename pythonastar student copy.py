from os import system, name
import numpy as np
import turtle
import time
from random import randrange
from PIL import Image
from typing import NamedTuple
sizemap = 100
scale = 10
color = False

array = np.random.randint(1,2, size=(sizemap, sizemap))

class Move(NamedTuple):
    Y: int
    X: int
    

startx = randrange(sizemap)
starty = randrange(sizemap)


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


w, h = sizemap*scale, sizemap*scale
data = np.zeros((h, w, 3), dtype=np.uint8)
for y in range(sizemap):
    for x in range(sizemap):
        if (array[y,x] == 1):
            rand = randrange(3)
            if(rand == 1 or rand == 2):
                array[y,x] = 0
                

for y in range(sizemap):
    for x in range(sizemap):
        if (y == starty and x == startx):
            for a in range(scale):
                for b in range(scale):
                    data[y*scale +b,x*scale +a] = [0,255,0]
        elif (y == endy and x == endx):
            for a in range(scale):
                for b in range(scale):
                    data[y*scale +b,x*scale +a] = [255,0,0]
        elif (array[y,x] == 0):
            for a in range(scale):
                for b in range(scale):
                    data[y*scale +b,x*scale +a] = [255,255,255]
                

                
img = Image.fromarray(data, 'RGB')
img.save('my.png')
print(startx)
print(starty)
turtle.penup()

t = turtle.Turtle()
t.penup()

turtle.goto((startx - sizemap/2) * scale +10, (-1*starty+sizemap/2) * scale -10)
t.goto((startx - sizemap/2) * scale +10, (-1*starty+sizemap/2) * scale -10)
turtle.showturtle()
turtle.shape("turtle")
# load the appropriate image
turtle.pendown()
turtle.bgpic('my.png')
turtle.penup()
turtle.colormode(255)
turtle.pencolor((0,0,255))
turtle.pendown()



t.pendown()
t.pencolor((0,255,0))






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
            if(color == True):
                if maze[node_position[0]][node_position[1]] == 0:
                    t.pencolor((0,255,0))
                elif maze[node_position[0]][node_position[1]] == 1:
                    t.pencolor((255,0,0))
                t.goto((node_position[1] - sizemap/2) * scale +10, (-1*node_position[0]+sizemap/2) * scale -10)

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                
                continue
                

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)
            
            
        # Loop through children
        for child in children:
            print(child.position)
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            print(child.h)
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
        turtle.goto((f[1] - sizemap/2) * scale +10, (-1*f[0]+sizemap/2) * scale -10)


if __name__ == '__main__':
    main()
