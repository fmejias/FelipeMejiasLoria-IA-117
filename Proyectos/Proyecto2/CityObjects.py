import queue
from random import randint
from operator import itemgetter
import copy

import client

class CityNode:
    def __init__(self,x,y,value,isBlock):
        self.visited = False
        self.adjacentNodesList = []
        self.x = x
        self.y = y
        self.typeOfNode = ""
        self.valueOfNode = value
        self.cost = 0
        self.d = 0
        self.h = 0
        self.father = 0
        self.belongToBlock = ""
        self.client = client.Client()
        self.haveBlockAsNeighbor = False 
        self.haveAClient = False

        self.setTypeAndSetValue(value, isBlock) 

    def setTypeAndSetValue(self,value, isBlock):
        if(value == "|"):
            self.typeOfNode = "wall"
        elif(value == "-"):
            self.typeOfNode = "wall"
        elif(value == "*"):
            self.typeOfNode = "water"
        elif(isBlock == "yes"):
            self.typeOfNode = "block"
        elif(value == " "):
            self.typeOfNode = "street"
        elif(value == "D"):
            self.typeOfNode = "taxi"
    
    def setBlockAsNeighbor(self):
        self.haveBlockAsNeighbor = True

    def getBlockAsNeighbor(self):
        return self.haveBlockAsNeighbor

    def setHaveAClient(self):
        self.haveAClient = True

    def resetHaveAClient(self):
        self.haveAClient = False

    def getHaveAClient(self):
        return self.haveAClient

    def getBlockAsNeighbor(self):
        return self.haveBlockAsNeighbor
    
    def setBlockToWall(self, block):
        self.belongToBlock = block

    def getBlockOfWall(self):
        return self.belongToBlock

    def getClient(self):
        return self.client

    def setInitialBlockToClient(self, initialBlock):
        self.client.setInitialBlock(initialBlock)

    def setDestinationBlockToClient(self, destinationBlock):
        self.client.setDestinationBlock(destinationBlock)

    def getInitialBlockOfTheClient(self):
        return self.client.getInitialBlock()

    def getDestinationBlockOfTheClient(self):
        return self.client.getDestinationBlock()
    
    def getFather(self):
        return self.father

    def setFather(self, father):
        self.father = father
    
    def getCost(self):
        return self.cost

    def setCost(self, cost):
        self.cost = cost

    def getD(self):
        return self.d

    def setD(self, distance):
        self.d = distance

    def getH(self):
        return self.h

    def setH(self, h):
        self.h = h

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def getNodeType(self):
        return self.typeOfNode

    def setNodeType(self, typeOfNode):
        self.typeOfNode = typeOfNode

    def getNodeValue(self):
        return self.valueOfNode

    def setNodeValue(self, valueOfNode):
        self.valueOfNode = valueOfNode

    def isVisited(self):
        return self.visited

    def getAdjacentNodesList(self):
        return self.adjacentNodesList

    def setVisit(self):
        self.visited = True

    def resetVisit(self):
        self.visited = False

    def updateAdjacentList(self, node):
        self.adjacentNodesList.append(node)

class CityGraph:
    def __init__(self, city):
        self.routeTraveled = [] 
        self.routeToTravel = [] 
        self.searchList = []
        self.clientsList = [] 
        self.routesVisited = [] 
        self.actualNode = ""  
        self.destinationNode = ""
        self.cityMatrix = copy.deepcopy(city) 
        self.rows = len(self.cityMatrix) 
        self.columns = len(self.cityMatrix[0]) 
        self.taxiInitialPosition = 0 
        self.taxisPosition = [] 

        self.createCityGraph(len(city),len(city[0]))
        self.numberOfTaxis = self.searchAllTaxis()

    def createCityGraph(self,rows,columns):
        x = 0 
        y = 0 
        while(x < rows):
            while(y < columns):
                node = CityNode(x,y,self.cityMatrix[x][y][1],
                                self.cityMatrix[x][y][0])
                
                if((y == 0) and (x < rows) and (x == 0)): 
                    node.updateAdjacentList((x,y+1)) 
                    node.updateAdjacentList((x+1,y)) 
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == 0) and (x == rows-1)): 
                    node.updateAdjacentList((x-1,y)) 
                    node.updateAdjacentList((x,y+1))
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == 0) and (x < rows)): 
                    node.updateAdjacentList((x-1,y)) 
                    node.updateAdjacentList((x,y+1)) 
                    node.updateAdjacentList((x+1,y)) 
                    self.cityMatrix[x][y] = node
                    y = y + 1
                    
                elif((y == columns-1) and (x < rows) and (x == 0)): 
                    node.updateAdjacentList((x,y-1)) 
                    node.updateAdjacentList((x+1,y)) 
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == columns - 1) and (x == rows-1)): 
                    node.updateAdjacentList((x-1,y)) 
                    node.updateAdjacentList((x,y-1)) 
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == columns - 1) and (x < rows)): 
                    node.updateAdjacentList((x-1,y)) 
                    node.updateAdjacentList((x,y-1)) 
                    node.updateAdjacentList((x+1,y))
                    self.cityMatrix[x][y] = node
                    y = y + 1


                elif((y < columns) and (x == 0)): 
                    node.updateAdjacentList((x,y-1)) 
                    node.updateAdjacentList((x,y+1)) 
                    node.updateAdjacentList((x+1,y)) 
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y < columns) and (x == rows - 1)):
                    node.updateAdjacentList((x-1,y)) 
                    node.updateAdjacentList((x,y-1)) 
                    node.updateAdjacentList((x,y+1)) 
                    self.cityMatrix[x][y] = node
                    y = y + 1
                else:
                    node.updateAdjacentList((x-1,y)) 
                    node.updateAdjacentList((x,y-1)) 
                    node.updateAdjacentList((x,y+1)) 
                    node.updateAdjacentList((x+1,y)) 
                    self.cityMatrix[x][y] = node
                    y = y + 1
                    
            x = x + 1
            y = 0
   

    def astar(self, destinationNode, taxiId):
        self.haveBlockAsNeighbor()
        sourceNode = self.searchTaxiNode(taxiId)
        openList = []
        openList.append(sourceNode)

        while( openList != []):
            nodeFromOpenList = openList[0]
            del openList[0] 
            if(nodeFromOpenList.getNodeValue() ==
               destinationNode.getNodeValue()):
                break

            nodeFromOpenListX = nodeFromOpenList.getX()
            nodeFromOpenListY = nodeFromOpenList.getY()
            self.cityMatrix[nodeFromOpenListX][nodeFromOpenListY].setVisit()
            adjacentNodesList = nodeFromOpenList.getAdjacentNodesList()

            for i in range(0, len(adjacentNodesList)):
                adjacentNodeX = adjacentNodesList[i][0]
                adjacentNodeY = adjacentNodesList[i][1]
                adjacentNode = self.searchNodeByCoordinates(adjacentNodeX,
                                                            adjacentNodeY)
                if(adjacentNode.isVisited() == False and
                   (adjacentNode.getNodeType() == "street" or
                   (adjacentNode.getNodeType() == "block" and
                    adjacentNode.getNodeValue()==
                    destinationNode.getNodeValue()) or
                    adjacentNode.getBlockAsNeighbor() == True)):

                    g = self.calculateG(nodeFromOpenList, adjacentNode)
                    h = self.calculateH(nodeFromOpenList, destinationNode)
                    f = g + h

                    if(self.isTheNodeAlreadyInTheList(openList, adjacentNode)
                       == True):
                        
                        if(f < adjacentNode.getCost()):
                            self.cityMatrix[adjacentNodeX][adjacentNodeY].setH(h)
                            self.cityMatrix[adjacentNodeX][adjacentNodeY].setD(g)
                            self.cityMatrix[adjacentNodeX][adjacentNodeY].setCost(f)
                            self.cityMatrix[adjacentNodeX][adjacentNodeY].setFather(
                                (nodeFromOpenList.getX(),nodeFromOpenList.getY()))
                            adjacentNode.setCost(f)

                    else:
                        self.cityMatrix[adjacentNodeX][adjacentNodeY].setH(h)
                        self.cityMatrix[adjacentNodeX][adjacentNodeY].setD(g)
                        self.cityMatrix[adjacentNodeX][adjacentNodeY].setCost(f)
                        self.cityMatrix[adjacentNodeX][adjacentNodeY].setFather(
                            (nodeFromOpenList.getX(),nodeFromOpenList.getY()))
                        adjacentNode.setCost(f)
                        openList.append(adjacentNode)

            openList = self.reorderOpenList(openList)

        self.buildTravel(destinationNode, taxiId)
        self.resetFatherNodes()
        self.setNodesAsNotVisited()

    def calculateG(self,actualNode, adyacentNode):
        adyacentNodeX = adyacentNode.getX()
        adyacentNodeY = adyacentNode.getY()
        actualNodeX = actualNode.getX()
        actualNodeY = actualNode.getY()
        g = abs(adyacentNodeX - actualNodeX) + abs(adyacentNodeY - actualNodeY)
        return g

    def calculateH(self,actualNode, destinationNode):
        destinationNodeX = destinationNode.getX()
        destinationNodeY = destinationNode.getY()
        actualNodeX = actualNode.getX()
        actualNodeY = actualNode.getY()
        h = abs(destinationNodeX - actualNodeX) + abs(destinationNodeY - actualNodeY)
        return h

    def reorderOpenList(self,openList):
        listWithCostReorder = self.createAListWithAllCostValuesAscendent(openList)
        newListReorder = []
        for i in range(0, len(openList)):
            index = listWithCostReorder[i][0]
            node = openList[index]
            newListReorder.append(node)
        return newListReorder

    def createAListWithAllCostValuesAscendent(self,openList):
        listWithCostValuesOnly = []
        for i in range(0, len(openList)):
            cost = openList[i].getCost()
            listWithCostValuesOnly.append((i, cost))

        reorderList = sorted(listWithCostValuesOnly,key=itemgetter(1))    
        return reorderList

    def isTheNodeAlreadyInTheList(self, openList, node):
        isAlready = False
        for i in range(0, len(openList)):
            nodeFromOpenList = openList[i]
            nodeFromOpenListX = nodeFromOpenList.getX()
            nodeFromOpenListY = nodeFromOpenList.getY()
            nodeX = node.getX()
            nodeY = node.getY()
            if(nodeX == nodeFromOpenListX and nodeY == nodeFromOpenListY):
                isAlready = True
                break
        return isAlready

    def setNodesAsNotVisited(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                self.cityMatrix[i][j].resetVisit()

    def resetFatherNodes(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                self.cityMatrix[i][j].setFather(0)

    def searchAnyClient(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "O"):
                    return self.cityMatrix[i][j]

    def buildTravel(self, destinationNode, taxiId):
        self.routeToTravel = []  
        destinationNodeX = destinationNode.getX()
        destinationNodeY = destinationNode.getY()
        fatherCoordinates = self.cityMatrix[destinationNodeX][destinationNodeY].getFather() 
        father = self.cityMatrix[fatherCoordinates[0]][fatherCoordinates[1]]

        while (father.getNodeValue() != taxiId):
            self.routeToTravel.append(fatherCoordinates)
            fatherCoordinates = father.getFather()
            father = self.cityMatrix[fatherCoordinates[0]][fatherCoordinates[1]]

        self.routeToTravel.reverse()
        self.routesVisited.append(self.routeToTravel)
            
    def searchNodeByCoordinates(self,x,y):
        return self.cityMatrix[x][y]

    def searchNodeByValue(self, nodeValue):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == nodeValue):
                    return self.cityMatrix[i][j]

    def searchNodeByType(self, nodeType):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeType() == nodeType):
                    return self.cityMatrix[i][j]

    def searchTaxiNode(self, taxiId):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == taxiId):
                    self.actualNode = self.cityMatrix[i][j]
                    return self.cityMatrix[i][j]

    def haveBlockAsNeighbor(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(i+1 < self.rows):
                    if((self.cityMatrix[i][j].getNodeValue() == "-" or
                        self.cityMatrix[i][j].getNodeValue() == "O" or
                        self.cityMatrix[i][j].getNodeValue() == "D" or
                        self.cityMatrix[i][j].getNodeValue() == " ") and
                       self.cityMatrix[i+1][j].getNodeType() == "block"):
                        self.cityMatrix[i][j].setBlockAsNeighbor()
                        self.cityMatrix[i][j].setBlockToWall(self.cityMatrix[i+1][j].getNodeValue())
                if(i-1 >= 0):
                    if ((self.cityMatrix[i][j].getNodeValue() == "-" or
                         self.cityMatrix[i][j].getNodeValue() == "O" or
                         self.cityMatrix[i][j].getNodeValue() == "D" or
                         self.cityMatrix[i][j].getNodeValue() == " ")
                          and self.cityMatrix[i-1][j].getNodeType() == "block"):
                        self.cityMatrix[i][j].setBlockAsNeighbor()
                        self.cityMatrix[i][j].setBlockToWall(self.cityMatrix[i-1][j].getNodeValue())

    def searchAllBlocks(self):
        blocks = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeType() == "block" and
                   self.cityMatrix[i][j].getNodeValue() != " "):
                    blocks.append(self.cityMatrix[i][j])
        return blocks

    def searchClientNode(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "O"):
                    return self.cityMatrix[i][j]

    def searchAllClients(self):
        clientPositions = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "O"):
                    clientPositions.append((self.cityMatrix[i][j].getX()
                                            ,self.cityMatrix[i][j].getY()))
        return clientPositions

    def searchAllWalls(self):
        wallsPositions = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "-"):
                    wallsPositions.append((self.cityMatrix[i][j].getX(),
                                           self.cityMatrix[i][j].getY()))
        return wallsPositions

    def searchAllTaxis(self):
        numberOfTaxis = 0
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue().isdigit() == True):
                    numberOfTaxis = numberOfTaxis + 1
        return numberOfTaxis

    def searchAllTaxisPosition(self):
        taxisPosition = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue().isdigit() == True):
                    taxisPosition.append([self.cityMatrix[i][j].getNodeValue(), [i,j]])
        return taxisPosition

    def searchAllTaxisId(self):
        taxisId = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue().isdigit() == True):
                    taxisId.append(self.cityMatrix[i][j].getNodeValue())
        return taxisId

    def searchAllApartmentsPosition(self):
        apartmentsPosition = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue().isupper() == True):
                    apartmentsPosition.append([self.cityMatrix[i][j].getNodeValue(), [i,j]])
        return apartmentsPosition

    def searchAllWorkplacesPosition(self):
        workplacesPosition = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue().islower() == True):
                    workplacesPosition.append([self.cityMatrix[i][j].getNodeValue(), [i,j]])
        return workplacesPosition

    def returnCityGraph(self):
        return self.cityMatrix

    def updateTaxisPosition(self, listOfNewPositions):
        listOfOldPositions = self.searchAllTaxisPosition()

        for i in range(0,len(listOfOldPositions)):
            x = listOfOldPositions[i][1][0]
            y = listOfOldPositions[i][1][1]
            self.cityMatrix[x][y].setNodeValue(" ")

        for j in range(0,len(listOfNewPositions)):
            x = listOfNewPositions[j][1][0]
            y = listOfNewPositions[j][1][1]
            self.cityMatrix[x][y].setNodeValue(listOfNewPositions[j][0])
            if(len(self.taxisPosition) < self.numberOfTaxis):
                self.taxisPosition.append([listOfNewPositions[j][0],[x,y]])
            else:
                self.taxisPosition[j] = [listOfNewPositions[j][0],[x,y]]
            
    def searchAllBuildings(self):
        numberOfBuildings = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue().isupper() == True):
                    numberOfBuildings.append(self.cityMatrix[i][j].getNodeValue())
        return numberOfBuildings

    def searchAllWorkplaces(self):
        numberOfWorkplaces = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue().islower() == True):
                    numberOfWorkplaces.append(self.cityMatrix[i][j].getNodeValue())
        return numberOfWorkplaces

    def resetAllClients(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "O"):
                    self.cityMatrix[i][j].setNodeValue("-")
                    self.cityMatrix[i][j].setNodeType("wall")
                    self.cityMatrix[i][j].client = Client()
                    self.cityMatrix[i][j].resetHaveAClient()

    def resetClient(self,x,y):
        self.cityMatrix[x][y].setNodeValue("-")
        self.cityMatrix[x][y].setNodeType("wall")
        self.cityMatrix[x][y].client = Client()
        self.cityMatrix[x][y].resetHaveAClient()

    def isThereAClient(self):
        clientsExist = False
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "O"):
                    clientsExist = True
                    
        return clientsExist

    def printRoute(self):
        for i in range(0, len(self.routeToTravel)):
            print("Nodo visitado-> x: ", self.routeToTravel[i][0])
            print("Nodo visitado-> y: ", self.routeToTravel[i][1])
            print()

    def updateInitialAndFinalValue(self):
        if(len(self.routeToTravel) > 1):
            initialNodeCoordinates = self.searchTaxiNode()
            finalNodeCoordinates = self.routeToTravel[len(self.routeToTravel)-1]
            self.cityMatrix[initialNodeCoordinates.getX()][initialNodeCoordinates.getY()].setNodeValue(" ")
            self.cityMatrix[finalNodeCoordinates[0]][finalNodeCoordinates[1]].setNodeValue("D")

    def pickAClient(self,apartmentName):
        taxi = ""
        for i in range(0,len(self.taxisPosition)):
            taxiPosition = self.taxisPosition[i][1]
            if(taxiPosition[0]+2 < self.rows):
                if(self.cityMatrix[taxiPosition[0]+2][taxiPosition[1]].getNodeValue() == apartmentName):
                    taxi = self.taxisPosition[i][0]
                    break
        return taxi

    def travelWithClientRoad(self, destination, taxiId):
        destinationNode = self.searchNodeByValue(destination)
        self.astar(destinationNode, taxiId)
        route = copy.deepcopy(self.routeToTravel)
        return route

def createCityGraph(matrix):
    cityGraph = CityGraph(matrix)
    return cityGraph
