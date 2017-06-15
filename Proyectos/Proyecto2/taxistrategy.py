import copy
import types
from random import shuffle
import abc

class Strategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def calculateMovements(self,coordinates, taxiId, road, haveClient, cityGraph):
        pass

class LastMoveNoneStrategy(Strategy):
    def calculateMovements(self,coordinates, taxiId, road, haveClient, cityGraph):
        possibleMovements = []
        x = coordinates[0]
        y = coordinates[1]
        if(cityGraph[x][y-1].getNodeValue() == " "):  
            possibleMovements.append(["left", [x,y-1]])
        if(cityGraph[x-1][y].getNodeValue() == " "):  
            possibleMovements.append(["up", [x-1,y]])
        if(cityGraph[x][y+1].getNodeValue() == " "): 
            possibleMovements.append(["right", [x,y+1]])
        if(cityGraph[x+1][y].getNodeValue() == " "):  
            possibleMovements.append(["down", [x+1,y]])
        return possibleMovements

class LastMoveLeftStrategy(Strategy):
    def calculateMovements(self,coordinates, taxiId, road, haveClient, cityGraph):
        possibleMovements = []
        numberOfMoves = 0
        x = coordinates[0]
        y = coordinates[1]
        if(cityGraph[x][y-1].getNodeValue() == " "):
            possibleMovements.append(["left", [x,y-1]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x-1][y].getNodeValue() == " "): 
            possibleMovements.append(["up", [x-1,y]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x+1][y].getNodeValue() == " "): 
            possibleMovements.append(["down", [x+1,y]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x][y+1].getNodeValue() == " "): 
            if(numberOfMoves ==3 or numberOfMoves == 2):
                shuffle(possibleMovements)
            possibleMovements.append(["right", [x,y+1]])
        return possibleMovements

class LastMoveRightStrategy(Strategy):
    def calculateMovements(self,coordinates, taxiId, road, haveClient, cityGraph):
        possibleMovements = []
        numberOfMoves = 0
        x = coordinates[0]
        y = coordinates[1]
        if(cityGraph[x][y+1].getNodeValue() == " "):  
            possibleMovements.append(["right", [x,y+1]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x-1][y].getNodeValue() == " "): 
            possibleMovements.append(["up", [x-1,y]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x+1][y].getNodeValue() == " "): 
            possibleMovements.append(["down", [x+1,y]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x][y-1].getNodeValue() == " "): 
            if(numberOfMoves ==3 or numberOfMoves == 2):
                shuffle(possibleMovements)
            possibleMovements.append(["left", [x,y-1]])
        return possibleMovements

class LastMoveUpStrategy(Strategy):
    def calculateMovements(self,coordinates, taxiId, road, haveClient, cityGraph):
        possibleMovements = []
        numberOfMoves = 0
        x = coordinates[0]
        y = coordinates[1]
        if(cityGraph[x-1][y].getNodeValue() == " "):  
            possibleMovements.append(["up", [x-1,y]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x][y+1].getNodeValue() == " "):  
            possibleMovements.append(["right", [x,y+1]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x][y-1].getNodeValue() == " "): 
            possibleMovements.append(["left", [x,y-1]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x+1][y].getNodeValue() == " "): 
            if(numberOfMoves ==3 or numberOfMoves == 2):
                shuffle(possibleMovements)
            possibleMovements.append(["down", [x+1,y]])
        return possibleMovements

class LastMoveDownStrategy(Strategy):
    def calculateMovements(self,coordinates, taxiId, road, haveClient, cityGraph):
        possibleMovements = []
        numberOfMoves = 0
        x = coordinates[0]
        y = coordinates[1]
        if(cityGraph[x+1][y].getNodeValue() == " "): 
            possibleMovements.append(["down", [x+1,y]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x][y+1].getNodeValue() == " "): 
            possibleMovements.append(["right", [x,y+1]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x][y-1].getNodeValue() == " "): 
            possibleMovements.append(["left", [x,y-1]])
            numberOfMoves = numberOfMoves + 1
        if(cityGraph[x-1][y].getNodeValue() == " "): 
            if(numberOfMoves ==3 or numberOfMoves == 2):
                shuffle(possibleMovements)
            possibleMovements.append(["up", [x-1,y]])
        return possibleMovements

class Context:
    def __init__(self):
        self.strategy = 0

    def setStrategy(self, strategy):
        self.strategy = strategy

    def getResult(self, coordinates, taxiId, road, haveClient, cityGraph):
        return self.strategy.calculateMovements(coordinates, taxiId, road, haveClient, cityGraph)

class TaxiStrategy:
    def __init__(self):
        self.cityGraph = []
        self.taxisPosition = []
        self.actualPositions = []
        self.newPositions = []
        self.lastMovement = []
        self.context = Context()
        
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
        possibleMovements = []
        lastMove = self.getLastMovement(taxiId) 
        if(haveClient == False):
            if(lastMove == ""):
                noneStrategy = LastMoveNoneStrategy()
                self.context.setStrategy(noneStrategy)
                possibleMovements = self.context.getResult(coordinates, taxiId, road,
                                                           haveClient, self.cityGraph)
            else:
                if(lastMove == "left"):
                    leftStrategy = LastMoveLeftStrategy()
                    self.context.setStrategy(leftStrategy)
                    possibleMovements = self.context.getResult(coordinates, taxiId, road,
                                                               haveClient, self.cityGraph)
                elif(lastMove == "right"):
                    rightStrategy = LastMoveRightStrategy()
                    self.context.setStrategy(rightStrategy)
                    possibleMovements = self.context.getResult(coordinates, taxiId, road,
                                                               haveClient, self.cityGraph)
                elif(lastMove == "down"):
                    downStrategy = LastMoveDownStrategy()
                    self.context.setStrategy(downStrategy)
                    possibleMovements = self.context.getResult(coordinates, taxiId, road,
                                                               haveClient, self.cityGraph)
                else:
                    upStrategy = LastMoveUpStrategy()
                    self.context.setStrategy(upStrategy)
                    possibleMovements = self.context.getResult(coordinates, taxiId, road,
                                                               haveClient, self.cityGraph)

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
    
