import random
import client

class Apartment:
    def __init__(self, name, numberOfClients, leaveSchedule, arriveSchedule):
        self.apartmentName = name
        self.numberOfClients = numberOfClients
        self.leaveSchedule = leaveSchedule
        self.arriveSchedule = arriveSchedule
        self.listOfClients = []
        self.actualNumberOfClientsInTheBuilding = int(numberOfClients)
        self.putAClient = True
        self.listOfClientsWaitingATaxi = [] 
        self.clientsAlreadyWaitingForATaxi = False

    def setPutAClient(self,value):
        self.putAClient = value

    def areClientsWaitingForTaxi(self):
        if(len(self.listOfClientsWaitingATaxi) >= 1):
            return True
        else:
            return False

    def getPutAClient(self):
        return self.putAClient
    
    def setApartmentName(self,name):
        self.apartmentName = name

    def getApartmentName(self):
        return self.apartmentName

    def setNumberOfClients(self,numberOfClients):
        self.numberOfClients = numberOfClients

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

    def clientsThatNeedToGoWork(self, time):
        if(self.leaveSchedule == time and self.clientsAlreadyWaitingForATaxi == False):
            numberOfClients = self.numberOfClients
            
            for j in range(0,int(numberOfClients)):
                self.listOfClientsWaitingATaxi.insert(0, self.listOfClients[j])
                
            self.clientsAlreadyWaitingForATaxi = True
            
        return self.listOfClientsWaitingATaxi

    def getClientWaitingForATaxi(self):
        return self.listOfClientsWaitingATaxi[len(self.listOfClientsWaitingATaxi)-1]

    def getNumberOfClientsWaitingForATaxi(self):
        return len(self.listOfClientsWaitingATaxi)

    def clientGrabbedATaxi(self):
        if(len(self.listOfClientsWaitingATaxi) >= 1):
            self.listOfClientsWaitingATaxi.pop()

class Workplace:
    def __init__(self, name):
        self.workplaceName = name 
        self.listOfWorkers = []
        self.numberOfWorkers = 0
        self.actualNumberOfClientsInTheWorkplace = 0
        self.listOfClientsWaitingATaxi = [] 
        self.listOfClientsApartmentWaitingATaxi = [] 
        self.clientsAlreadyWaitingForATaxi = False
        self.timeToLeave = "12:00"
        self.putAClient = True

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

    def addWorker(self, worker):
        self.numberOfWorkers = self.numberOfWorkers + 1
        self.listOfWorkers.append(worker)

    def getWorkplaceWorkers(self):
        return self.listOfWorkers

    def incrementNumberOfClientsInTheWorkplace(self):
        self.actualNumberOfClientsInTheWorkplace = self.actualNumberOfClientsInTheWorkplace + 1

    def decrementNumberOfClientsInTheWorkplace(self):
        self.actualNumberOfClientsInTheWorkplace = self.actualNumberOfClientsInTheWorkplace - 1

    def numberOfClientsForEachApartment(self, apartmentName):
        numberOfClients = 0
        for i in range(0, len(self.listOfWorkers)):
            clientInApartment = self.listOfWorkers[i]
            clientInApartment = clientInApartment.getApartment()
            if(clientInApartment == apartmentName):
                numberOfClients = numberOfClients + 1

        return numberOfClients
    
    def clientsThatNeedToGoHome(self, time):
        if(self.timeToLeave == time and
           self.clientsAlreadyWaitingForATaxi == False):
            numberOfWorkers = self.numberOfWorkers

            for j in range(0,numberOfWorkers):
                self.listOfClientsWaitingATaxi.insert(0, self.listOfWorkers[j])

            self.clientsAlreadyWaitingForATaxi = True

        return self.listOfClientsWaitingATaxi

    def getClientWaitingForATaxi(self):
        length = len(self.listOfClientsWaitingATaxi)
        return self.listOfClientsWaitingATaxi[length-1]

    def getNumberOfClientsWaitingForATaxi(self):
        return len(self.listOfClientsWaitingATaxi)

    def clientGrabbedATaxi(self):
        if(len(self.listOfClientsWaitingATaxi) >= 1):
            self.listOfClientsWaitingATaxi.pop()

    def checkClientsToGoHome(self, time):
        clientsWaiting = False
        self.clientsThatNeedToGoHome(time)
        if(len(self.listOfClientsWaitingATaxi) >= 1):
            clientsWaiting = True
        else:
            clientsWaiting = False

        return clientsWaiting
        

class ApartmentController:
    def __init__(self, listOfWorkplaces):
        self.listOfApartments = []
        self.listOfApartmentNames = []
        self.leaveApartmentHours = ["07:00", "08:00"]
        self.arriveApartmentHours = ["12:00"]
        self.workplaceController = WorkplaceController(listOfWorkplaces)

    def addApartment(self,name, numberOfClients, workplace):
        leaveSchedule = random.choice(self.leaveApartmentHours)
        arriveSchedule = random.choice(self.arriveApartmentHours)
        newApartment = Apartment(name, numberOfClients, leaveSchedule,
                                 arriveSchedule)
        self.listOfApartments.append(newApartment)
        self.listOfApartmentNames.append(name)
        self.addClientsToApartment(name, workplace, leaveSchedule,
                                   arriveSchedule, numberOfClients)

    def addClientsToApartment(self, apartment, workplace, leaveSchedule,
                              arriveSchedule, numberOfClients):
        for i in range(0, int(numberOfClients)):
            clientToApartment = client.Client()
            clientToApartment.setApartment(apartment)
            clientToApartment.setWorkplace(workplace)
            clientToApartment.setLeaveSchedule(leaveSchedule)
            clientToApartment.setArriveSchedule(arriveSchedule)
            self.workplaceController.addClientToWorkplace(workplace, clientToApartment)
            length = len(self.listOfApartments)
            self.listOfApartments[length-1].addClientToApartment(clientToApartment)

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

    def checkClientsToGoToWork(self, time):
        listOfApartmentsToGoToWork = []
        for i in range(0, len(self.listOfApartments)):
            apartment = self.listOfApartments[i]
            if(apartment.getLeaveSchedule() == time and
               apartment.actualNumberOfClientsInTheBuilding > 0):
                listOfApartmentsToGoToWork.append([apartment.getApartmentName(),
                                                   apartment.getPutAClient()])
                self.listOfApartments[i].setPutAClient(False) 
        return listOfApartmentsToGoToWork

    def checkClientsToEraseFromApartment(self):
        listOfApartmentsToGoToWork = []
        for i in range(0, len(self.listOfApartments)):
            apartment = self.listOfApartments[i]
            if(apartment.getNumberOfClientsWaitingForATaxi() == 0):
                listOfApartmentsToGoToWork.append([apartment.getApartmentName(),
                                                   apartment.getPutAClient()])
        return listOfApartmentsToGoToWork

    def getClientsToGoToWork(self, apartmentName, time):
        for i in range(0, len(self.listOfApartments)):
            apartment = self.listOfApartments[i]
            if(apartment.getApartmentName() == apartmentName):
                return apartment.clientsThatNeedToGoWork(time)
                
    def clientGrabbedATaxi(self, apartmentName):
        for i in range(0, len(self.listOfApartments)):
            apartment = self.listOfApartments[i]
            if(apartment.getApartmentName() == apartmentName):
                self.listOfApartments[i].subtractClientsInTheBuilding()
                self.listOfApartments[i].setPutAClient(True)
    
    def getListOfApartments(self):
        return self.listOfApartments

    def getListOfApartmentNames(self):
        return self.listOfApartmentNames

    def getWorkplaceController(self):
        return self.workplaceController

    
class WorkplaceController:
    def __init__(self, listOfWorkplacesNames):
        self.listOfWorkplaces = []
        self.addWorkplace(listOfWorkplacesNames)

    def addWorkplace(self,listOfWorkplacesNames):
        for i in range(0, len(listOfWorkplacesNames)):
            name = listOfWorkplacesNames[i]
            newWorkplace = Workplace(name)
            self.listOfWorkplaces.append(newWorkplace)

    def addClientToWorkplace(self, workplaceName, client):
        for i in range(0, len(self.listOfWorkplaces)):
            workplace = self.listOfWorkplaces[i]
            if(workplace.getWorkplaceName() == workplaceName):
                self.listOfWorkplaces[i].addWorker(client)

    def checkClientsToGoHome(self, time):
        listOfWorkplacesToGoHome = []
        for i in range(0, len(self.listOfWorkplaces)):
            workplace = self.listOfWorkplaces[i]
            if(workplace.checkClientsToGoHome(time) == True):
                listOfWorkplacesToGoHome.append([workplace.getWorkplaceName(),
                                                 workplace.getPutAClient()])
                self.listOfWorkplaces[i].setPutAClient(False) 

        return listOfWorkplacesToGoHome

    def clientGrabbedATaxi(self, workplaceName):
        for i in range(0, len(self.listOfWorkplaces)):
            workplace = self.listOfWorkplaces[i]
            if(workplace.getWorkplaceName() == workplaceName):
                self.listOfWorkplaces[i].setPutAClient(True)

    def getListOfWorkplaces(self):
        return self.listOfWorkplaces

    def getClientsToGoHome(self, workplaceName, time):
        for i in range(0, len(self.listOfWorkplaces)):
            workplace = self.listOfWorkplaces[i]
            if(workplace.getWorkplaceName() == workplaceName):
                return workplace.clientsThatNeedToGoHome(time)
