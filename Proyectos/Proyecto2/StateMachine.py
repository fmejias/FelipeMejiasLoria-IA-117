###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################

import copy

###########################################################################################################
# StateMachine Class:
# Attributes:
# 1-) 
##########################################################################################################

class StateMachine:
    def __init__(self):
        self.cityGraph = []
        self.taxisPosition = []
        self.actualPositions = []
        self.newPositions = []
        self.lastMovement = [] #Format of the list = [["A", "up"]]

    #This method is in charge of generate the movements for all of the autonoumous taxis
    def generateMovements(self, taxisPosition, cityGraph):

        #Set the graph and the list with the positions
        self.cityGraph = cityGraph
        self.taxisPosition = copy.deepcopy(taxisPosition)

        #Extract only the coordinates x and y
        self.actualPositions = [item[1] for item in self.taxisPosition]

        #This variable indicates if the taxi cant move
        canMove = False

        #This array is to compare if a new movement is already taken
        newPositions = []
        newCoordinate = []

        #Iterate for all of the taxis
        for i in range(0, len(self.taxisPosition)):

            #Extract the coordinates for the taxi
            taxiCoordinates = self.actualPositions[i]
            
            #Calculate the possible movements for that taxi
            self.newPositions = self.calculatePossibleMovements(taxiCoordinates, self.taxisPosition[i][0])

            #Check if there is one path to go
            for j in range(0, len(self.newPositions)):

                #Extract an item coordinate
                newCoordinate = self.newPositions[j]

                #Check if the item is in the old positions or in the new positions
                isCoordinateInOldPositions = newCoordinate[1] in self.actualPositions
                isCoordinateInNewPositions = newCoordinate[1] in newPositions

                #See if it has to append the new coordinate
                if(isCoordinateInOldPositions == False and isCoordinateInNewPositions == False):
                    self.taxisPosition[i][1] = newCoordinate[1] #Update the new coordinate
                    newPositions.append(newCoordinate[1])
                    break

            if(len(self.lastMovement) < len(self.taxisPosition)):            
                #Append the last movement of the taxi
                self.lastMovement.append([self.taxisPosition[i][0], newCoordinate[0]])
            else:
                for k in range(0,len(self.lastMovement)):
                    if(self.lastMovement[k][0] == self.taxisPosition[i][0]):
                        self.lastMovement[k] = [self.taxisPosition[i][0], newCoordinate[0]]
                        break

        #Return the list with the new positions [Nuevas, Viejas]
        return self.taxisPosition
                    
    #This method calculates the possible movements
    def calculatePossibleMovements(self,coordinates, taxiId):

        #Get the x and y coordinates
        x = coordinates[0]
        y = coordinates[1]

        #List to save all of the movements
        possibleMovements = []

        #First move of all the taxis
        lastMove = self.getLastMovement(taxiId) #last movement of the taxi
        
        if(lastMove == ""):
            #Check possible movements
            if(self.cityGraph[x][y-1].getNodeValue() == " "):  #Left
                possibleMovements.append(["left", [x,y-1]])
            if(self.cityGraph[x-1][y].getNodeValue() == " "):  #Up
                possibleMovements.append(["up", [x-1,y]])
            if(self.cityGraph[x][y+1].getNodeValue() == " "):  #Right
                possibleMovements.append(["right", [x,y+1]])
            if(self.cityGraph[x+1][y].getNodeValue() == " "):  #Down
                possibleMovements.append(["down", [x+1,y]])

        #After the first movement
        else:
            
            if(lastMove == "left"):
                #Check possible movements
                if(self.cityGraph[x][y-1].getNodeValue() == " "):  #Left
                    possibleMovements.append(["left", [x,y-1]])
                if(self.cityGraph[x-1][y].getNodeValue() == " "):  #Up
                    possibleMovements.append(["up", [x-1,y]])
                if(self.cityGraph[x+1][y].getNodeValue() == " "):  #Down
                    possibleMovements.append(["down", [x+1,y]])
                if(self.cityGraph[x][y+1].getNodeValue() == " "):  #Right
                    possibleMovements.append(["right", [x,y+1]])
                
            elif(lastMove == "right"):
                #Check possible movements
                if(self.cityGraph[x][y+1].getNodeValue() == " "):  #Right
                    possibleMovements.append(["right", [x,y+1]])
                if(self.cityGraph[x-1][y].getNodeValue() == " "):  #Up
                    possibleMovements.append(["up", [x-1,y]])
                if(self.cityGraph[x+1][y].getNodeValue() == " "):  #Down
                    possibleMovements.append(["down", [x+1,y]])
                if(self.cityGraph[x][y-1].getNodeValue() == " "):  #Left
                    possibleMovements.append(["left", [x,y-1]])
                    
            elif(lastMove == "down"):
                #Check possible movements
                if(self.cityGraph[x+1][y].getNodeValue() == " "):  #Down
                    possibleMovements.append(["down", [x+1,y]])
                if(self.cityGraph[x][y+1].getNodeValue() == " "):  #Right
                    possibleMovements.append(["right", [x,y+1]])
                if(self.cityGraph[x][y-1].getNodeValue() == " "):  #Left
                    possibleMovements.append(["left", [x,y-1]])
                if(self.cityGraph[x-1][y].getNodeValue() == " "):  #Up
                    possibleMovements.append(["up", [x-1,y]])

            else:
                #Check possible movements
                if(self.cityGraph[x-1][y].getNodeValue() == " "):  #Up
                    possibleMovements.append(["up", [x-1,y]])
                if(self.cityGraph[x][y+1].getNodeValue() == " "):  #Right
                    possibleMovements.append(["right", [x,y+1]])
                if(self.cityGraph[x][y-1].getNodeValue() == " "):  #Left
                    possibleMovements.append(["left", [x,y-1]])
                if(self.cityGraph[x+1][y].getNodeValue() == " "):  #Down
                    possibleMovements.append(["down", [x+1,y]])
            
        #Return the list with the possible movements
        return possibleMovements

    #This method returns the last movement of the taxi
    def getLastMovement(self,taxiId):
        lastMove = ""
        for i in range(0, len(self.lastMovement)):
            if(self.lastMovement[i][0] == taxiId):
                lastMove = self.lastMovement[i][1]
                break
        return lastMove
    
