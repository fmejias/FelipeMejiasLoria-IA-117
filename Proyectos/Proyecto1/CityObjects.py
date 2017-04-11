###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################

###This import is necessary to get a Python queue #####
import queue

###This import is necessary to generate random numbers
from random import randint

##Import the copy module
import copy

###########################################################################################################
# Client Class:
##########################################################################################################

class Client:
    def __init__(self):
        self.initialBlock = "" 
        self.destinationBlock = ""

    #This method set the initialBlock of the Client
    def setInitialBlock(self,initialBlock):
        self.initialBlock = initialBlock

    #This method get the initial block of the client
    def getInitialBlock(self):
        return self.initialBlock

    #This method set the destination block of the Client
    def setDestinationBlock(self,destinationBlock):
        self.destinationBlock = destinationBlock

    #This method get the destination block of the client
    def getDestinationBlock(self):
        return self.destinationBlock


###########################################################################################################
# CityNode Class:
###########################################################################################################
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
        self.client = Client() #Each city node contains an object client
        self.haveBlockAsNeighbor = False 
        self.haveAClient = False

        self.setTypeAndSetValue(value, isBlock) #To specified the type of the node

    #This method is in charge of specified the type and the value of the node
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

    #This method set the block as neighbor
    def setBlockAsNeighbor(self):
        self.haveBlockAsNeighbor = True

    #This method get the block as neighbor
    def getBlockAsNeighbor(self):
        return self.haveBlockAsNeighbor

    #This method indicates that this node have a client
    def setHaveAClient(self):
        self.haveAClient = True

    #This method indicates that this node not have a client
    def resetHaveAClient(self):
        self.haveAClient = False

    #This method returns if this node have a client
    def getHaveAClient(self):
        return self.haveAClient

    #This method get the block as neighbor
    def getBlockAsNeighbor(self):
        return self.haveBlockAsNeighbor
    
    #This method set the block to a wall according to that city node
    def setBlockToWall(self, block):
        self.belongToBlock = block

    #This method get the block of the wall
    def getBlockOfWall(self):
        return self.belongToBlock

    #This method return the client  of that city node
    def getClient(self):
        return self.client

    #This method set the initial block of the client
    def setInitialBlockToClient(self, initialBlock):
        self.client.setInitialBlock(initialBlock)

    #This method set the destination block of the client
    def setDestinationBlockToClient(self, destinationBlock):
        self.client.setDestinationBlock(destinationBlock)

    #This method get the initial block of the client
    def getInitialBlockOfTheClient(self):
        return self.client.getInitialBlock()

    #This method get the destination block of the client
    def getDestinationBlockOfTheClient(self):
        return self.client.getDestinationBlock()
    
    #This method return the father of the node
    def getFather(self):
        return self.father

    #This method set the father of the node
    def setFather(self, father):
        self.father = father
    
    #This method return the cost of the node
    def getCost(self):
        return self.cost

    #This method set the cost of the node
    def setCost(self, cost):
        self.cost = cost

    #This method return the distance of the node
    def getD(self):
        return self.d

    #This method set the distance of the node
    def setD(self, distance):
        self.d = self.d + distance

    #This method return the heuristic of the node
    def getH(self):
        return self.h

    #This method set the heuristic of the node
    def setH(self, h):
        self.h = h

    #This method return the x position
    def getX(self):
        return self.x

    #This method set the x position of the node
    def setX(self, x):
        self.x = x

    #This method return the y position
    def getY(self):
        return self.y

    #This method set the y position of the node
    def setY(self, y):
        self.y = y
        
    #This method return the type of the node
    def getNodeType(self):
        return self.typeOfNode

    #This method set the type of the node
    def setNodeType(self, typeOfNode):
        self.typeOfNode = typeOfNode

    #This method return the value of the Node
    def getNodeValue(self):
        return self.valueOfNode

    #This method set the value of the Node
    def setNodeValue(self, valueOfNode):
        self.valueOfNode = valueOfNode

    #This method indicates if the node has been visited
    def isVisited(self):
        return self.visited

    #This method returns the list of the adjacent node
    def getAdjacentNodesList(self):
        return self.adjacentNodesList

    #This method set the node as visited
    def setVisit(self):
        self.visited = True

    #This method set the node as not visited
    def resetVisit(self):
        self.visited = False

    #This method updates the adjacent nodes list, this method receives an string, not an object CityNode
    def updateAdjacentList(self, node):
        self.adjacentNodesList.append(node)



###########################################################################################################
# CityGraph Class:
###########################################################################################################
class CityGraph:
    def __init__(self, city):
        self.routeTraveled = [] #Contains the route in progress of the taxi
        self.routeToTravel = [] #Contains the route from one block to another block
        self.routesVisited = [] #Contains all of the routes visited by the taxi (Is a list of lists)
        self.actualNode = ""  #This is going to be the actual node of the taxi
        self.destinationNode = ""
        self.cityMatrix = copy.deepcopy(city) #Contains the matrix of the city
        self.rows = len(self.cityMatrix) #Rows of the city matrix
        self.columns = len(self.cityMatrix[0]) #Columns of the city matrix

        #Call the method in charge of create the city graph
        self.createCityGraph(len(city),len(city[0]))


    #This method is in charge of create the city matrix as a graph
    def createCityGraph(self,rows,columns):
        x = 0 #Assign the x position of the node in the grid
        y = 0 #Assign the y position of the node in the grid
        while(x < rows):
            while(y < columns):
                node = CityNode(x,y,self.cityMatrix[x][y][1], self.cityMatrix[x][y][0])
                ####Append the adjacent nodes#####
                if((y == 0) and (x < rows) and (x == 0)): #y = 0 y x = 0
                    node.updateAdjacentList((x,y+1)) #Right
                    node.updateAdjacentList((x+1,y)) #Down
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == 0) and (x == rows-1)): #y = 0 y x = rows - 1
                    node.updateAdjacentList((x-1,y)) #Up
                    node.updateAdjacentList((x,y+1)) #Right
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == 0) and (x < rows)): #y = 0 y x > 0
                    node.updateAdjacentList((x-1,y)) #Up
                    node.updateAdjacentList((x,y+1)) #Right
                    node.updateAdjacentList((x+1,y)) #Down
                    self.cityMatrix[x][y] = node
                    y = y + 1
                    
                elif((y == columns-1) and (x < rows) and (x == 0)): #y = columns-1 y x = 0
                    node.updateAdjacentList((x,y-1)) #Left
                    node.updateAdjacentList((x+1,y)) #Down
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == columns - 1) and (x == rows-1)): #y = columns - 1 y x = rows - 1
                    node.updateAdjacentList((x-1,y)) #Up
                    node.updateAdjacentList((x,y-1)) #Left
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y == columns - 1) and (x < rows)): #y = columns - 1 y x = x > 0
                    node.updateAdjacentList((x-1,y)) #Up
                    node.updateAdjacentList((x,y-1)) #Left
                    node.updateAdjacentList((x+1,y)) #Down
                    self.cityMatrix[x][y] = node
                    y = y + 1


                elif((y < columns) and (x == 0)): #y < columns y x = 0
                    node.updateAdjacentList((x,y-1)) #Left
                    node.updateAdjacentList((x,y+1)) #Right
                    node.updateAdjacentList((x+1,y)) #Down
                    self.cityMatrix[x][y] = node
                    y = y + 1

                elif((y < columns) and (x == rows - 1)):
                    node.updateAdjacentList((x-1,y)) #Up
                    node.updateAdjacentList((x,y-1)) #Left
                    node.updateAdjacentList((x,y+1)) #Right
                    self.cityMatrix[x][y] = node
                    y = y + 1
                else:
                    node.updateAdjacentList((x-1,y)) #Up
                    node.updateAdjacentList((x,y-1)) #Left
                    node.updateAdjacentList((x,y+1)) #Right
                    node.updateAdjacentList((x+1,y)) #Down
                    self.cityMatrix[x][y] = node
                    y = y + 1
                    
            x = x + 1
            y = 0
   
        

    #This method is in charge of perform the BFS search
    def BFS(self, destinationNode):
        
        #For the beginning, I use this
        self.haveBlockAsNeighbor()
        
        #First, search the taxi node
        sourceNode = self.searchTaxiNode()

        #Get the coordinates of the source node
        sourceNodeX = sourceNode.getX()
        sourceNodeY = sourceNode.getY()

        #Second, set the source node as visited
        self.cityMatrix[sourceNodeX][sourceNodeY].setVisit()

        #Third, create a queue
        q = queue.Queue()

        #Fourth, enqueue the source node
        q.put(sourceNode)

        #Fifth, while the queue is not empty
        while(q.empty() != True):

            #Sixth, extract node from the queue
            nodeFromQueue = q.get()

            #Finish condition
            if(nodeFromQueue.getNodeValue() == destinationNode.getNodeValue()):
                break

            #7, extract the adjacent list
            adjacentNodesList = nodeFromQueue.getAdjacentNodesList()

            #8, explore all adjacent nodes
            for i in range(0, len(adjacentNodesList)):

                #9, get adjacent node and then get its coordinates
                adjacentNodeX = adjacentNodesList[i][0]
                adjacentNodeY = adjacentNodesList[i][1]
                adjacentNode = self.searchNodeByCoordinates(adjacentNodeX,adjacentNodeY)
                
                #10, if the adjacent node is not visited, then set as visited
                if(adjacentNode.isVisited() == False and (adjacentNode.getNodeType() == "street" or adjacentNode.getNodeType() == "block" or
                                                          adjacentNode.getBlockAsNeighbor() == True)):

                    self.cityMatrix[adjacentNodeX][adjacentNodeY].setVisit()
                    self.cityMatrix[adjacentNodeX][adjacentNodeY].setFather((nodeFromQueue.getX(),nodeFromQueue.getY()))

                    #11, Enqueue this adjacentNode
                    q.put(adjacentNode)

        #12, then build the path
        self.buildTravel(destinationNode)

    #This method is in charge of perform the DFS search
    def DFS(self, destinationNode):
        #For the beginning, I use this
        self.haveBlockAsNeighbor()
        
        #First, search the taxi node
        sourceNode = self.searchTaxiNode()

        #Get the coordinates of the source node
        sourceNodeX = sourceNode.getX()
        sourceNodeY = sourceNode.getY()

        #Second, set the source node as visited
        self.cityMatrix[sourceNodeX][sourceNodeY].setVisit()

        #Third, create a stack
        stack = []

        #4, add the sourceNode to the stack
        stack.append(sourceNode)

        #Fifth, while the stack is not empty
        while( stack != []):
            #Sixth, extract node from the stack
            nodeFromStack = stack.pop()

            #Finish condition
            if(nodeFromStack.getNodeValue() == destinationNode.getNodeValue()):
                break

            #7, extract the adjacent list
            adjacentNodesList = nodeFromStack.getAdjacentNodesList()

            #8, explore all adjacent nodes
            for i in range(0, len(adjacentNodesList)):

                #9, get adjacent node and then get its coordinates
                adjacentNodeX = adjacentNodesList[i][0]
                adjacentNodeY = adjacentNodesList[i][1]
                adjacentNode = self.searchNodeByCoordinates(adjacentNodeX,adjacentNodeY)
                
                #10, if the adjacent node is not visited, then set as visited
                if(adjacentNode.isVisited() == False and (adjacentNode.getNodeType() == "street" or adjacentNode.getNodeType() == "block" or
                                                          adjacentNode.getBlockAsNeighbor() == True)):
                    self.cityMatrix[adjacentNodeX][adjacentNodeY].setVisit()
                    self.cityMatrix[adjacentNodeX][adjacentNodeY].setFather((nodeFromStack.getX(),nodeFromStack.getY()))

                    #11, Add the adjacentNode to the stack
                    stack.append(adjacentNode)

        #12, then build the path
        self.buildTravel(destinationNode)


    #This method is in charge of perform the A*
    def astar(self):
        print("Realiza A*")

    #This method is in charge of set all the nodes as not visited
    def setNodesAsNotVisited(self):
        for i in (0,self.rows):
            for j in (0,self.columns):
                self.cityMatrix[i][j].resetVisit()

    #This method is in charge of set all the nodes as not visited
    def resetFatherNodes(self):
        for i in (0,self.rows):
            for j in (0,self.columns):
                self.cityMatrix[i][j].setFather(0)

    #This method is in charge of search any client
    def searchAnyClient(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "O"):
                    return self.cityMatrix[i][j]

    #This method is in charge of adding N Random Clients to the City
    def addRandomClients(self,n):
        for i in range(0,n):
            listOfBlocks = self.searchAllBlocks() #Get a list with all of the blocks
            randomOriginIndex = randint(0,len(listOfBlocks)-1) #This is for the origin of the client
            randomDestinationIndex = randint(0,len(listOfBlocks)-1) #This is for the destination of the client

            #This is to verificate that the destination and the origin are not the same
            while(randomOriginIndex != randomDestinationIndex):
                randomDestinationIndex = randint(0,len(listOfBlocks)-1) #This is for the destination of the client

            #Establish the coordinates of the client
            clientX = listOfBlocks[randomOriginIndex].getX() - 1
            clientY = listOfBlocks[randomOriginIndex].getY()

            #Get the client node
            clientNode = self.cityMatrix[clientX][clientY]

            if(clientNode.getNodeValue() != "O"):
                self.cityMatrix[clientX][clientY].setNodeValue("O")
                self.cityMatrix[clientX][clientY].setHaveAClient()
                self.cityMatrix[clientX][clientY].setInitialBlockToClient(listOfBlocks[randomOriginIndex].getNodeValue())
                self.cityMatrix[clientX][clientY].setDestinationBlockToClient(listOfBlocks[randomDestinationIndex].getNodeValue())

            else:
                #Establish the coordinates of the client
                clientX = listOfBlocks[randomOriginIndex].getX() + 1
                clientY = listOfBlocks[randomOriginIndex].getY()
                self.cityMatrix[clientX][clientY].setNodeValue("O")
                self.cityMatrix[clientX][clientY].setHaveAClient()
                self.cityMatrix[clientX][clientY].setInitialBlockToClient(listOfBlocks[randomOriginIndex].getNodeValue())
                self.cityMatrix[clientX][clientY].setDestinationBlockToClient(listOfBlocks[randomDestinationIndex].getNodeValue())

    #This method is in charge of adding a specific client to the City (c1 y c2 son Strings)
    def addSpecificClient(self,c1,c2):
        #Get initial and destination blocks
        initialNode = searchNodeByValue(c1)
        destinationNode = searchNodeByValue(c2)
        
        #Establish the coordinates of the client
        clientX = initialNode.getX() - 1
        clientY = initialNode.getY()

        #Get the client node
        clientNode = self.cityMatrix[clientX][clientY]

        if(clientNode.getNodeValue() != "O"):
            self.cityMatrix[clientX][clientY].setNodeValue("O")
            self.cityMatrix[clientX][clientY].setHaveAClient()
            self.cityMatrix[clientX][clientY].setInitialBlockToClient(initialNode.getNodeValue())
            self.cityMatrix[clientX][clientY].setDestinationBlockToClient(destinationNode.getNodeValue())

        else:
            #Establish the coordinates of the client
            clientX = initialNode.getX() + 1
            clientY = initialNode.getY()
            self.cityMatrix[clientX][clientY].setNodeValue("O")
            self.cityMatrix[clientX][clientY].setHaveAClient()
            self.cityMatrix[clientX][clientY].setInitialBlockToClient(initialNode.getNodeValue())
            self.cityMatrix[clientX][clientY].setDestinationBlockToClient(destinationNode.getNodeValue())
    
    #This method is in charge of park the Taxi in C block, C is a string
    def parkTaxi(self,c):
        destinationNode = self.searchNodeByValue(c)

        ##For the moment, Im going to use the BFS search algorithm
        self.BFS(destinationNode)

    #This method is use to search all of the clients
    def search(self):
        areThereClients = self.isThereAClient()
        while(areThereClients != False):

            #Search for a client node
            clientNode = self.searchClientNode()

            #Get the destination block of that client
            destinationBlock = clientNode.getDestinationBlockOfTheClient()

            #Get the destination node
            destinationNode = self.searchNodeByValue(destinationBlock.getNodeValue())

            #Calculate the path to go and pick up the client
            self.BFS(clientNode)

            #Then calculate the path to go and leave the client in its destiny
            self.BFS(destinationNode)

    #This method is in charge of go over the city with the taxi
    def taxiTravel(self):
        #Get all of the blocks available
        listOfBlocks = self.searchAllBlocks()

        #This is for the origin of the client
        randomOriginIndex = randint(0,len(listOfBlocks)-1)

        #Get a random block to go
        randomBlock = listOfBlocks[randomOriginIndex]

        #Specify the destination node as the random block
        destinationNode = randomBlock

        ##For the moment, Im going to use the BFS search algorithm
        self.BFS(destinationNode)

        #Print the travel
        self.printRoute()

        #Return the travel
        return self.routeToTravel

    #This method build all of the travel
    def buildTravel(self, destinationNode):
        #Reset the route to travel
        self.routeToTravel = []
        
        destinationNodeX = destinationNode.getX()
        destinationNodeY = destinationNode.getY()
        fatherCoordinates = self.cityMatrix[destinationNodeX][destinationNodeY].getFather() #Get father coordinates of the destination node
        father = self.cityMatrix[fatherCoordinates[0]][fatherCoordinates[1]]

        #While the father is different from the taxi node
        while (father.getNodeValue() != "D"):
            self.routeToTravel.append(fatherCoordinates)
            fatherCoordinates = father.getFather()
            father = self.cityMatrix[fatherCoordinates[0]][fatherCoordinates[1]]

        #Then reverse the list
        self.routeToTravel.reverse()

        #Add the route to the routes visited list
        self.routesVisited.append(self.routeToTravel)
            

    #This method is in charge of search a node by the coordinates
    def searchNodeByCoordinates(self,x,y):
        return self.cityMatrix[x][y]

    #This method is in charge of search a node by the value of the node
    def searchNodeByValue(self, nodeValue):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == nodeValue):
                    return self.cityMatrix[i][j]

    #This method is in charge of search a node by the type of the node
    def searchNodeByType(self, nodeType):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeType() == nodeType):
                    return self.cityMatrix[i][j]

    #This method is in charge of search the taxi node
    def searchTaxiNode(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "D"):
                    self.actualNode = self.cityMatrix[i][j]
                    return self.cityMatrix[i][j]

    
    #This method set all the walls (-) that have blocks as neighbors
    def haveBlockAsNeighbor(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(i+1 < self.rows):
                    if((self.cityMatrix[i][j].getNodeValue() == "-" or self.cityMatrix[i][j].getNodeValue() == "O")
                       and self.cityMatrix[i+1][j].getNodeType() == "block"):
                        self.cityMatrix[i][j].setBlockAsNeighbor()
                        self.cityMatrix[i][j].setBlockToWall(self.cityMatrix[i+1][j].getNodeValue())
                elif(i-1 >= 0):
                    if ((self.cityMatrix[i][j].getNodeValue() == "-" or self.cityMatrix[i][j].getNodeValue() == "O")
                          and self.cityMatrix[i-1][j].getNodeType() == "block"):
                        self.cityMatrix[i][j].setBlockAsNeighbor()
                        self.cityMatrix[i][j].setBlockToWall(self.cityMatrix[i-1][j].getNodeValue())

    #This method is in charge of return a list with all of the node blocks availables
    def searchAllBlocks(self):
        blocks = []
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeType() == "block" and self.cityMatrix[i][j].getNodeValue() != " "):
                    blocks.append(self.cityMatrix[i][j])
        return blocks

    #This method is in charge of search any client
    def searchClientNode(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "O"):
                    return self.cityMatrix[i][j]
                    

    #This method is in charge of tell if there are some clients
    def isThereAClient(self):
        clientsExist = False
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(self.cityMatrix[i][j].getNodeValue() == "O"):
                    clientsExist = True
        return clientsExist

    #This method print a route
    def printRoute(self):
        for i in range(0, len(self.routeToTravel)):
            print("Nodo visitado-> x: ", self.routeToTravel[i][0])
            print("Nodo visitado-> y: ", self.routeToTravel[i][1])
            print()


#This method return an CityGraph Object
def createCityGraph(matrix):
    cityGraph = CityGraph(matrix)
    return cityGraph
