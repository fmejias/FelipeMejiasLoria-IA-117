import copy
from random import shuffle

class StateMachine:
    def __init__(self):
        self.cityGraph = []
        self.taxisPosition = []
        self.actualPositions = []
        self.newPositions = []
        self.lastMovement = []
        
    def generateMovements(self, taxisPosition, cityGraph, taxiController):
        self.cityGraph = cityGraph
        self.taxisPosition = copy.deepcopy(taxisPosition)
        self.actualPositions = [item[1] for item in self.taxisPosition]
        canMove = False
        newPositions = []
        newCoordinate = []

        for i in range(0, len(self.taxisPosition)):
            taxiCoordinates = self.actualPositions[i]
            taxiFromTaxiController = taxiController.returnTaxi(self.taxisPosition[i][0])
            taxiHaveClient = taxiFromTaxiController.getWithClient()
            taxiRoad = taxiFromTaxiController.getRoadWithClient()
            if(taxiRoad == []):
                taxiHaveClient = False
                taxiFromTaxiController.setWithNoClient()

            self.newPositions = self.calculatePossibleMovements(taxiCoordinates,
                                                                self.taxisPosition[i][0],
                                                                taxiRoad, taxiHaveClient)

            for j in range(0, len(self.newPositions)):
                newCoordinate = self.newPositions[j]
                isCoordinateInOldPositions = newCoordinate[1] in self.actualPositions
                isCoordinateInNewPositions = newCoordinate[1] in newPositions
                if(isCoordinateInOldPositions == False and isCoordinateInNewPositions == False):
                    self.taxisPosition[i][1] = newCoordinate[1] 
                    newPositions.append(newCoordinate[1])
                    break

            if(len(self.lastMovement) < len(self.taxisPosition)):            
                self.lastMovement.append([self.taxisPosition[i][0], newCoordinate[0]])
            else:
                for k in range(0,len(self.lastMovement)):
                    if(self.lastMovement[k][0] == self.taxisPosition[i][0]):
                        self.lastMovement[k] = [self.taxisPosition[i][0], newCoordinate[0]]
                        break
                    
        return self.taxisPosition
                    
    def calculatePossibleMovements(self,coordinates, taxiId, road, haveClient):
        x = coordinates[0]
        y = coordinates[1]
        possibleMovements = []
        lastMove = self.getLastMovement(taxiId) 
        numberOfMoves = 0

        if(haveClient == False):
            if(lastMove == ""):
                if(self.cityGraph[x][y-1].getNodeValue() == " "):  
                    possibleMovements.append(["left", [x,y-1]])
                if(self.cityGraph[x-1][y].getNodeValue() == " "):  
                    possibleMovements.append(["up", [x-1,y]])
                if(self.cityGraph[x][y+1].getNodeValue() == " "): 
                    possibleMovements.append(["right", [x,y+1]])
                if(self.cityGraph[x+1][y].getNodeValue() == " "):  
                    possibleMovements.append(["down", [x+1,y]])

            else:
                if(lastMove == "left"):
                    if(self.cityGraph[x][y-1].getNodeValue() == " "):  
                        possibleMovements.append(["left", [x,y-1]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x-1][y].getNodeValue() == " "): 
                        possibleMovements.append(["up", [x-1,y]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x+1][y].getNodeValue() == " "): 
                        possibleMovements.append(["down", [x+1,y]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x][y+1].getNodeValue() == " "): 
                        if(numberOfMoves ==3 or numberOfMoves == 2):
                            shuffle(possibleMovements)
                        possibleMovements.append(["right", [x,y+1]])
                    
                elif(lastMove == "right"):
                    if(self.cityGraph[x][y+1].getNodeValue() == " "):  
                        possibleMovements.append(["right", [x,y+1]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x-1][y].getNodeValue() == " "): 
                        possibleMovements.append(["up", [x-1,y]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x+1][y].getNodeValue() == " "): 
                        possibleMovements.append(["down", [x+1,y]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x][y-1].getNodeValue() == " "): 
                        if(numberOfMoves ==3 or numberOfMoves == 2):
                            shuffle(possibleMovements)
                        possibleMovements.append(["left", [x,y-1]])
                        
                elif(lastMove == "down"):
                    if(self.cityGraph[x+1][y].getNodeValue() == " "): 
                        possibleMovements.append(["down", [x+1,y]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x][y+1].getNodeValue() == " "): 
                        possibleMovements.append(["right", [x,y+1]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x][y-1].getNodeValue() == " "): 
                        possibleMovements.append(["left", [x,y-1]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x-1][y].getNodeValue() == " "): 
                        if(numberOfMoves ==3 or numberOfMoves == 2):
                            shuffle(possibleMovements)
                        possibleMovements.append(["up", [x-1,y]])

                else:
                    if(self.cityGraph[x-1][y].getNodeValue() == " "):  
                        possibleMovements.append(["up", [x-1,y]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x][y+1].getNodeValue() == " "):  
                        possibleMovements.append(["right", [x,y+1]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x][y-1].getNodeValue() == " "): 
                        possibleMovements.append(["left", [x,y-1]])
                        numberOfMoves = numberOfMoves + 1
                    if(self.cityGraph[x+1][y].getNodeValue() == " "): 
                        if(numberOfMoves ==3 or numberOfMoves == 2):
                            shuffle(possibleMovements)
                        possibleMovements.append(["down", [x+1,y]])

        else:
            possibleMovements.append(["right", [road[0][0],road[0][1]]]) 
            del road[0]

        return possibleMovements

    def getLastMovement(self,taxiId):
        lastMove = ""
        for i in range(0, len(self.lastMovement)):
            if(self.lastMovement[i][0] == taxiId):
                lastMove = self.lastMovement[i][1]
                break
        return lastMove
    
