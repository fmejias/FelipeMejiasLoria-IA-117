###########################################################################################################
# Apartment Class:
##########################################################################################################

class Apartment:
    def __init__(self):
        self.initialBlock = "" 
        self.destinationBlock = ""

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
