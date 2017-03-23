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

    #This method indicates if the vertex has been visited
    def isVisited(self):
        return self.visited

    #This method returns the list of the adjacent vertex
    def getAdjacentVertex(self):
        return self.adjacent_vertex_list

    #This method set the vertex as visited
    def setVisit(self):
        self.visited = True


    #This method updates the adjacent vertex of the vertex, this method receives an string, not an object Vertex
    def updateAdjacentList(self, vertex):
        self.adjacent_vertex_list.append(vertex)





##### This is the method in charge of perform pacman-astar ##################
def pacman_astar():
    entry = input().strip() #Reads the first input
    pacman_initial_position = [int(s) for s in entry.split() if s.isdigit()] ##Separate the two numbers of the first line
    pacman_initial_x =  pacman_initial_position[0] #Get pacman x initial position
    pacman_initial_y =  pacman_initial_position[1] #Get pacman y initial position

    entry = input().strip() #Reads the second input
    food_position = [int(s) for s in entry.split() if s.isdigit()] ##Separate the two numbers of the second line
    food_x = food_position[0] #Get food x position
    food_y = food_position[1] #Get food y position

    entry = input().strip() #Reads the third input
    grid_size = [int(s) for s in entry.split() if s.isdigit()] ##Separate the two numbers of the third line
    rows = grid_size[0] #Get the number of rows
    columns = grid_size[1] #Get the number of columns


    ######Variables need it to convert the grid in a graph##########
    graph = [] #This contains the graphs created
    number_of_nodes = 0 #Variable use in the creation of the graph
    x = 0 #Assign the x position of the node in the grid
    y = 0 #Assign the y position of the node in the grid
   
    list_of_vertex = create_vertex(rows, columns) #Here I call a function to get a list of all the Vertex of the graph
    graph = list_of_vertex #Save the graph created in the graph list
    graph_index = 0 #Index to go over the nodes of the graph
    input_index = 0 #Index to go over the input


    ## Open the file with read only permit
    f = open('case1.txt')
    
    while(number_of_nodes < rows * columns): #Go over the grid and assign the value and the type of the vertex
        line = f.readline().strip()
        input_index = 0 #Index to go over the input
        while(input_index < len(line)):
            if(line[input_index] == "%"):
                graph[graph_index].setVertexType("Wall")
                graph[graph_index].setVertexValue("%")
                graph_index = graph_index + 1
                input_index = input_index + 1
                number_of_nodes = number_of_nodes + 1
                
            elif(line[input_index] == "-"):
                graph[graph_index].setVertexType("Space")
                graph[graph_index].setVertexValue("-")
                graph_index = graph_index + 1
                input_index = input_index + 1
                number_of_nodes = number_of_nodes + 1
                
            elif(line[input_index] == "P"):
                graph[graph_index].setVertexType("PacMan")
                graph[graph_index].setVertexValue("P")
                graph_index = graph_index + 1
                input_index = input_index + 1
                number_of_nodes = number_of_nodes + 1
                
            else:
                graph[graph_index].setVertexType("Food")
                graph[graph_index].setVertexValue(".")
                graph_index = graph_index + 1
                input_index = input_index + 1
                number_of_nodes = number_of_nodes + 1
                
    f.close()
    
    ###Now the graph has been created###
    astar(graph, pacman_initial_x, pacman_initial_y, food_x, food_y, rows, columns)





    
###This function performs the A* algorithm###
def astar(graph, pacman_x, pacman_y, food_x, food_y, rows, columns):   
    graph_index = 0 #This index is used to go over the graph
    stack = [] #This stack is use in the algorithm
    distance = 0 #This is the distance of the edges

    food_cost = 0 #This is the cost if the neighbor is the food
    wall_space_cost = 1 #This is the cost if the neighbor is anything else
    
    open_list = [] #This list is use to introduce nodes that are going to be evaluated
    close_list = [] #This list is use to introduce nodes that were evaluated

    find_food = False #This variable is use to finish the algorithm
    assign_father = False #This variable is use to assign a father to the adjacent nodes
    

    ##Step 0: Add the source cell to the open list
    pacman_initial_vertex_index = search_vertex(graph,pacman_x, pacman_y) #Find the index of the initial pacman
    open_list.append(graph[pacman_initial_vertex_index]) #Add the initial pacman vertex to the open list

    #Beginning of the algorithm
    while(open_list != []):
        #Step 1: Get the first element of the open list
        open_list_element = open_list[0]
        open_list_element_index = search_vertex(graph,open_list_element.getVertexX(), open_list_element.getVertexY())

        #Step 2: Set the open_list_element as visited and get out of the open list
        close_list.append(open_list_element)
        
        graph[open_list_element_index].setVisit() #Set the first open_list vertex as visited
        open_list.pop(0) #Delete the first element of the list

        #Step 3: For each neighbor ...
        open_list_element_neighbors_list = graph[open_list_element.getVertexId()].getAdjacentVertex() #Get the list of adjacent cells
        total_open_list_element_neighbors = len(open_list_element_neighbors_list) #Get the number of neighbors
        i = 0 #Index to go over the list
        assign_father = False
        
        while((i < total_open_list_element_neighbors)):
            neighbor = open_list_element_neighbors_list[i] #Get the ID of an adjacent cell
            is_neighbor_in_open_list = has_vertex(open_list_element_neighbors_list, neighbor) #Get if the element is in the open list
            if(graph[neighbor].getVertexValue() == "."): #Finish the algorithm A*
                find_food = True #PacMan find the food
                graph[neighbor].setFather(open_list_element.getVertexId()) #Set father
                break
              #  print_astar(close_list) #Go and print the travel of A* algorithm
            elif(graph[neighbor].getVertexValue() == "%"): #Simply ignore the Walls(%)
                i = i + 1 #Update the index
            elif(graph[neighbor].isVisited() == True): #If the cell is already visited, we just ignore it
                i = i + 1 #Update the index
            elif(is_neighbor_in_open_list == True and
                 open_list_element.getD() + 1 > graph[neighbor].getD() and assign_father == False): #If the new D is better than the old one
                i = i + 1 #Update the index
                graph[neighbor].setD(open_list_element.getD() + 1)
                h = abs(graph[neighbor].getVertexX() - open_list_element.getVertexX()) + abs(graph[neighbor].getVertexY() - open_list_element.getVertexY())
                graph[neighbor].setH(h)
                graph[neighbor].setCost(open_list_element.getD() + 1 + h)
                graph[neighbor].setFather(open_list_element.getVertexId()) #Set father
                assign_father = True
                open_list.append(graph[neighbor])
          #      print("Entro aqui assign father = false")
            elif (assign_father == True):
                i = i + 1 #Update the index
                graph[neighbor].setD(open_list_element.getD() + 1)
                h = abs(graph[neighbor].getVertexX() - open_list_element.getVertexX()) + abs(graph[neighbor].getVertexY() - open_list_element.getVertexY())
                graph[neighbor].setH(h)
                graph[neighbor].setCost(open_list_element.getD() + 1 + h)
                graph[neighbor].setFather(open_list_element.getVertexId()) #Set father
                open_list.append(graph[neighbor])
           #     print("Entro aqui assign father = true")
            

        #Step 4: Sort the open_list in an ascendent form
    #    open_list = review_open_list(open_list)
        
    
  #  print_astar(close_list) #Go and print the travel of A* algorithm
    food_vertex_index = search_vertex(graph,food_x, food_y) #Find the index of the initial pacman
    print_astar(food_vertex_index, graph) #Go and print the travel of A* algorithm
  #  print_graph(graph)

#### This function sort the open_list in an ascendent form ####
def review_open_list(open_list):
    i = 0
    j = 0
    while(i < len(open_list)):
        while(j + 1 < len(open_list)):
            if(open_list[i].getCost() < open_list[j+1].getCost()):
                temp = open_list[i]
                open_list[i] = open_list[j+1]
                open_list[j+1] = temp
                j = j + 1
            else:
                j = j + 1
        i = i + 1
    return open_list


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
                vertex.updateAdjacentList(vertex_id + 1) #Right
                vertex.updateAdjacentList(vertex_id + columns) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == 0) and (x == rows-1)): #y = 0 y x = rows - 1
                vertex.updateAdjacentList(vertex_id - columns) #Up
                vertex.updateAdjacentList(vertex_id + 1) #Right
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == 0) and (x < rows)): #y = 0 y x > 0
                vertex.updateAdjacentList(vertex_id - columns) #Up
                vertex.updateAdjacentList(vertex_id + 1) #Right
                vertex.updateAdjacentList(vertex_id + columns) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1
                
            elif((y == columns-1) and (x < rows) and (x == 0)): #y = columns-1 y x = 0
                vertex.updateAdjacentList(vertex_id - 1) #Left
                vertex.updateAdjacentList(vertex_id + columns) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == columns - 1) and (x == rows-1)): #y = columns - 1 y x = rows - 1
                vertex.updateAdjacentList(vertex_id - columns) #Up
                vertex.updateAdjacentList(vertex_id - 1) #Left
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y == columns - 1) and (x < rows)): #y = columns - 1 y x = x > 0
                vertex.updateAdjacentList(vertex_id - columns) #Up
                vertex.updateAdjacentList(vertex_id - 1) #Left
                vertex.updateAdjacentList(vertex_id + columns) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1


            elif((y < columns) and (x == 0)): #y < columns y x = 0
                vertex.updateAdjacentList(vertex_id - 1) #Left
                vertex.updateAdjacentList(vertex_id + 1) #Right
                vertex.updateAdjacentList(vertex_id + columns) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1

            elif((y < columns) and (x == rows - 1)):
                vertex.updateAdjacentList(vertex_id - columns) #Up
                vertex.updateAdjacentList(vertex_id - 1) #Left
                vertex.updateAdjacentList(vertex_id + 1) #Right
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1
            else:
                vertex.updateAdjacentList(vertex_id - columns) #Up
                vertex.updateAdjacentList(vertex_id - 1) #Left
                vertex.updateAdjacentList(vertex_id + 1) #Right
                vertex.updateAdjacentList(vertex_id + columns) #Down
                vertex_list.append(vertex)
                vertex_id = vertex_id + 1
                y = y + 1
                
        x = x + 1
        y = 0
    return vertex_list

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
         #   print(travel)
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
        print("Su coordenada x es: ", vertex.getVertexX())
        print("Su coordenada y es: ", vertex.getVertexY())
        print("Su tipo es: ", vertex.getVertexType())
        print("Su valor es: ", vertex.getVertexValue())
        print("Su padre es: ", vertex.getFather())
        print("La lista de vertices vecinos es: ", vertex.getAdjacentVertex())
        j = j + 1
    
