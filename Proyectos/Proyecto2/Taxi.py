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

class TaxiController:
    def __init__(self, listOfTaxis):
        self.listOfTaxisObjects = []
        self.listOfTaxisNames = listOfTaxis
        self.createAllTaxis()

    def createAllTaxis(self):
        for i in range(0, len(self.listOfTaxisNames)):
            taxiId = self.listOfTaxisNames[i]
            taxi = Taxi(taxiId)
            self.listOfTaxisObjects.append(taxi)

    def returnTaxi(self, name):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiName = self.listOfTaxisObjects[i].getTaxiId()
            if(taxiName == name):
                return self.listOfTaxisObjects[i]

    def setTaxiRoad(self, road, name):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiName = self.listOfTaxisObjects[i].getTaxiId()
            if(taxiName == name):
                self.listOfTaxisObjects[i].setRoadWithClient(road)
                break

    def setTaxiWithClient(self, name):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiName = self.listOfTaxisObjects[i].getTaxiId()
            if(taxiName == name):
                self.listOfTaxisObjects[i].setWithClient()
                break

    def getTaxiWithClient(self, name):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiName = self.listOfTaxisObjects[i].getTaxiId()
            if(taxiName == name):
                return self.listOfTaxisObjects[i].getWithClient()

    def setTaxiWithNoClient(self):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiName = self.listOfTaxisObjects[i].getTaxiId()
            if(taxiName == name):
                self.listOfTaxisObjects[i].setWithNoClient()
                break

    def checkAlreadyInDestination(self):
        for i in range(0, len(self.listOfTaxisObjects)):
            taxiRoad = self.listOfTaxisObjects[i].getRoadWithClient()
            taxiHaveClient = self.listOfTaxisObjects[i].getWithClient()

            if(taxiRoad == [] and taxiHaveClient == True):
                self.listOfTaxisObjects[i].setWithNoClient()

    
                

