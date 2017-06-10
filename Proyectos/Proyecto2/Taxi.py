###########################################################################################################
# Taxi Class:
##########################################################################################################

class Taxi:
    def __init__(self, taxiId):
        self.taxiId = taxiId 
        self.roadWithClient = []
        self.withClient = False

    def setTaxiId(self,taxiId):
        self.taxiId = taxiId

    def getTaxiId(self):
        return self.taxiId

    def setRoadWithClient(self,road):
        self.roadWithClient = road

    def getRoadWithClient(self):
        return self.roadWithClient

    def setWithClient(self):
        self.withClient = True

    def setWithNoClient(self):
        self.withClient = False

    def getWithClient(self):
        return self.withClient

###########################################################################################################
# TaxiController Class:
##########################################################################################################

class TaxiController:
    def __init__(self, listOfTaxis):
        self.listOfTaxisObjects = []
        self.listOfTaxisNames = listOfTaxis

        #Create all the taxis
        self.createAllTaxis()
        
    #Create an apartment
    def createAllTaxis(self):
        for i in range(0, len(self.listOfTaxisNames)):
            taxiId = self.listOfTaxisNames[i]
            taxi = Taxi(taxiId)
            self.listOfTaxisObjects.append(taxi)

    #Return a taxi object
    def returnTaxi(self, name):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiName = self.listOfTaxisObjects[i].getTaxiId()
            if(taxiName == name):
                return self.listOfTaxisObjects[i]

    #Set taxi road with a client
    def setTaxiRoad(self, road, name):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiName = self.listOfTaxisObjects[i].getTaxiId()
            if(taxiName == name):
                self.listOfTaxisObjects[i].setRoadWithClient(road)
                break

    #Set taxi road with no client
    def setTaxiWithClient(self, name):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiName = self.listOfTaxisObjects[i].getTaxiId()
            if(taxiName == name):
                self.listOfTaxisObjects[i].setWithClient()
                break

    #Set taxi road with no client
    def getTaxiWithClient(self, name):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiName = self.listOfTaxisObjects[i].getTaxiId()
            if(taxiName == name):
                return self.listOfTaxisObjects[i].getWithClient()
                

    #Set taxi road with no client
    def setTaxiWithNoClient(self):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiName = self.listOfTaxisObjects[i].getTaxiId()
            if(taxiName == name):
                self.listOfTaxisObjects[i].setWithNoClient()
                break

    #Set the taxi to no client if they get to its destiny
    def checkAlreadyInDestination(self):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiRoad = self.listOfTaxisObjects[i].getRoadWithClient()
            taxiHaveClient = self.listOfTaxisObjects[i].getWithClient()

            if(taxiRoad == [] and taxiHaveClient == True):
                self.listOfTaxisObjects[i].setWithNoClient()
                

