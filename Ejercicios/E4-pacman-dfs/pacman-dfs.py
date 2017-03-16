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





##### This is the method in charge of perform pacman-dfs ##################
def pacman_dfs():
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
    constraint_error = False #This is used to know where to exit the algorithm
    number_of_nodes = 0 #Variable use in the creation of the graph
    x = 0 #Assign the x position of the node in the grid
    y = 0 #Assign the y position of the node in the grid

    ###First constraint = Max grid 30x30 and rows >= 1 and columns <= 40
    if((rows >= 1) and (columns <= 40) and (rows*columns <= 30*30)):
        list_of_vertex = create_vertex(rows, columns) #Here I call a function to get a list of all the Vertex of the graph
        graph = list_of_vertex #Save the graph created in the graph list
        graph_index = 0 #Index to go over the nodes of the graph
        input_index = 0 #Index to go over the input
        while(number_of_nodes < rows * columns): #Go over the grid and assign the value and the type of the vertex
            entry = input().strip()
            input_index = 0 #Index to go over the input
            while(input_index < len(entry)):
                if(entry[input_index] == "%"):
                    graph[graph_index].setVertexType("Wall")
                    graph[graph_index].setVertexValue("%")
                    graph_index = graph_index + 1
                    input_index = input_index + 1
                    number_of_nodes = number_of_nodes + 1
                elif(entry[input_index] == "-"):
                    graph[graph_index].setVertexType("Space")
                    graph[graph_index].setVertexValue("-")
                    graph_index = graph_index + 1
                    input_index = input_index + 1
                    number_of_nodes = number_of_nodes + 1
                elif(entry[input_index] == "P"):
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

        ###Now the graph has been created###
        DFS(graph, pacman_initial_x, pacman_initial_y, food_x, food_y, rows, columns)
            
    else:
        return "Error: Numero no permitido de filas y columnas"
    


###This function performs the BFS algorithm###
def DFS(graph, pacman_x, pacman_y, food_x, food_y, rows, columns):   
    graph_index = 0 #This index is used to go over the graph
    stack = [] #This stack is use in the algorithm
    distance = 0 #This is the distance of the edges
    pacman_initial_vertex_index = search_vertex(graph,pacman_x, pacman_y) #Find the index of the initial pacman
    graph[pacman_initial_vertex_index].setVisit() #Set the initial pacman vertex as visited
    stack.append(graph[pacman_initial_vertex_index]) #Stack the initial pacman vertex
    total_vertex_neighbors = 0
    visited_vertex_list = []
    
    while(stack != []):
        stack_vertex = stack.pop()
        vertex_neighbors_list = graph[stack_vertex.getVertexId()].getAdjacentVertex()
        total_vertex_neighbors = len(vertex_neighbors_list)
        i = 0
        visited_vertex_list.append(stack_vertex)
        while((i < total_vertex_neighbors)):
            if(total_vertex_neighbors == 4):
                neighbor = vertex_neighbors_list[i]
                if(graph[neighbor].getVertexValue() == "%"):
                    i = i + 1
                elif(graph[neighbor].getVertexValue() == "."):
                    i = i + 1
                    travel = visited_vertex_list + [graph[neighbor]]
                    print_dfs(travel)
                    print(len(travel) - 1)
                    print_dfs(travel)
                else:
                    if(graph[neighbor].isVisited() == False):
                        graph[neighbor].setVisit()
                        stack.append(graph[neighbor])
                        i = i + 1

                    else:
                        i = i + 1
            elif(total_vertex_neighbors == 3):
                neighbor = vertex_neighbors_list[i]
                if(graph[neighbor].getVertexValue() == "%"):
                    i = i + 1
                elif(graph[neighbor].getVertexValue() == "."):
                    i = i + 1
                    travel = visited_vertex_list + [graph[neighbor]]
                    print_dfs(travel)
                    print(len(travel) - 1)
                    print_dfs(travel)
                else:
                    if(graph[neighbor].isVisited() == False):
                        graph[neighbor].setVisit()
                        stack.append(graph[neighbor])
                        i = i + 1
                    else:
                        i = i + 1
            else:
                neighbor = vertex_neighbors_list[i]
                if(graph[neighbor].getVertexValue() == "%"):
                    i = i + 1
                elif(graph[neighbor].getVertexValue() == "."):
                    i = i + 1
                    travel = visited_vertex_list + [graph[neighbor]]
                    print_dfs(travel)
                    print(len(travel) - 1)
                    print_dfs(travel)
                else:
                    if(graph[neighbor].isVisited() == False):
                        graph[neighbor].setVisit()
                        stack.append(graph[neighbor])
                        i = i + 1
                    else:
                        i = i + 1


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
    while(i < len(graph_list)):
        node = graph_list[i]
        if(node.getVertexX() == vertex_x and node.getVertexY() == vertex_y):
            return i
        else:
            i = i + 1


### This function prints all the travel of PacMan ###
def print_dfs(travel_list):
    i = 0
    print(len(travel_list))
    while(i < len(travel_list)):
        print(travel_list[i].getVertexX(), end=" ")
        print(travel_list[i].getVertexY())
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
        print("La lista de vertices vecinos es: ", vertex.getAdjacentVertex())
        j = j + 1
    
