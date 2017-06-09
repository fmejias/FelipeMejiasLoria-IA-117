###########################################################################################################
# Client Class:
##########################################################################################################

class Client:
    def __init__(self):
        self.initialBlock = "" 
        self.destinationBlock = ""
        self.leaveSchedule = ""
        self.arriveSchedule = ""
        self.workplace = "" #Name of the workplace of the client
        self.apartment = "" #Name of the apartment of the client

    #This method set the initialBlock of the Client
    def setInitialBlock(self,initialBlock):
        self.initialBlock = initialBlock

    #This method get the initial block of the client
    def getInitialBlock(self):
        return self.initialBlock

    #This method set the destination block of the Client
    def setDestinationBlock(self,destinationBlock):
        self.destinationBlock = destinationBlock

    #This method get the destination block of the client
    def getDestinationBlock(self):
        return self.destinationBlock

    def setWorkplace(self,workplace):
        self.workplace = workplace

    def getWorkplace(self):
        return self.workplace
    
    def setLeaveSchedule(self,schedule):
        self.leaveSchedule = schedule

    def getLeaveSchedule(self):
        return self.leaveSchedule

    def setArriveSchedule(self,schedule):
        self.arriveSchedule = schedule

    def getArriveSchedule(self):
        return self.leaveSchedule

    def setApartment(self,apartment):
        self.apartment = apartment

    def getApartment(self):
        return self.apartment

    #This method set the client with the destination to go to work
    def goToWork(self):
        self.initialBlock = apartment
        self.destinationBlock = workplace

    #This method set the client with the destination to go to home
    def goHome(self):
        self.initialBlock = workplace
        self.destinationBlock = apartment
    
