import numpy as np
from random import randrange
from typing import NamedTuple
from PIL import Image
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

array[starty,startx] = 9




i = 0
while(i < 100):
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
        
    
    if(i == 99):
        array[pos.Y, pos.X] = 5
        endx = pos.X
        endy = pos.Y

    i = i+1

for y in range(30):
    for x in range(30):
        if (array[y,x] == 1):
            rand = randrange(3)
            if(rand == 1):
                array[y,x] = 0
        
    
for y in range(30):
    for x in range(30):
        if (array[y,x] == 0):
            print(" ", end=" ")
        elif(array[y,x] == 9):
            print("9", end=" ")
        elif(array[y,x] == 5):
            print("5", end=" ")
        else:
            print(u"\u25A0", end=" ")
    print()
print (repr(array))
print (array)
print(starty, startx)
print (endy, endx)
            
            
