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
        self.listOfClientsWaitingATaxi = [] #This list contains all of the clients that needs a taxi
        self.clientsAlreadyWaitingForATaxi = False

    #This two methods indicates if a client has to be waiting for a taxi
    def setPutAClient(self,value):
        self.putAClient = value

    #This two methods indicates if a client has to be waiting for a taxi
    def areClientsWaitingForTaxi(self):
        if(len(self.listOfClientsWaitingATaxi) >= 1):
            return True
        else:
            return False

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

    #This method return the list with all of the clients waiting for a taxi
    def clientsThatNeedToGoWork(self, time):

        #Checks if the client has to go home
        if(self.leaveSchedule == time and self.clientsAlreadyWaitingForATaxi == False):

            #Get the number of clients of the same apartment
            numberOfClients = self.numberOfClients

            #Append all of the clients in the list of waiting for a taxi
            for j in range(0,int(numberOfClients)):
                self.listOfClientsWaitingATaxi.insert(0, self.listOfClients[j])

            #Append the name of the apartment to no repeat the clients on the list
            self.clientsAlreadyWaitingForATaxi = True

        return self.listOfClientsWaitingATaxi

    #This method return a client waiting for a taxi
    def getClientWaitingForATaxi(self):
        return self.listOfClientsWaitingATaxi[len(self.listOfClientsWaitingATaxi)-1]

    #This method get the number of clients waiting for a taxi
    def getNumberOfClientsWaitingForATaxi(self):
        return len(self.listOfClientsWaitingATaxi)

    #This method pop a client from the list when it grabbed a taxi
    def clientGrabbedATaxi(self):
        if(len(self.listOfClientsWaitingATaxi) >= 1):
            self.listOfClientsWaitingATaxi.pop()

        
    
###########################################################################################################
# Workplace Class:
##########################################################################################################

class Workplace:
    def __init__(self, name):
        self.workplaceName = name 
        self.listOfWorkers = []
        self.numberOfWorkers = 0
        self.actualNumberOfClientsInTheWorkplace = 0
        self.listOfClientsWaitingATaxi = [] #This list contains all of the clients that needs a taxi
        self.listOfClientsApartmentWaitingATaxi = [] #This list works to not append repeated clients
        self.clientsAlreadyWaitingForATaxi = False
        self.timeToLeave = "09:00"
        self.putAClient = True

    #This two methods indicates if a client has to be waiting for a taxi
    def setPutAClient(self,value):
        self.putAClient = value

    def getPutAClient(self):
        return self.putAClient
    
    def setWorkplaceName(self,name):
        self.workplaceName = name

    def getWorkplaceName(self):
        return self.workplaceName

    def setNumberOfWorkers(self,numberOfWorkers):
        self.numberOfWorkers = numberOfWorkers

    def getNumberOfWorkers(self):
        return self.numberOfWorkers

    #Add in a list a worker of that workplace
    def addWorker(self, worker):
        self.numberOfWorkers = self.numberOfWorkers + 1
        self.listOfWorkers.append(worker)

    def getWorkplaceWorkers(self):
        return self.listOfWorkers

    def incrementNumberOfClientsInTheWorkplace(self):
        self.actualNumberOfClientsInTheWorkplace = self.actualNumberOfClientsInTheWorkplace + 1

    def decrementNumberOfClientsInTheWorkplace(self):
        self.actualNumberOfClientsInTheWorkplace = self.actualNumberOfClientsInTheWorkplace - 1

    #This method return the number of clients on each apartment
    def numberOfClientsForEachApartment(self, apartmentName):
        numberOfClients = 0
        for i in range(0, len(self.listOfWorkers)):
            client = self.listOfWorkers[i]
            clientApartment = client.getApartment()
            if(clientApartment == apartmentName):
                numberOfClients = numberOfClients + 1

        return numberOfClients
    
    #This method return the list with all of the clients waiting for a taxi
    def clientsThatNeedToGoHome(self, time):
        #Checks if the client has to go home
        if(self.timeToLeave == time and self.clientsAlreadyWaitingForATaxi == False):

            #Get the number of clients of the same apartment
            numberOfWorkers = self.numberOfWorkers

            #Append all of the clients in the list of waiting for a taxi
            for j in range(0,numberOfWorkers):
                self.listOfClientsWaitingATaxi.insert(0, self.listOfWorkers[j])

            #Append the name of the apartment to no repeat the clients on the list
            self.clientsAlreadyWaitingForATaxi = True

        return self.listOfClientsWaitingATaxi

    #This method return a client waiting for a taxi
    def getClientWaitingForATaxi(self):
        return self.listOfClientsWaitingATaxi[len(self.listOfClientsWaitingATaxi)-1]

    #This method get the number of clients waiting for a taxi
    def getNumberOfClientsWaitingForATaxi(self):
        return len(self.listOfClientsWaitingATaxi)

    #This method pop a client from the list when it grabbed a taxi
    def clientGrabbedATaxi(self):
        if(len(self.listOfClientsWaitingATaxi) >= 1):
            self.listOfClientsWaitingATaxi.pop()

    #This method indicates if the workplace has clients that need to go home, is use for the GUI
    def checkClientsToGoHome(self, time):
        clientsWaiting = False
        self.clientsThatNeedToGoHome(time)
        if(len(self.listOfClientsWaitingATaxi) >= 1):
            clientsWaiting = True
        else:
            clientsWaiting = False

        return clientsWaiting
        


###########################################################################################################
# ApartmentController Class:
##########################################################################################################

class ApartmentController:
    def __init__(self, listOfWorkplaces):
        self.listOfApartments = []
        self.listOfApartmentNames = []
        self.leaveApartmentHours = ["07:00", "08:00"]
        self.arriveApartmentHours = ["09:00"]
        self.workplaceController = WorkplaceController(listOfWorkplaces)

    #Create an apartment
    def addApartment(self,name, numberOfClients, workplace):
        leaveSchedule = random.choice(self.leaveApartmentHours)
        arriveSchedule = random.choice(self.arriveApartmentHours)
        newApartment = Apartment(name, numberOfClients, leaveSchedule, arriveSchedule)
        self.listOfApartments.append(newApartment)
        self.listOfApartmentNames.append(name)

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

            #Add a client to the workplace
            self.workplaceController.addClientToWorkplace(workplace, client)

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
                self.listOfApartments[i].setPutAClient(False) #This value change after the taxi grabbed the client
        return listOfApartmentsToGoToWork

    #This method check which apartment need to send clients to work(Lista asi: [["A", True], ["B", True]]) (NombreEdificio, putAClient)
    def checkClientsToEraseFromApartment(self):
        listOfApartmentsToGoToWork = []
        for i in range(0, len(self.listOfApartments)):
            apartment = self.listOfApartments[i]
            if(apartment.getNumberOfClientsWaitingForATaxi() == 0):
                listOfApartmentsToGoToWork.append([apartment.getApartmentName(), apartment.getPutAClient()])
        return listOfApartmentsToGoToWork

    ###Get the list with all of the clients that need to go to work from an specific apartment##
    def getClientsToGoToWork(self, apartmentName, time):
        for i in range(0, len(self.listOfApartments)):
            apartment = self.listOfApartments[i]
            if(apartment.getApartmentName() == apartmentName):
                return apartment.clientsThatNeedToGoWork(time)
                

    #This method is called when a client grabbed a taxi, so there is less people in the apartment
    def clientGrabbedATaxi(self, apartmentName):
        for i in range(0, len(self.listOfApartments)):
            apartment = self.listOfApartments[i]
            if(apartment.getApartmentName() == apartmentName):
                self.listOfApartments[i].subtractClientsInTheBuilding()
                self.listOfApartments[i].setPutAClient(True)
          #      self.listOfApartments[i].clientGrabbedATaxi()
    
    #Return the list with all of the Apartments
    def getListOfApartments(self):
        return self.listOfApartments

    #Return the list with all of the Apartment Names
    def getListOfApartmentNames(self):
        return self.listOfApartmentNames

    #Return the list with all of the Apartment Names
    def getWorkplaceController(self):
        return self.workplaceController

    

###########################################################################################################
# WorkplaceController Class:
##########################################################################################################

class WorkplaceController:
    def __init__(self, listOfWorkplacesNames):
        self.listOfWorkplaces = []
        self.addWorkplace(listOfWorkplacesNames)

    #Create a workplace
    def addWorkplace(self,listOfWorkplacesNames):
        for i in range(0, len(listOfWorkplacesNames)):
            name = listOfWorkplacesNames[i]
            newWorkplace = Workplace(name)
            self.listOfWorkplaces.append(newWorkplace)

    #Add a client to workplace
    def addClientToWorkplace(self, workplaceName, client):
        for i in range(0, len(self.listOfWorkplaces)):
            workplace = self.listOfWorkplaces[i]
            if(workplace.getWorkplaceName() == workplaceName):
                self.listOfWorkplaces[i].addWorker(client)

    #This method check which workplace need to send clients to work([["A", True], ["B", True]]) (NombreEdificio, putAClient)
    def checkClientsToGoHome(self, time):
        listOfWorkplacesToGoHome = []
        for i in range(0, len(self.listOfWorkplaces)):
            workplace = self.listOfWorkplaces[i]
            if(workplace.checkClientsToGoHome(time) == True):
                listOfWorkplacesToGoHome.append([workplace.getWorkplaceName(), workplace.getPutAClient()])
                self.listOfWorkplaces[i].setPutAClient(False) #This value change after the taxi grabbed the client

        return listOfWorkplacesToGoHome

    #This method is called when a client grabbed a taxi, so there is less people in the apartment
    def clientGrabbedATaxi(self, workplaceName):
        for i in range(0, len(self.listOfWorkplaces)):
            workplace = self.listOfWorkplaces[i]
            if(workplace.getApartmentName() == apartmentName):
                self.listOfWorkplaces[i].setPutAClient(True)

    def getListOfWorkplaces(self):
        return self.listOfWorkplaces

    ###Get the list with all of the clients that need to go to work from an specific apartment##
    def getClientsToGoHome(self, workplaceName, time):
        for i in range(0, len(self.listOfWorkplaces)):
            workplace = self.listOfWorkplaces[i]
            if(workplace.getWorkplaceName() == workplaceName):
                return workplace.clientsThatNeedToGoHome(time)
