###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################



###########################################################################################################
# ClientsParser Class:
# Attributes:
##########################################################################################################

class ClientsParser:
    def __init__(self):
        self.clientsFile = "EspecificacionClientesApartamentos.txt"
        self.clientsForApartment = []

    #This method is in charge of get the number of clients for apartment
    def parseClients(self):
        clientsFile = open(self.clientsFile,'r') #Open the file with the clients specification in read mode

        #Get all the content of the file
        for line in clientsFile:
            self.clientsForApartment.append(line.replace("\n","").split("=")) #Append the number of characters in each line, withput counting the \n
            
        #Close the clients file
        clientsFile.close()

        return self.clientsForApartment
