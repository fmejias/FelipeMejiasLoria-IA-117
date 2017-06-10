###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################

import TaxiSimulationGraphicalInterface
import threading
import copy

###########################################################################################################
# CongestionMaps Class:
# Attributes:
# Methods:
#
##########################################################################################################
class CongestionMaps:
    def __init__(self):
        self.mapDirectory = "MapCongestionFiles/" #Directory of the congestion maps
        self.mapFileName = "congestionMap" #Name of the congestion map file
        self.numberOfFile = 1 #This number is used to write different files
        self.idStreets = 1 #Contains the number to assign to the streets
        self.listOfStreets = [] #["idStreet",[x,y], congestion]
        self.streetsAlreadySearch = False
        self.cityGraph = []
        self.rows = 0
        self.columns = 0
        
    #This method is use to create a new file of maxNumberOfCharacters x maxNumberOfCharacters
    def generateMap(self):
        numberOfNewFile = self.mapDirectory + self.mapFileName + str(self.numberOfFile) + ".txt"
        newFile = open(numberOfNewFile,'w')

        #Read the city graph
        self.cityGraph = copy.deepcopy(TaxiSimulationGraphicalInterface.returnCityGraph())
        self.rows = 0
        self.columns = 0

        #Get the number of rows and columns
        if(self.cityGraph != []):
            self.rows = len(self.cityGraph)
            self.columns = len(self.cityGraph[0])

        #Checks if if has to calculate all of the streets
        if(self.cityGraph != [] and self.streetsAlreadySearch == False):
            self.streetsAlreadySearch = True
            self.searchStreets()

        
        #Calculate the congestion on the map
        self.calculateCongestion()

        #Update the city with the congestion
        self.updateCityGraphWithCongestion()
    
        #Go over all the matrix
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                stringToWrite = self.cityGraph[i][j].getNodeValue()
                newFile.write(stringToWrite)

            #Write a newline
            newFile.write("\n")

        #Close all the files
        newFile.close()

        #Increment the number of file
        self.numberOfFile = self.numberOfFile + 1

    #This method search all of the streets
    def searchStreets(self):
        #Go over all the matrix
        for i in range(0,self.rows):
            for j in range(0,self.columns):

                if(i+2 < self.rows and self.cityGraph[i][j].getNodeValue() == " "):
                    #Check if the block is a street
                    if(self.cityGraph[i-1][j].getNodeValue() == "-" and self.cityGraph[i+1][j].getNodeValue() == "-"
                       and (self.cityGraph[i+2][j].getNodeValue() == " " or self.cityGraph[i+2][j].getNodeValue().isupper() == True)
                       and (self.cityGraph[i][j-1].getNodeValue() == " " or self.cityGraph[i][j-1].getNodeValue().isdigit() == True)
                       and (self.cityGraph[i][j+1].getNodeValue() == " " or self.cityGraph[i][j+1].getNodeValue().isdigit() == True)):

                        #Append the street coordinate
                        street = [str(self.idStreets), [i,j],0]
                        self.idStreets = self.idStreets + 1
                        self.listOfStreets.append(street)

                    #Check if the block is a street
                    elif(self.cityGraph[i][j-1].getNodeValue() == "|" and self.cityGraph[i][j+1].getNodeValue() == "|"
                       and (self.cityGraph[i+1][j].getNodeValue() == " " or self.cityGraph[i+1][j].getNodeValue().isdigit() == True)
                       and (self.cityGraph[i-1][j].getNodeValue() == " " or self.cityGraph[i-1][j].getNodeValue().isdigit() == True)):

                        #Append the street coordinate
                        street = [str(self.idStreets), [i,j],0]
                        self.idStreets = self.idStreets + 1
                        self.listOfStreets.append(street)

                elif(self.cityGraph[i][j].getNodeValue() == " "):
                    #Check if the block is a street
                    if(self.cityGraph[i-1][j].getNodeValue() == "-" and self.cityGraph[i+1][j].getNodeValue() == "-"
                       and (self.cityGraph[i-2][j].getNodeValue() == " ")
                       and (self.cityGraph[i][j-1].getNodeValue() == " " or self.cityGraph[i][j-1].getNodeValue().isdigit() == True)
                       and (self.cityGraph[i][j+1].getNodeValue() == " " or self.cityGraph[i][j+1].getNodeValue().isdigit() == True)):

                        #Append the street coordinate
                        street = [str(self.idStreets), [i,j], 0]
                        self.idStreets = self.idStreets + 1
                        self.listOfStreets.append(street)


    #This method is in charge of calculate the congestion on the street
    def calculateCongestion(self):

        #Iterate for all of the streets
        for i in range(0, len(self.listOfStreets)):
            street = self.listOfStreets[i]
            x = street[1][0]
            y = street[1][1]

            #Checks how many cars are on the street
            numberOfCars = 0

            if(self.cityGraph[x][y].getNodeValue().isdigit() == True):
                numberOfCars = numberOfCars + 1
            if(self.cityGraph[x][y-1].getNodeValue().isdigit() == True):
                numberOfCars = numberOfCars + 1
            if(self.cityGraph[x][y+1].getNodeValue().isdigit() == True):
                numberOfCars = numberOfCars + 1
            if(self.cityGraph[x-1][y].getNodeValue().isdigit() == True):
                numberOfCars = numberOfCars + 1
            if(self.cityGraph[x+1][y].getNodeValue().isdigit() == True):
                numberOfCars = numberOfCars + 1

            #Append the value of congestion of the street
            self.listOfStreets[i][2] = numberOfCars

    #This method writes the value of congestion on the street for the city graph
    def updateCityGraphWithCongestion(self):
        #Iterate for all of the streets
        for i in range(0, len(self.listOfStreets)):
            street = self.listOfStreets[i]
            x = street[1][0]
            y = street[1][1]

            #Change the value
            self.cityGraph[x][y].setNodeValue(str(street[2]))


##Declaration of some global variables to comunicate with the Threads
directionsOfTaxis = ""
congestionMapGenerator = CongestionMaps()

#This function is in charge of call the generate map every 5 seconds
def generateCongestionMaps():
    global congestionMapGenerator #Declaration of the global CongestionMapGenerator object
    congestionMapGenerator.generateMap() #Call the function to generate the congestion maps
    threading.Timer(5, generateCongestionMaps).start() #Every 5 seconds call the generation function

#This function returns the best directions of the taxis
def returnTaxisDirections():
    global congestionMapGenerator
    global directionsOfTaxis
    directionsOfTaxis = congestionMapGenerator.getTaxisDirections()
    return directionsOfTaxis
