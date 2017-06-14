class Client:
    def __init__(self):
        self.initialBlock = "" 
        self.destinationBlock = ""
        self.leaveSchedule = ""
        self.arriveSchedule = ""
        self.workplace = "" 
        self.apartment = "" 

    def setInitialBlock(self,initialBlock):
        self.initialBlock = initialBlock

    def getInitialBlock(self):
        return self.initialBlock

    def setDestinationBlock(self,destinationBlock):
        self.destinationBlock = destinationBlock

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
        return self.arriveSchedule

    def setApartment(self,apartment):
        self.apartment = apartment

    def getApartment(self):
        return self.apartment

    def goToWork(self):
        self.initialBlock = self.apartment
        self.destinationBlock = self.workplace

    def goHome(self):
        self.initialBlock = self.workplace
        self.destinationBlock = self.apartment
    
