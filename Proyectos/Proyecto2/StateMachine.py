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

        #Iterate for all of the taxis
        for i in range(0, len(self.taxisPosition)):

            #Extract the coordinates for the taxi
            taxiCoordinates = self.actualPositions[i]
            
            #Calculate the possible movements for that taxi
            self.newPositions = self.calculatePossibleMovements(taxiCoordinates)

            #Check if there is one path to go
            for j in range(0, len(self.newPositions)):

                #Extract an item
                newCoordinate = self.newPositions[j]

                #Check if the item is in the old positions or in the new positions
                isCoordinateInOldPositions = newCoordinate in self.actualPositions
                isCoordinateInNewPositions = newCoordinate in newPositions

                #See if it has to append the new coordinate
                if(isCoordinateInOldPositions == False and isCoordinateInNewPositions == False):
                    self.taxisPosition[i][1] = newCoordinate #Update the new coordinate
                    newPositions.append(newCoordinate)
                    break

        #Return the list with the new positions [Nuevas, Viejas]
        return self.taxisPosition
                    
    #This method calculates the possible movements
    def calculatePossibleMovements(self,coordinates):

        #Get the x and y coordinates
        x = coordinates[0]
        y = coordinates[1]

        #List to save all of the movements
        possibleMovements = []

        #Check possible movements
        if(self.cityGraph[x-1][y].getNodeValue() == " "):  #Up
            possibleMovements.append([x-1,y])
        if(self.cityGraph[x+1][y].getNodeValue() == " "):  #Down
            possibleMovements.append([x+1,y])
        if(self.cityGraph[x][y-1].getNodeValue() == " "):  #Left
            possibleMovements.append([x,y-1])
        if(self.cityGraph[x][y+1].getNodeValue() == " "):  #Right
            possibleMovements.append([x,y+1])

        #Return the list with the possible movements
        return possibleMovements
    
