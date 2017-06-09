###########################################################################################################
# Apartment Class:
##########################################################################################################

class Apartment:
    def __init__(self):
        self.apartmentName = "" 
        self.numberOfClients = 0
        self.leaveSchedule = ""
        self.arriveSchedule = ""
        self.listOfClients = []

    #This method set the apartmentName
    def setApartmentName(self,name):
        self.apartmentName = name

    #This method get the apartment name
    def getApartmentName(self):
        return self.apartmentName

    #This method set the number of clients in the apartment
    def setNumberOfClients(self,numberOfClients):
        self.numberOfClients = numberOfClients

    #This method get the number of clients in the apartment
    def getNumberOfClients(self):
        return self.numberOfClients

    def setLeaveSchedule(self,leaveSchedule):
        self.leaveSchedule = leaveSchedule

    def getLeaveSchedule(self):
        return self.leaveSchedule

    def setArriveSchedule(self,arriveSchedule):
        self.arriveSchedule = arriveSchedule

    def getArriveSchedule(self):
        return self.arriveSchedule

    def addClientToApartment(self, client):
        self.listOfClients.append(client)

    def getApartmentClients(self):
        return self.listOfClients
        
    
###########################################################################################################
# Workplace Class:
##########################################################################################################

class Workplace:
    def __init__(self):
        self.workplaceName = "" 
        self.listOfWorkers = []
        self.numberOfWorkers = 0

    def setWorkplaceName(self,name):
        self.workplaceName = name

    def getWorkplaceName(self):
        return self.workplaceName

    def setNumberOfWorkers(self,numberOfWorkers):
        self.numberOfWorkers = numberOfWorkers

    def getNumberOfWorkers(self):
        return self.numberOfWorkers

    def addWorker(self, worker):
        self.listOfWorkers.append(worker)

    def getWorkplaceWorkers(self):
        return self.listOfWorkers
