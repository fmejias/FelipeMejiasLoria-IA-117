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
    ###
    def __init__(self,vertex_id):
        self.vertex_id = vertex_id
        self.visited = False
        self.adjacent_vertex_list = []
        self.distance_from_s = -1
        self.initial_node = False

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

    #This method update the distance of the search
    def updateDistance(self,distance):
        self.distance_from_s = distance

    #This method set the vertex as visited
    def setVisit(self):
        self.visited = True

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
    
    ###This cycle creates the graphs
    while(number_of_queries > 0):
        entry = input().strip()
        if(len(entry) == 1):
            initial_vertex = int(entry[0]) #Get the s vertex
            vertex_index = search_vertex(graphs[graph_index], initial_vertex) #Find the position on the list of the vertex
            graphs[graph_index][vertex_index].setInitialNode() #Set that node as the initial node
            number_of_queries = number_of_queries - 1 #Pass to another graph
            first_line = True 
            graph_index = graph_index + 1 
        elif(first_line == True):
            number_of_nodes = int(entry[0]) #gets the number of nodes of the graph
            list_of_vertex = create_vertex(number_of_nodes) #Here I call a function to get a list of Vertex
            graphs.append(list_of_vertex) #Save the graph created in the graph list
            first_line = False
        else:
            initial_vertex = int(entry[0]) #Get the initial vertex
            final_vertex = int(entry[2]) #Get the neighbor vertex of the initial vertex
            vertex_index = search_vertex(graphs[graph_index],initial_vertex) #Find the position on the list of the vertex
            graphs[graph_index][vertex_index].updateAdjacentList(final_vertex) #Update the adjacent list of the vertex

    #Call the function to do the BFS
    BFS(graphs)

    #This function prints the graphs results
    print_bfsshortreach_results(graphs)


###This function performs the BFS algorithm###
def BFS(graphs):
    number_of_graphs = len(graphs) #Contains the total of graphs
    graph_index = 0 #This index is used to go over the graphs
    q = queue.Queue() #This queue is use in the algorithm
    distance = 0 #This is the distance of the edges

    s_vertex_index = search_s_vertex(graphs[graph_index]) #Find the index and the id of the s vertex
    graphs[graph_index][s_vertex_index].setVisit() #Set the S vertex as visited
    q.put(graphs[graph_index][s_vertex_index]) #Enqueue the the S vertex
    
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
                    graphs[graph_index][adjacent_index].updateDistance(distance) #This update the distance of the vertex
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
            print("La distancia del nodo s hasta aquí es: ", vertex.getDistanceFromS())
            print("La lista de vertices vecinos es: ", vertex.getAdjacentVertex())
            j = j + 1
    
