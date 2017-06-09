import random
import Client

###########################################################################################################
# Apartment Class:
##########################################################################################################

class Apartment:
    def __init__(self, name, numberOfClients, leaveSchedule, arriveSchedule):
        self.apartmentName = name
        self.numberOfClients = numberOfClients
        self.leaveSchedule = leaveSchedule
        self.arriveSchedule = arriveSchedule
        self.listOfClients = []
        self.actualNumberOfClientsInTheBuilding = int(numberOfClients)
        self.putAClient = True

    def setPutAClient(self,value):
        self.putAClient = value

    def getPutAClient(self):
        return self.putAClient
    
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

    def subtractClientsInTheBuilding(self):
        self.actualNumberOfClientsInTheBuilding = self.actualNumberOfClientsInTheBuilding - 1

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
    def __init__(self, name):
        self.workplaceName = name 
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


###########################################################################################################
# ApartmentController Class:
##########################################################################################################

class ApartmentController:
    def __init__(self):
        self.listOfApartments = []
        self.leaveApartmentHours = ["07:00", "07:30", "08:00", "08:30"]
        self.arriveApartmentHours = ["05:00", "05:30", "06:00", "06:30", "07:00"]

    #Create an apartment
    def addApartment(self,name, numberOfClients, workplace):
        leaveSchedule = random.choice(self.leaveApartmentHours)
        arriveSchedule = random.choice(self.arriveApartmentHours)
        newApartment = Apartment(name, numberOfClients, leaveSchedule, arriveSchedule)
        self.listOfApartments.append(newApartment)

        #Add all of the clients of the apartment
        self.addClientsToApartment(name, workplace, leaveSchedule, arriveSchedule, numberOfClients)

    #This method add all of the clients of the apartment
    def addClientsToApartment(self, apartment, workplace, leaveSchedule, arriveSchedule, numberOfClients):
        for i in range(0, int(numberOfClients)):

            #Create the client
            client = Client.Client()
            client.setApartment(apartment)
            client.setWorkplace(workplace)
            client.setLeaveSchedule(leaveSchedule)
            client.setArriveSchedule(arriveSchedule)

            #Add the client to the Apartment
            self.listOfApartments[len(self.listOfApartments)-1].addClientToApartment(client)

    #Get the leave and arrive schedule of an specific apartment
    def getLeaveArriveSchedule(self, apartmentName):
        leaveSchedule = []
        arriveSchedule = []

        for i in range(0, len(self.listOfApartments)):
            apartment = self.listOfApartments[i]
            if(apartment.getApartmentName() == apartmentName):
                leaveSchedule = apartment.getLeaveSchedule()
                arriveSchedule = apartment.getArriveSchedule()
                break

        return [leaveSchedule, arriveSchedule]

    #This method check which apartment need to send clients to work(Lista asi: [["A", True], ["B", True]]) (NombreEdificio, putAClient)
    def checkClientsToGoToWork(self, time):
        listOfApartmentsToGoToWork = []
        for i in range(0, len(self.listOfApartments)):
            apartment = self.listOfApartments[i]
            if(apartment.getLeaveSchedule() == time and apartment.actualNumberOfClientsInTheBuilding > 0):
                listOfApartmentsToGoToWork.append([apartment.getApartmentName(), apartment.getPutAClient()])
                apartment.setPutAClient(False) #This value change after the taxi grabbed the client

        return listOfApartmentsToGoToWork

    #This method is called when a client grabbed a taxi, so there is less people in the apartment
    def clientGrabbedATaxi(self, apartmentName):
        for i in range(0, len(self.listOfApartments)):
            apartment = self.listOfApartments[i]
            if(apartment.getApartmentName() == apartmentName):
                apartment.subtractClientsInTheBuilding()
                apartment.setPutAClient(True)
    
    #Return the list with all of the Apartments
    def getListOfApartments(self):
        return self.listOfApartments

###########################################################################################################
# WorkplaceController Class:
##########################################################################################################

class WorkplaceController:
    def __init__(self):
        self.listOfWorkplaces = []
        
    def addWorkplace(self,name):
        newWorkplace = Workplace(name)
        self.listOfWorkplaces.append(newWorkplace)

    def getListOfWorkplaces(self):
        return self.listOfWorkplaces
