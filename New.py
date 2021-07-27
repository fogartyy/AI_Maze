
from os import system, name
import numpy as np
import turtle
import time
import math
import imageio

from numpy.core.fromnumeric import size
from perlin_numpy import (
    generate_perlin_noise_2d, generate_fractal_noise_2d
)


from random import randrange
from PIL import Image, ImageOps
from typing import NamedTuple
sizemap = 1024
val = sizemap/2
scale = 4
color = False
np.random.seed()
noise = generate_fractal_noise_2d((sizemap, sizemap),(int(val), int(val)))
np.random.seed()
anoise = generate_perlin_noise_2d((sizemap,sizemap),(int(val),int(val)))
np.random.seed()
bnoise = generate_perlin_noise_2d((sizemap,sizemap),(int(val),int(val)))

np.random.seed()
mask = generate_perlin_noise_2d((sizemap,sizemap),(int(val/2),int(val/2)))

for a in range(sizemap):
    for b in range(sizemap):
        if(mask[a,b] < 0):
            diss = math.sqrt(pow(a-b, 2) +pow(sizemap/2 - sizemap/2, 2))
            noise[a,b] = noise[a,b] - anoise[a,b] + bnoise[a,b] 
        else:
            noise[a,b] = noise[a,b] - anoise[a,b] - bnoise[a,b]


print(noise)
for x in range(sizemap):
    for y in range(sizemap):
        if noise[x,y] >= -0.3:
            noise[x,y] = 0
        else:
            noise[x,y] = 1
print(noise)

array = np.random.randint(1,2, size=(sizemap, sizemap))

class Move(NamedTuple):
    Y: int
    X: int
    

startx = sizemap-1
starty = sizemap-1


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
array[endx,endy] = 0




i = 0


w, h = sizemap*scale, sizemap*scale
data = np.zeros((h, w, 3), dtype=np.uint8)
for y in range(sizemap):
    for x in range(sizemap):
                array[y,x] = noise[x,y]
                

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

turtle.goto((startx - sizemap/2) * scale +scale / 2, (-1*starty+sizemap/2) * scale -scale / 2)
t.goto((startx - sizemap/2) * scale +scale / 2, (-1*starty+sizemap/2) * scale -scale / 2)
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



class Node:
    """
        A node class for A* Pathfinding
        parent is parent of the current Node
        position is current position of the Node in the maze
        g is cost from start to current Node
        h is heuristic based estimated cost for current Node to end Node
        f is total cost of present node i.e. :  f = g + h
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

#This function return the path of the 
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate
@static_vars(r=250)
@static_vars(g=0)
@static_vars(b=0)
def color():
    color.r += 5

    if color.r == 255:
        color.r = 0
        color.g += 5
        if color.g == 255:
            color.g = 0
            color.b += 5
    return [color.r,color.g,color.b]

def return_path(current_node,vis,data):
    print(len(vis))
    num = 0
    for l in vis:
        datas = data
        c = color()
        imgs = []

        while l is not None:
            g = l.position[0]
            m = l.position[1]
            for a in range(scale):
                for b in range(scale):
                    datas[g*scale +b,m*scale +a] = [c[0],c[1],c[2]]
                    
                    
            l = l.parent
            
        datas = datas[::-1]
        num += 1
        i = Image.fromarray(datas, 'RGB')
        i = ImageOps.flip(i)
        imgs.append(i)
        img.save('out.gif', save_all=True, append_images=imgs)

    path = []
    
    
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # Return reversed path as we need to show from start to end path
    path = path[::-1]
    
    return path



def search(maze, cost, start, end):
    """
        Returns a list of tuples as a path from the given start to the given end in the given maze
        :param maze:
        :param cost
        :param start:
        :param end:
        :return:
    """

    # Create start and end node with initized values for g, h and f
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both yet_to_visit and visited list
    # in this list we will put all node that are yet_to_visit for exploration. 
    # From here we will find the lowest cost node to expand next
    yet_to_visit_list = []  
    # in this list we will put all node those already explored so that we don't explore it again
    visited_list = [] 
    
    # Add the start node
    yet_to_visit_list.append(start_node)
    
    # Adding a stop condition. This is to avoid any infinite loop and stop 
    # execution after some reasonable number of steps
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    # what squares do we search . serarch movement is left-right-top-bottom 
    #(4 movements) from every positon

    move  =  [[-1,0],
              [-1,1],
              [0,1],
              [1,1],
              [1,0],
              [1,-1],
              [0,-1],
              [-1,-1]]


    """
        1) We first get the current node by comparing all f cost and selecting the lowest cost node for further expansion
        2) Check max iteration reached or not . Set a message and stop execution
        3) Remove the selected node from yet_to_visit list and add this node to visited list
        4) Perofmr Goal test and return the path else perform below steps
        5) For selected node find out all children (use move to find children)
            a) get the current postion for the selected node (this becomes parent node for the children)
            b) check if a valid position exist (boundary will make few nodes invalid)
            c) if any node is a wall then ignore that
            d) add to valid children node list for the selected parent
            
            For all the children node
                a) if child in visited list then ignore it and try next node
                b) calculate child node g, h and f values
                c) if child in yet_to_visit list then ignore it
                d) else move the child to yet_to_visit list
    """
    #find maze has got how many rows and columns 
    no_rows, no_columns = np.shape(maze)
    
    # Loop until you find the end
    
    while len(yet_to_visit_list) > 0:
        
        # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
        outer_iterations += 1    

        
        # Get the current node
        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        # if we hit this point return the path such as it may be no solution or 
        # computation cost is too high
        if outer_iterations > max_iterations:
            print ("giving up on pathfinding too many iterations")
            return return_path(current_node,visited_list,data)

        # Pop current node out off yet_to_visit list, add to visited list
        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        # test if goal is reached or not, if yes then return the path
        if current_node == end_node:
            return return_path(current_node, visited_list,data)

        # Generate children from all adjacent squares
        children = []

        for new_position in move: 

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if(color == True):
                if maze[node_position[0]][node_position[1]] == 0:
                    t.pencolor((0,255,0))
                elif maze[node_position[0]][node_position[1]] == 1:
                    t.pencolor((255,0,0))
                t.goto((node_position[1] - sizemap/2) * scale + scale / 2, (-1*node_position[0]+sizemap/2) * scale - scale / 2)

            # Make sure within range (check if within maze boundary)
            if (node_position[0] > (no_rows - 1) or 
                node_position[0] < 0 or 
                node_position[1] > (no_columns -1) or 
                node_position[1] < 0):
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
            
            # Child is on the visited list (search entire visited list)
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + cost
            ## Heuristic costs calculated here, this is using eucledian distance
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                       ((child.position[1] - end_node.position[1]) ** 2)) 

            child.f = child.g + child.h

            # Child is already in the yet_to_visit list and g cost is already lower
            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            # Add the child to the yet_to_visit list
            yet_to_visit_list.append(child)


if __name__ == '__main__':

    maze = array
    
    start = [startx, starty] # starting position
    end = [endx,endy] # ending position
    cost = 1 # cost per movement

    path = search(maze,cost, start, end)
    print(path)
    for f in path:
        turtle.goto((f[1] - sizemap/2) * scale +scale / 2, (-1*f[0]+sizemap/2) * scale -scale / 2)

    hello = input("")