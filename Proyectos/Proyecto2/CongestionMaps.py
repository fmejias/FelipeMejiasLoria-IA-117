import threading
import copy

import taxisimulationgui

class CongestionMaps:
    def __init__(self):
        self.mapDirectory = "MapCongestionFiles/" 
        self.mapFileName = "congestionMap" 
        self.numberOfFile = 1 
        self.idStreets = 1 
        self.listOfStreets = [] 
        self.streetsAlreadySearch = False
        self.cityGraph = []
        self.rows = 0
        self.columns = 0

    def generateMap(self):
        numberOfNewFile = self.mapDirectory + self.mapFileName
        numberOfNewFile = numberOfNewFile + str(self.numberOfFile) + ".txt"
        newFile = open(numberOfNewFile,'w')
        self.cityGraph = copy.deepcopy(taxisimulationgui.returnCityGraph())
        self.rows = 0
        self.columns = 0

        if(self.cityGraph != []):
            self.rows = len(self.cityGraph)
            self.columns = len(self.cityGraph[0])

        if(self.cityGraph != [] and self.streetsAlreadySearch == False):
            self.streetsAlreadySearch = True
            self.searchStreets()

        self.calculateCongestion()
        self.updateCityGraphWithCongestion()

        for i in range(0,self.rows):
            for j in range(0,self.columns):
                stringToWrite = self.cityGraph[i][j].getNodeValue()
                newFile.write(stringToWrite)
            newFile.write("\n")

        newFile.close()
        self.numberOfFile = self.numberOfFile + 1

    def searchStreets(self):
        for i in range(0,self.rows):
            for j in range(0,self.columns):
                if(i+2 < self.rows and self.cityGraph[i][j].getNodeValue() == " "):
                    if(self.cityGraph[i-1][j].getNodeValue() == "-" and
                       self.cityGraph[i+1][j].getNodeValue() == "-"
                       and (self.cityGraph[i+2][j].getNodeValue() == " " or
                            self.cityGraph[i+2][j].getNodeValue().isupper() == True)
                       and (self.cityGraph[i][j-1].getNodeValue() == " " or
                            self.cityGraph[i][j-1].getNodeValue().isdigit() == True)
                       and (self.cityGraph[i][j+1].getNodeValue() == " " or
                            self.cityGraph[i][j+1].getNodeValue().isdigit() == True)):

                        street = [str(self.idStreets), [i,j],0]
                        self.idStreets = self.idStreets + 1
                        self.listOfStreets.append(street)

                    elif(self.cityGraph[i][j-1].getNodeValue() == "|" and
                         self.cityGraph[i][j+1].getNodeValue() == "|"
                       and (self.cityGraph[i+1][j].getNodeValue() == " " or
                            self.cityGraph[i+1][j].getNodeValue().isdigit() == True)
                       and (self.cityGraph[i-1][j].getNodeValue() == " " or
                            self.cityGraph[i-1][j].getNodeValue().isdigit() == True)):

                        street = [str(self.idStreets), [i,j],0]
                        self.idStreets = self.idStreets + 1
                        self.listOfStreets.append(street)

                elif(self.cityGraph[i][j].getNodeValue() == " "):
                    if(self.cityGraph[i-1][j].getNodeValue() == "-"
                       and self.cityGraph[i+1][j].getNodeValue() == "-"
                       and (self.cityGraph[i-2][j].getNodeValue() == " ")
                       and (self.cityGraph[i][j-1].getNodeValue() == " " or
                            self.cityGraph[i][j-1].getNodeValue().isdigit() == True)
                       and (self.cityGraph[i][j+1].getNodeValue() == " " or
                            self.cityGraph[i][j+1].getNodeValue().isdigit() == True)):

                        street = [str(self.idStreets), [i,j], 0]
                        self.idStreets = self.idStreets + 1
                        self.listOfStreets.append(street)

    def calculateCongestion(self):
        for i in range(0, len(self.listOfStreets)):
            street = self.listOfStreets[i]
            x = street[1][0]
            y = street[1][1]
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

            self.listOfStreets[i][2] = numberOfCars

    def updateCityGraphWithCongestion(self):
        for i in range(0, len(self.listOfStreets)):
            street = self.listOfStreets[i]
            x = street[1][0]
            y = street[1][1]
            self.cityGraph[x][y].setNodeValue(str(street[2]))

directionsOfTaxis = ""
congestionMapGenerator = CongestionMaps()

def generateCongestionMaps():
    global congestionMapGenerator 
    congestionMapGenerator.generateMap() 
    threading.Timer(5, generateCongestionMaps).start()
    
def returnTaxisDirections():
    global congestionMapGenerator
    global directionsOfTaxis
    directionsOfTaxis = congestionMapGenerator.getTaxisDirections()
    return directionsOfTaxis
