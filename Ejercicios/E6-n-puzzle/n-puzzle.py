import random

####This class represent a vertex of the graph ####
class Vertex:
    ###
    # self.vertex_id = contains the label of the vertex
    # self.visited = indicates if the node has been visited
    # self.adjacent_vertex_list = contains all of the adjacent vertex of the vertex
    ###
    def __init__(self,vertex_id,x,y):
        self.vertex_id = vertex_id
        self.visited = False
        self.adjacent_vertex_list = []
        self.x = x
        self.y = y
        self.typeOfVertex = ""
        self.valueOfVertex = ""
        self.cost = 0
        self.d = 0
        self.h = 0
        self.father = 0

    #This method return the father of the vertex
    def getFather(self):
        return self.father

    #This method set the father of the Vertex
    def setFather(self, father):
        self.father = father
    
    #This method return the cost of the vertex
    def getCost(self):
        return self.cost

    #This method set the cost of the Vertex
    def setCost(self, cost):
        self.cost = cost

    #This method return the distance of the vertex
    def getD(self):
        return self.d

    #This method set the distance of the Vertex
    def setD(self, distance):
        self.d = self.d + distance

    #This method return the heuristic of the vertex
    def getH(self):
        return self.h

    #This method set the heuristic of the Vertex
    def setH(self, h):
        self.h = h

    #This method return the x position
    def getVertexX(self):
        return self.x

    #This method set the x position of the Vertex
    def setVertexX(self, x):
        self.x = x

    #This method return the y position
    def getVertexY(self):
        return self.y

    #This method set the y position of the Vertex
    def setVertexY(self, y):
        self.y = y
        
    #This method return the type of the Vertex
    def getVertexType(self):
        return self.typeOfVertex

    #This method set the type of the Vertex
    def setVertexType(self, typeOfVertex):
        self.typeOfVertex = typeOfVertex

    #This method return the value of the Vertex
    def getVertexValue(self):
        return self.valueOfVertex

    #This method set the value of the Vertex
    def setVertexValue(self, valueOfVertex):
        self.valueOfVertex = valueOfVertex
        
    #This method return the vertex id
    def getVertexId(self):
        return self.vertex_id

    #This method return the vertex id
    def setVertexId(self,vertex_id):
        self.vertex_id = vertex_id

    #This method indicates if the vertex has been visited
    def isVisited(self):
        return self.visited

    #This method returns the list of the adjacent vertex
    def getAdjacentVertex(self):
        return self.adjacent_vertex_list

    #This method returns the list of the adjacent vertex
    def resetAdjacentList(self):
        self.adjacent_vertex_list = []
    
    #This method set the vertex as visited
    def setVisit(self):
        self.visited = True

    #This method updates the adjacent vertex of the vertex, this method receives an string, not an object Vertex
    def updateAdjacentList(self, vertex):
        self.adjacent_vertex_list.append(vertex)



##### This is the method in charge of perform n-puzzle ##################
def n_puzzle():
    entry = int(input().strip())#Reads the first input
    grid_rows = entry #Number of rows of the grid
    grid_columns = entry #Number of columns of the grid
    number_of_tiles = (grid_rows*grid_columns) - 1 #Number of tiles of the puzzle
    
    ######Variables need it to convert the inital grid in a graph##########
    initial_graph = [] #This contains the initial graph created
    number_of_nodes = 0 #Variable use in the creation of the graph 
    list_of_vertex = create_vertex(grid_rows, grid_columns) #Here I call a function to get a list of all the Vertex of the graph
    initial_graph = list_of_vertex #Save the graph created in the graph list
    graph_index = 0 #Index to go over the nodes of the graph
    empty_cell_index = 0

    ###Txt FILE
 #   f = open('n-puzzle.txt', "r")
    ## The variable "lines" is a list containing all lines
 #   lines = f.readlines()

    #Go over the grid and assign the value and the type of the vertex, and also creates the initial grid
    while(number_of_nodes < grid_rows*grid_columns): 
        entry = input().strip()
        if(entry == "0"):
            initial_graph[graph_index].setVertexType("empty_cell")
            initial_graph[graph_index].setVertexValue("0")
            empty_cell_index = graph_index
            graph_index = graph_index + 1
            number_of_nodes = number_of_nodes + 1
        else:
            initial_graph[graph_index].setVertexType("tile")
            initial_graph[graph_index].setVertexValue(entry)
            graph_index = graph_index + 1
            number_of_nodes = number_of_nodes + 1

  #  f.close()
    
    ######Variables need it to convert the final grid in a graph##########
    final_graph = [] #This contains the final graph created
    number_of_nodes = 0 #Variable use in the creation of the graph 
    list_of_vertex = create_vertex(grid_rows, grid_columns) #Here I call a function to get a list of all the Vertex of the graph
    final_graph = list_of_vertex #Save the graph created in the graph list
    graph_index = 0 #Index to go over the nodes of the graph
    node_value = 1 #Contains the value of the node
    #Go over the grid and assign the value and the type of the vertex, and also creates the initial grid
    while(number_of_nodes < grid_rows * grid_columns): 
        if(number_of_nodes == 0):
            final_graph[graph_index].setVertexType("empty_cell")
            final_graph[graph_index].setVertexValue("0")
            graph_index = graph_index + 1
            number_of_nodes = number_of_nodes + 1
        else:
            final_graph[graph_index].setVertexType("tile")
            final_graph[graph_index].setVertexValue(node_value)
            graph_index = graph_index + 1
            number_of_nodes = number_of_nodes + 1
            node_value = node_value + 1

    ###Now the graph has been created###
    astar(initial_graph, final_graph,  grid_rows, grid_columns)

    
###This function performs the A* algorithm###
def astar(initial_graph, resolved_graph, rows, columns):

    ####Assign the rearrange graph with the initial graph###
    rearrange_graph = initial_graph
    graph = initial_graph
    
    graph_index = 0 #This index is used to go over the graph
    stack = [] #This stack is use in the algorithm
    distance = 0 #This is the distance of the edges

    food_cost = 0 #This is the cost if the neighbor is the food
    wall_space_cost = 1 #This is the cost if the neighbor is anything else
    
    open_list = [] #This list is use to introduce nodes that are going to be evaluated
    close_list = [] #This list is use to introduce nodes that were evaluated

    find_food = False #This variable is use to finish the algorithm
    assign_father = False #This variable is use to assign a father to the adjacent nodes
    
    resolved = False #This variable indicates when the puzzle is solved
    empty_cell_number_of_movements = 0 #Count the number of movements

    path_list = []
    
    #Beginning of the algorithm
    while(resolved == False):
        
        #Step 1: Get the first element of the open list
        empty_cell_index = search_empty_cell(graph) #Get the index of the empty cell
        element_neighbors_list = graph[empty_cell_index].getAdjacentVertex() #Get the list of adjacent cells
        neighbor_choose = random.randint(0,len(element_neighbors_list)-1)
        graph = rearrange_puzzle(graph, graph[empty_cell_index].getVertexId(), element_neighbors_list[neighbor_choose][0])
        graph = update_graph_neighbors(graph,rows,columns)
        empty_cell_number_of_movements = empty_cell_number_of_movements + 1
     #   print(element_neighbors_list[neighbor_choose][1])
        path_list.append(element_neighbors_list[neighbor_choose][1])
        
        #This check if the puzzle is solved
        if(graph[0].getVertexValue() == "0" and graph[1].getVertexValue() == "1" and graph[2].getVertexValue() == "2"
           and graph[3].getVertexValue() == "3" and graph[4].getVertexValue() == "4" and graph[5].getVertexValue() == "5"
           and graph[6].getVertexValue() == "6" and graph[7].getVertexValue() == "7" and graph[8].getVertexValue() == "8"):
        #    print_puzzle(graph,rows,columns)
            resolved = True
            #print()
            print(empty_cell_number_of_movements)
            print_list(path_list)


#### This function sort the open_list in an ascendent form ####
def review_open_list(graph, graph_resolved):
    i = 0
    resolved = True
    while(i < len(graph)):
        if(graph[i].getVertexValue() != graph_resolved[i].getVertexValue()):
            resolved = False
            break
        else:
            i = i + 1
    return resolved

###This function update the new graph neighbor ###
def update_graph_neighbors(graph,rows,columns):
    x = 0 #Assign the x position of the node in the grid
    y = 0 #Assign the y position of the node in the grid
    vertex_id = 0
    while(x < rows):
        while(y < columns):
            ####Append the adjacent nodes#####
            if((y == 0) and (x < rows) and (x == 0)): #y = 0 y x = 0
                graph[vertex_id].resetAdjacentList()
                graph[vertex_id].updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                graph[vertex_id].updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == 0) and (x == rows-1)): #y = 0 y x = rows - 1
                graph[vertex_id].resetAdjacentList()
                graph[vertex_id].updateAdjacentList([vertex_id - columns,"UP"]) #Up
                graph[vertex_id].updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == 0) and (x < rows)): #y = 0 y x > 0
                graph[vertex_id].resetAdjacentList()
                graph[vertex_id].updateAdjacentList([vertex_id - columns,"UP"]) #Up
                graph[vertex_id].updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                graph[vertex_id].updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_id = vertex_id + 1
                y = y + 1
                
            elif((y == columns-1) and (x < rows) and (x == 0)): #y = columns-1 y x = 0
                graph[vertex_id].resetAdjacentList()
                graph[vertex_id].updateAdjacentList([vertex_id - 1, "LEFT"]) #Left
                graph[vertex_id].updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == columns - 1) and (x == rows-1)): #y = columns - 1 y x = rows - 1
                graph[vertex_id].resetAdjacentList()
                graph[vertex_id].updateAdjacentList([vertex_id - columns,"UP"]) #Up
                graph[vertex_id].updateAdjacentList([vertex_id - 1, "LEFT"]) #Left
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == columns - 1) and (x < rows)): #y = columns - 1 y x = x > 0
                graph[vertex_id].updateAdjacentList([vertex_id - columns,"UP"]) #Up
                graph[vertex_id].updateAdjacentList([vertex_id - 1, "LEFT"]) #Left
                graph[vertex_id].updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_id = vertex_id + 1
                y = y + 1


            elif((y < columns) and (x == 0)): #y < columns y x = 0
                graph[vertex_id].resetAdjacentList()
                graph[vertex_id].updateAdjacentList([vertex_id - 1, "LEFT"]) #Left
                graph[vertex_id].updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                graph[vertex_id].updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y < columns) and (x == rows - 1)):
                graph[vertex_id].resetAdjacentList()
                graph[vertex_id].updateAdjacentList([vertex_id - columns,"UP"]) #Up
                graph[vertex_id].updateAdjacentList([vertex_id - 1, "LEFT"]) #Left
                graph[vertex_id].updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                vertex_id = vertex_id + 1
                y = y + 1
            else:
                graph[vertex_id].resetAdjacentList()
                graph[vertex_id].updateAdjacentList([vertex_id - columns,"UP"]) #Up
                graph[vertex_id].updateAdjacentList([vertex_id - 1, "LEFT"]) #Left
                graph[vertex_id].updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                graph[vertex_id].updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_id = vertex_id + 1
                y = y + 1
                
        x = x + 1
        y = 0
    return graph



#### This functions is goint to return a list of vertexs #####
def create_vertex(rows, columns):
    vertex_list = []
    x = 0 #Assign the x position of the node in the grid
    y = 0 #Assign the y position of the node in the grid
    vertex_id = 0
    while(x < rows):
        while(y < columns):
            vertex = Vertex(vertex_id,x,y)
            ####Append the adjacent nodes#####
            if((y == 0) and (x < rows) and (x == 0)): #y = 0 y x = 0
                vertex.updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                vertex.updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == 0) and (x == rows-1)): #y = 0 y x = rows - 1
                vertex.updateAdjacentList([vertex_id - columns,"UP"]) #Up
                vertex.updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == 0) and (x < rows)): #y = 0 y x > 0
                vertex.updateAdjacentList([vertex_id - columns,"UP"]) #Up
                vertex.updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                vertex.updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1
                
            elif((y == columns-1) and (x < rows) and (x == 0)): #y = columns-1 y x = 0
                vertex.updateAdjacentList([vertex_id - 1, "LEFT"]) #Left
                vertex.updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == columns - 1) and (x == rows-1)): #y = columns - 1 y x = rows - 1
                vertex.updateAdjacentList([vertex_id - columns,"UP"]) #Up
                vertex.updateAdjacentList(vertex_id - 1) #Left
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == columns - 1) and (x < rows)): #y = columns - 1 y x = x > 0
                vertex.updateAdjacentList([vertex_id - columns,"UP"]) #Up
                vertex.updateAdjacentList([vertex_id - 1, "LEFT"]) #Left
                vertex.updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1


            elif((y < columns) and (x == 0)): #y < columns y x = 0
                vertex.updateAdjacentList([vertex_id - 1, "LEFT"]) #Left
                vertex.updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                vertex.updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y < columns) and (x == rows - 1)):
                vertex.updateAdjacentList([vertex_id - columns,"UP"]) #Up
                vertex.updateAdjacentList([vertex_id - 1, "LEFT"]) #Left
                vertex.updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1
            else:
                vertex.updateAdjacentList([vertex_id - columns,"UP"]) #Up
                vertex.updateAdjacentList([vertex_id - 1, "LEFT"]) #Left
                vertex.updateAdjacentList([vertex_id + 1, "RIGHT"]) #Right
                vertex.updateAdjacentList([vertex_id + columns, "DOWN"]) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1
                
        x = x + 1
        y = 0
    return vertex_list


### This function is going to rearrange the puzzle ###
def rearrange_puzzle(graph, empty_cell_id, neighbor_id):
    graph[empty_cell_id].setVertexId(neighbor_id)
    graph[neighbor_id].setVertexId(empty_cell_id)
    graph[empty_cell_id],graph[neighbor_id] = graph[neighbor_id],graph[empty_cell_id]
    return graph
    

#### This function is going to go over the list of nodes and return the index of the node ####
def search_vertex(graph_list, vertex_x, vertex_y):
    i = 0
    find_vertex = False
    while(i < len(graph_list)):
        node = graph_list[i]
        if(node.getVertexX() == vertex_x and node.getVertexY() == vertex_y):
            find_vertex = True
            return i
        else:
            i = i + 1


#### This function is going to go over the list of nodes and return the index of the node ####
def search_empty_cell(graph_list):
    i = 0
    find_vertex = False
    while(i < len(graph_list)):
        node = graph_list[i]
        if(node.getVertexValue() == "0"):
            return i
        else:
            i = i + 1

#### This function is going to go over the list of nodes and return the index of the node ####
def has_vertex(graph_list, vertex_id):
    i = 0
    find_vertex = False
    while(i < len(graph_list)):
        node = graph_list[i]
        if(node == vertex_id):
            find_vertex = True
            return find_vertex
        else:
            i = i + 1

    return find_vertex


### This function prints all the travel of PacMan ###
def print_astar(food_index, graph):
    node = graph[food_index]
    father = node.getFather()
    travel_list = []
    i = 0
    while(node.getVertexValue() != "P" ):
        if(node.getFather != 0):
            travel = str(node.getVertexX()) + " " + str(node.getVertexY())
            travel_list.insert(0,travel)
            father = node.getFather()
            node = graph[father]
        else:
            father = node.getFather()
            node = graph[father]

    ##Add the source node
    travel = str(node.getVertexX()) + " " + str(node.getVertexY())
    travel_list.insert(0,travel)

    ## Print the travel
    print(len(travel_list)-1)        
    while(i < len(travel_list)):
        print(travel_list[i])
        i = i + 1
    
        
### This function prints the graph
def print_graph(graph):
    total_of_graphs = len(graph)
    i = 0
    j = 0
    print("Grafo: ")
    while (j < total_of_graphs):
        vertex = graph[j]
        print("El vertice es: ", vertex.getVertexId())
    #    print("Su coordenada x es: ", vertex.getVertexX())
    #    print("Su coordenada y es: ", vertex.getVertexY())
    #    print("Su tipo es: ", vertex.getVertexType())
        print("Su valor es: ", vertex.getVertexValue())
        print("La lista de vertices vecinos es: ", vertex.getAdjacentVertex())
        j = j + 1

def print_list(lista):
    i = 0
    while(i < len(lista)):
        print(lista[i])
        i = i + 1

### This function prints the puzzle
def print_puzzle(graph,rows,columns):
    i = 0
    j = 0
    graph_index = 0
    tiles = ""
    while(i < rows):
        while(j < columns):
            vertex = graph[graph_index]
            tiles = tiles + str(vertex.getVertexValue()) + " "
            j = j + 1
            graph_index = graph_index + 1
        i = i + 1
        print(tiles)
        tiles = ""
        j = 0
    print("")
