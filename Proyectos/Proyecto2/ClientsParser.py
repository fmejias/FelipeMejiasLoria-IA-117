class ClientsParser:
    def __init__(self):
        self.clientsFile = "EspecificacionClientesApartamentos.txt"
        self.clientsForApartment = []

    def parseClients(self):
        clientsFile = open(self.clientsFile,'r') 
        for line in clientsFile:
            self.clientsForApartment.append(line.replace("\n","").split("=")) 
        clientsFile.close()
        return self.clientsForApartment
