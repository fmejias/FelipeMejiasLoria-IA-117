#!/usr/bin/python

# Head ends here
def next_move(posr, posc, board):
    n = 5 #Grid size: NxN
    
    
    ###Here we start with the definition of the routes 
    if((posr == 0 and posc == 0) or (posr == 0 and posc == n-1)):
        if(posc == 0):
            if(board[posr][posc] == "d"):
                print("CLEAN")
            elif(board[posr + 1][posc] == "d"):
                print("DOWN")
            elif(board[posr][posc + 1] == "d"):
                print("RIGHT")
            else:
                print("DOWN")
        else:
            if(board[posr][posc] == "d"):
                print("CLEAN")
            elif(board[posr + 1][posc] == "d"):
                print("DOWN")
            elif(board[posr][posc - 1] == "d"):
                print("LEFT")
            else:
                print("LEFT")
            
    elif((posr == n - 1 and posc == 0) or (posr == n - 1 and posc == n-1)):
        if(posc == 0):
            if(board[posr][posc] == "d"):
                print("CLEAN")
            elif(board[posr - 1][posc] == "d"):
                print("UP")
            elif(board[posr][posc + 1] == "d"):
                print("RIGHT")
            else:
                print("RIGHT")
        else:
            if(board[posr][posc] == "d"):
                print("CLEAN")
            elif(board[posr - 1][posc] == "d"):
                print("UP")
            elif(board[posr][posc - 1] == "d"):
                print("LEFT")
            else:
                print("UP")

    
    elif(posr == 0 and (posc > 0 and posc < n-1)):
        if(board[posr][posc] == "d"):
            print("CLEAN")
        elif(board[posr][posc - 1] == "d"):
            print("LEFT")
        elif(board[posr][posc + 1] == "d"):
            print("RIGHT")
        elif(board[posr+1][posc] == "d"):
            print("DOWN")
        else:
            print("LEFT")

    elif(posr == n - 1 and (posc > 0 and posc < n-1) ):
        if(board[posr][posc] == "d"):
            print("CLEAN")
        elif(board[posr][posc - 1] == "d"):
            print("LEFT")
        elif(board[posr][posc + 1] == "d"):
            print("RIGHT")
        elif(board[posr-1][posc] == "d"):
            print("UP")
        else:
            print("RIGHT")
       
    elif(posc == 0 and (posr > 0 and posr < n-1)):
        if(board[posr][posc] == "d"):
            print("CLEAN")
        elif(board[posr - 1][posc] == "d"):
            print("UP")
        elif(board[posr + 1][posc] == "d"):
            print("DOWN")
        elif(board[posr][posc+1] == "d"):
            print("RIGHT")
        else:
            print("DOWN")
               
    elif(posc == n - 1 and (posr > 0 and posr < n-1)):
        if(board[posr][posc] == "d"):
            print("CLEAN")
        elif(board[posr-1][posc] == "d"):
            print("UP")
        elif(board[posr+1][posc] == "d"):
            print("DOWN")
        elif(board[posr][posc-1] == "d"):
            print("LEFT")
        else:
            print("UP")
                
    else: 
        if(board[posr][posc] == "d"):
            print("CLEAN")
        elif(board[posr - 1][posc] == "d"):
            print("UP")
        elif(board[posr][posc - 1] == "d"):
            print("LEFT")
        elif(board[posr][posc + 1] == "d"):
            print("RIGHT")
        elif(board[posr + 1][posc] == "d"):
            print("DOWN")
        else: #Default route
            print("RIGHT")

# Tail starts here
if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)