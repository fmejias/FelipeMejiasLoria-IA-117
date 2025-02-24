###This import is necessary to get a Python queue #####
import queue

####This class represent a vertex of the graph ####
class Vertex:
    ###
    # self.vertex_id = contains the label of the vertex
    # self.visited = indicates if the node has been visited
    # self.adjacent_vertex_list = contains all of the adjacent vertex of the vertex
    # self.distance_from_s = this is the distance from the node s to that vertex
    # self.initial_node = indicates if it is the initial node
    # self.father = indicates if the node has a father
    ###
    def __init__(self,vertex_id):
        self.vertex_id = vertex_id
        self.visited = False
        self.adjacent_vertex_list = []
        self.distance_from_s = -1
        self.initial_node = False
        self.father = False
        self.distance = 0

    #This method return the vertex id
    def getVertexId(self):
        return self.vertex_id

    #This method return if it is the initial node
    def isInitialNode(self):
        return self.initial_node

    #This method indicates if the vertex has been visited
    def isVisited(self):
        return self.visited

    #This method returns the list of the adjacent vertex
    def getAdjacentVertex(self):
        return self.adjacent_vertex_list

    #This method returns the distance from s
    def getDistanceFromS(self):
        return self.distance_from_s

    #This method returns the distance
    def getDistance(self):
        return self.distance

    #This method returns the distance 
    def setDistance(self,distance):
        self.distance =  distance

    #This method update the distance of the search
    def updateDistance(self):
        self.distance_from_s = self.distance * 6

    #This method set the vertex as visited
    def setVisit(self):
        self.visited = True

    #This method set father = True, to indicates that the node has a father
    def setFather(self):
        self.father = True

    #This method indicates if the node has father
    def hasFather(self):
        return self.father

    #This method set the initial node 
    def setInitialNode(self):
        self.initial_node = True

    #This method updates the adjacent vertex of the vertex, this method receives an string, not an object Vertex
    def updateAdjacentList(self, vertex):
        self.adjacent_vertex_list.append(vertex)





##### This is the method to do the breadth first search(BFS) ##################
def bfsshortreach():
    number_of_queries = int(input()) #This contains the number of queries
    graphs = [] #This contains all of the graphs created
    graph_index = 0 #This index is used when a new graph has to be created
    first_line = True #This is used to know the number of nodes and edges
    constraint_error = False #This is used to know where to exit the algorithm
    number_of_nodes = 0
    numbers = []
    s_vertex = 0
    if(number_of_queries >= 1 and number_of_queries <= 10):
        ###This cycle creates the graphs
        while(number_of_queries > 0):
            entry = input().strip()
            numbers = [int(s) for s in entry.split() if s.isdigit()]
            if(len(numbers) == 1):
                numbers = [int(s) for s in entry.split() if s.isdigit()]
                initial_vertex = int(numbers[0]) #Get the s vertex
                s_vertex = initial_vertex
                vertex_index = search_vertex(graphs[graph_index], initial_vertex) #Find the position on the list of the vertex
                graphs[graph_index][vertex_index].setInitialNode() #Set that node as the initial node
                number_of_queries = number_of_queries - 1 #Pass to another graph
                first_line = True 
                graph_index = graph_index + 1

                if(s_vertex < 1 or s_vertex > number_of_nodes):
                    constraint_error = True
                    number_of_queries = 0
            elif(first_line == True):
                numbers = [int(s) for s in entry.split() if s.isdigit()]
                number_of_nodes = int(numbers[0]) #gets the number of nodes of the graph
                number_of_edges = int(numbers[1]) #gets the number of edges
                if((number_of_nodes < 2) or (number_of_nodes > 1000)):
                    constraint_error = True
                    number_of_queries = 0
                elif((number_of_edges < 1) or (number_of_edges > ((number_of_nodes*(number_of_nodes - 1)))/2) ):
                    constraint_error = True
                    number_of_queries = 0
                else:
                    list_of_vertex = create_vertex(number_of_nodes) #Here I call a function to get a list of Vertex
                    graphs.append(list_of_vertex) #Save the graph created in the graph list
                    first_line = False
            else:
                numbers = [int(s) for s in entry.split() if s.isdigit()]
                initial_vertex = int(numbers[0]) #Get the initial vertex
                final_vertex = int(numbers[1]) #Get the neighbor vertex of the initial vertex

                if(initial_vertex < 1 or initial_vertex > number_of_nodes):
                    constraint_error = True
                    number_of_queries = 0
                elif(final_vertex < 1 or final_vertex > number_of_nodes):
                    constraint_error = True
                    number_of_queries = 0
                else:
                    vertex_index = search_vertex(graphs[graph_index],initial_vertex) #Find the position on the list of the vertex
                    adjacent_list = graphs[graph_index][vertex_index].getAdjacentVertex() #Get the list of adjacent vertex of the node initial vertex
                    if(search_neighbor(adjacent_list, final_vertex) == False):
                        graphs[graph_index][vertex_index].updateAdjacentList(final_vertex) #Update the adjacent list of the vertex

                    vertex_index = search_vertex(graphs[graph_index],final_vertex) #Find the position on the list of the vertex
                    graphs[graph_index][vertex_index].setFather() #Set father = true
                    adjacent_list = graphs[graph_index][vertex_index].getAdjacentVertex() #Get the list of adjacent vertex of the node final vertex
                    if(search_neighbor(adjacent_list, initial_vertex) == False):
                        graphs[graph_index][vertex_index].updateAdjacentList(initial_vertex) #Update the adjacent list of the vertex                    


        if(constraint_error == True):
            print("Error")

        elif (constraint_error == False):
            #Call the function to do the BFS
            BFS(graphs)

            #This function prints the graphs results
            print_bfsshortreach_results(graphs)

            #This function prints the graphs
            print_graphs(graphs)

    else:
        print("Error")


###This function performs the BFS algorithm###
def BFS(graphs):
    number_of_graphs = len(graphs) #Contains the total of graphs
    graph_index = 0 #This index is used to go over the graphs
    q = queue.Queue() #This queue is use in the algorithm
    distance = 0 #This is the distance of the edges

    s_vertex_index = search_s_vertex(graphs[graph_index]) #Find the index and the id of the s vertex
    graphs[graph_index][s_vertex_index].setVisit() #Set the S vertex as visited
    q.put(graphs[graph_index][s_vertex_index]) #Enqueue the the S vertex

    hasFather = True #This variable is use to indicate if the node has a father
    
    ###This cycle realize the search
    while(number_of_graphs > 0):

        if(q.empty() == True and (number_of_graphs - 1) > 0):
            graph_index = graph_index + 1
            s_vertex_index = search_s_vertex(graphs[graph_index]) #Find the index and the id of the s vertex
            graphs[graph_index][s_vertex_index].setVisit() #Set the S vertex as visited
            q.put(graphs[graph_index][s_vertex_index]) #Enqueue the the S vertex
            number_of_graphs = number_of_graphs - 1
            distance = 0

        elif(q.empty() == False):
            vertex = q.get() #Get a vertex of the queue
            adjacent_list = vertex.getAdjacentVertex() #Get the list of adjacent vertex of the vertex
            distance = distance + 6 #Here we update the distance
            i = 0
            while (i < len(adjacent_list)):
                adjacent_index = search_vertex(graphs[graph_index],adjacent_list[i])
                if(graphs[graph_index][adjacent_index].isVisited() == False):
                    graphs[graph_index][adjacent_index].setVisit() #This mark the node as visited
                    graphs[graph_index][adjacent_index].setDistance(vertex.getDistance() + 1)
                    graphs[graph_index][adjacent_index].updateDistance() #This update the distance of the vertex
                    q.put(graphs[graph_index][adjacent_index]) #This enqueue the neighbor node
                    
                    i = i +1
                else:
                    i = i + 1
                     
        else:
            number_of_graphs = number_of_graphs - 1
    
    

#### This functions is goint to return a list of vertexs #####
def create_vertex(number_of_nodes):
    vertex_list = []
    i = 0
    vertex_id = 1
    while(i < number_of_nodes):
        vertex = Vertex(vertex_id)
        vertex_list.append(vertex)
        i = i + 1
        vertex_id = vertex_id + 1
    return vertex_list
    

#### This function is going to go over the list of nodes and return the index of the node ####
def search_vertex(graph_list, vertex):
    i = 0
    while(i < len(graph_list)):
        node = graph_list[i]
        if(node.getVertexId() == vertex):
            return i
        else:
            i = i + 1

#### This function is going to go over the list of nodes and return the index of the node ####
def search_neighbor(graph_list, vertex):
    i = 0
    result = False
    while(i < len(graph_list)):
        node = graph_list[i]
        if(node == vertex):
            result = True
            i = i + 1
           # return result
        else:
            i = i + 1
    return result

#### This function is going to go over the list of nodes and return the index of the node and the id ####
def search_s_vertex(graph_list):
    i = 0
    while(i < len(graph_list)):
        node = graph_list[i]
        if(node.isInitialNode() == True):
            return i
        else:
            i = i + 1


### This function prints the results ###
def print_bfsshortreach_results(graphs):
    total_of_graphs = len(graphs)
    i = 0
    j = 0
    while (i < total_of_graphs):
        if(j == len(graphs[i])):
            i = i + 1
            j = 0
            print()
        else:
            vertex = graphs[i][j]
            if(vertex.isInitialNode() == False):
                print(vertex.getDistanceFromS(), end=" ")
                j = j + 1
            else:
                j = j + 1
                
            
### This function prints the graphs
def print_graphs(graphs):
    total_of_graphs = len(graphs)
    i = 0
    j = 0
    print("Grafo: ")
    while (i < total_of_graphs):
        if(j == len(graphs[i])):
            i = i + 1
            j = 0
            print(" ")
            print("Grafo: ")
            
        else:
            vertex = graphs[i][j]
            print("El vertice es: ", vertex.getVertexId())
          #  print("Tiene nodo padre: ", vertex.hasFather())
            print("La distancia del nodo s hasta aquí es: ", vertex.getDistance())
       #     print("La lista de vertices vecinos es: ", vertex.getAdjacentVertex())
            j = j + 1
    
