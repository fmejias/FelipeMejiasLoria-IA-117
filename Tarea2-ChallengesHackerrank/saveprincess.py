#!/usr/bin/python
def displayPathtoPrincess(n,grid):
    
    #print all the moves here
    m = int(input())
    grid = [] #Here we define the matrix
    for i in range(0, m): 
        grid.append(input().strip())
    
    #Here we print all the moves of the Bot
    print("DOWN")
    print("LEFT")
    if(grid[2][0] == "p"):
        return "La encontre"
    print("UP")
    print("UP")
    if(grid[0][0] == "p"):
        return "La encontre"
    print("RIGHT")
    print("RIGHT")
    if(grid[0][2] == "p"):
        return "La encontre"
    print("DOWN")
    print("DOWN")
    if(grid[2][2] == "p"):
        return "La encontre"
    
#Here we call the function to display the path to the princess    
displayPathtoPrincess(3, [])