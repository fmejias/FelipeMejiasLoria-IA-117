from random import randint
from operator import itemgetter
import copy

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

    def getBlockAsNeighbor(self):
        return self.haveBlockAsNeighbor
    
    def setBlockToWall(self, block):
        self.belongToBlock = block

    def getBlockOfWall(self):
        return self.belongToBlock

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


class CityGraph:
    def __init__(self, city):
        self.actualNode = ""
        self.destinationNode = ""
        self.cityMatrix = copy.deepcopy(city) 
        self.rows = len(self.cityMatrix) 
        self.columns = len(self.cityMatrix[0]) 
        self.taxiInitialPosition = 0
        self.taxiX = 0
        self.taxiY = 0
        self.nothing = 0
        self.right = 1
        self.left = 2
        self.up = 3
        self.down = 4

        self.createCityGraph(len(city),len(city[0]))

    def createCityGraph(self,rows,columns):
        x = 0 
        y = 0 
        while(x < rows):
            while(y < columns):
                node = CityNode(x,y,self.cityMatrix[x][y][1], self.cityMatrix[x][y][0])
                if((y == 0) and (x < rows) and (x == 0)): 
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == 0) and (x == rows-1)): 
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == 0) and (x < rows)): 
                    self.cityMatrix[x][y] = node
                    y = y + 1
                    
                elif((y == columns-1) and (x < rows) and (x == 0)): 
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == columns - 1) and (x == rows-1)): 
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == columns - 1) and (x < rows)): 
                    self.cityMatrix[x][y] = node
                    y = y + 1


                elif((y < columns) and (x == 0)): 
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y < columns) and (x == rows - 1)):
                    self.cityMatrix[x][y] = node
                    y = y + 1
                else:
                    self.cityMatrix[x][y] = node
                    y = y + 1
                    
            x = x + 1
            y = 0

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

    def searchTaxi(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "D"):
                    self.actualNode = self.cityMatrix[i][j]
                    return self.cityMatrix[i][j]

    def searchAllBlocks(self):
        blocks = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeType() == "block" and self.cityMatrix[i][j].getNodeValue() != " "):
                    blocks.append(self.cityMatrix[i][j])
        return blocks

    def searchAllWalls(self):
        wallsPositions = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "-"):
                    wallsPositions.append((self.cityMatrix[i][j].getX(),self.cityMatrix[i][j].getY()))
        return wallsPositions

    def taxiCrashed(self,action):
        taxiNode = self.searchTaxi()
        taxiX = taxiNode.getX()
        taxiY = taxiNode.getY()
        crashed = 0
        if(action == self.nothing):
            crashed = 0
        elif(action == self.right):
            rightNode = self.searchNodeByCoordinates(taxiX, taxiY+1)
            if(rightNode.getNodeValue() != " "):
                crashed = 1
        elif(action == self.left):
            leftNode = self.searchNodeByCoordinates(taxiX, taxiY-1)
            if(leftNode.getNodeValue() != " "):
                crashed = 1
        elif(action == self.up):
            upNode = self.searchNodeByCoordinates(taxiX-1, taxiY)
            if(upNode.getNodeValue() != " "):
                crashed = 1
        elif(action == self.down):
            downNode = self.searchNodeByCoordinates(taxiX+1, taxiY)
            if(downNode.getNodeValue() != " "):
                crashed = 1
        return crashed

    def calculateReward(self,action):
        crashed = self.taxiCrashed(action)
        reward = 0
        if(crashed == 1):
            reward = -500
        else:
            reward = -5

        return reward

    def calculateState(self):
        taxiNode = self.searchTaxi()
        leftDistance = self.getLeftDistance(taxiNode)
        rightDistance = self.getRightDistance(taxiNode)
        upDistance = self.getUpDistance(taxiNode)
        downDistance = self.getDownDistance(taxiNode)
        return [leftDistance, rightDistance, upDistance, downDistance]

    def getLeftDistance(self,taxiNode):
        x = taxiNode.getX()
        y = taxiNode.getY() 
        if(taxiNode.getY()-1 > 0):
            y = taxiNode.getY()-1
        nodeValue = self.cityMatrix[x][y].getNodeValue()
        distance = 0
        while (nodeValue == " " and y-1 > 0):
            distance = distance + 1
            y = y - 1
            nodeValue = self.cityMatrix[x][y].getNodeValue()
        return distance

    def getRightDistance(self,taxiNode):
        x = taxiNode.getX()
        y = taxiNode.getY() 
        if(taxiNode.getY()+1 < self.columns):
            y = taxiNode.getY()+1
        nodeValue = self.cityMatrix[x][y].getNodeValue()
        distance = 0
        while (nodeValue == " " and y+1 < self.columns):
            distance = distance + 1
            y = y + 1
            nodeValue = self.cityMatrix[x][y].getNodeValue()
        return distance

    def getUpDistance(self,taxiNode):
        x = taxiNode.getX() 
        if(taxiNode.getX()-1 > 0):
            x = taxiNode.getX()-1
        y = taxiNode.getY()
        nodeValue = self.cityMatrix[x][y].getNodeValue()
        distance = 0
        while (nodeValue == " " and x-1 > 0):
            distance = distance + 1
            x = x - 1
            nodeValue = self.cityMatrix[x][y].getNodeValue()
        return distance

    def getDownDistance(self,taxiNode):
        x = taxiNode.getX() 
        if(taxiNode.getX()+1 < self.rows):
            x = taxiNode.getX()+1
        y = taxiNode.getY()
        nodeValue = self.cityMatrix[x][y].getNodeValue()
        distance = 0
        while (nodeValue == " " and x+1 < self.rows):
            distance = distance + 1
            x = x + 1
            nodeValue = self.cityMatrix[x][y].getNodeValue()
        return distance    
    
    def updateTaxiCoordinates(self, action):
        taxiNode = self.searchTaxi()
        taxiX = taxiNode.getX()
        taxiY = taxiNode.getY()
        if(action == self.nothing):
            self.cityMatrix[taxiX][taxiY].setNodeValue("D")
        elif(action == self.right):
            self.cityMatrix[taxiX][taxiY].setNodeValue(" ")
            self.cityMatrix[taxiX][taxiY+1].setNodeValue("D")
        elif(action == self.left):
            self.cityMatrix[taxiX][taxiY].setNodeValue(" ")
            self.cityMatrix[taxiX][taxiY-1].setNodeValue("D")
        elif(action == self.up):
            self.cityMatrix[taxiX][taxiY].setNodeValue(" ")
            self.cityMatrix[taxiX-1][taxiY].setNodeValue("D")
        elif(action == self.down):
            self.cityMatrix[taxiX][taxiY].setNodeValue(" ")
            self.cityMatrix[taxiX+1][taxiY].setNodeValue("D")

    def updateTaxiWallCoordinates(self, action):
        taxiNode = self.searchTaxi()
        taxiX = taxiNode.getX()
        taxiY = taxiNode.getY()
        if(action == self.nothing):
            self.cityMatrix[taxiX][taxiY].setNodeValue("D")
        elif(action == self.right):
            self.cityMatrix[taxiX][taxiY].setNodeValue("-")
            self.cityMatrix[taxiX][taxiY+1].setNodeValue("D")
        elif(action == self.left):
            self.cityMatrix[taxiX][taxiY].setNodeValue("-")
            self.cityMatrix[taxiX][taxiY-1].setNodeValue("D")
        elif(action == self.up):
            self.cityMatrix[taxiX][taxiY].setNodeValue("-")
            self.cityMatrix[taxiX-1][taxiY].setNodeValue("D")
        elif(action == self.down):
            self.cityMatrix[taxiX][taxiY].setNodeValue("-")
            self.cityMatrix[taxiX+1][taxiY].setNodeValue("D")

def createCityGraph(matrix):
    cityGraph = CityGraph(matrix)
    return cityGraph
