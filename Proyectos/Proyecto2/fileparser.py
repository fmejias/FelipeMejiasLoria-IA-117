class FileParser:
    def __init__(self):
        self.mapFile = "MapFiles/" + "mapa1.txt"
        self.maxNumberOfCharacters = self.getMaxNumberOfCharacters()
        self.intermediateFile = "MapFiles/mapParse.txt"
        self.newFile = "MapFiles/mapFinalParse.txt"
        self.city = []
        self.cityForTkinter = []
        self.clientsFile = "EspecificacionClientesApartamentos.txt"
        self.clientsForApartment = []

    def printMap(self):
        mapFile = open(self.mapFile,'r') 
        for line in mapFile:
            print(line, end='')
        print()
        mapFile.close()

    def getMaxNumberOfCharacters(self):
        charactersInEachLine = []
        mapFile = open(self.mapFile,'r') 
        for line in mapFile:
            charactersInEachLine.append(len(line.replace("\n","")))
        mapFile.close()
        return max(charactersInEachLine)

    def generateNewMap(self):
        newString = "*"
        newFile = open(self.intermediateFile,'w') 
        mapFile = open(self.mapFile,'r')
        for line in mapFile:
            if(len(line) < self.maxNumberOfCharacters):
                stringToAppend = newString * (self.maxNumberOfCharacters - len(line)+1)
                newMapString = line.replace("\n","") + stringToAppend + "\n"
                newFile.write(newMapString)
            else:
                newFile.write(line)
        newFile.close()
        mapFile.close()
        self.reviewNewMap()

    def reviewNewMap(self):
        newString = "*"
        newFile = open(self.intermediateFile,'r') 
        firstNewStringPosition = 0
        for line in newFile:
            firstNewStringPosition = line.find("*")
            break

        newFile.close()
        newFile = open(self.intermediateFile,'r') 
        finalMapFile = open(self.newFile,'w')

        for line in newFile:
            j = line[firstNewStringPosition:self.maxNumberOfCharacters].find("|")
            k = line[firstNewStringPosition:self.maxNumberOfCharacters].find("-")
            newLine = ""
            if((line[firstNewStringPosition-1] == "|" or
                line[firstNewStringPosition-1] == "-") and
               line[firstNewStringPosition] == " " and j!= -1):

                for i in range(firstNewStringPosition,firstNewStringPosition+j):
                    newLine = newLine + newString

                lineToAppend = line[0:firstNewStringPosition] + newLine
                lineToAppend = lineToAppend + line[firstNewStringPosition+j:self.maxNumberOfCharacters]                    
                self.city.append(list(lineToAppend))
                self.cityForTkinter.append(list(lineToAppend))
                newLine = line[0:firstNewStringPosition] + newLine
                newLine = newLine + line[firstNewStringPosition+j:self.maxNumberOfCharacters] + "\n"
                finalMapFile.write(newLine)

            elif((line[firstNewStringPosition-1] == "|" or
                  line[firstNewStringPosition-1] == "-") and
                 line[firstNewStringPosition] == " " and k!= -1):

                for x in range(firstNewStringPosition,firstNewStringPosition+k):
                    newLine = newLine + newString
                    
                lineToAppend = line[0:firstNewStringPosition] + newLine
                lineToAppend = lineToAppend + line[firstNewStringPosition+k:self.maxNumberOfCharacters] 
                self.city.append(list(lineToAppend))
                self.cityForTkinter.append(list(lineToAppend))
                newLine = line[0:firstNewStringPosition] + newLine
                newLine = newLine + line[firstNewStringPosition+k:self.maxNumberOfCharacters] + "\n"
                finalMapFile.write(newLine)
 
            else:
                newLine = line
                finalMapFile.write(newLine)
                lineToAppend = line.replace("\n","")
                self.city.append(list(lineToAppend))
                self.cityForTkinter.append(list(lineToAppend))

        newFile.close()
        finalMapFile.close()
                
    def printNewMap(self):
        newFile = open(self.newFile,'r') 
        for line in newFile:
            print(line, end='')
        newFile.close()

    def parseClients(self):
        clientsFile = open(self.clientsFile,'r') 
        for line in clientsFile:
            self.clientsForApartment.append(line.replace("\n","").split("=")) 
        clientsFile.close()
        return self.clientsForApartment

    def getCity(self):
        for i in range(0, len(self.city)):
            for j in range(0,len(self.city[0])):
                if( (i - 1 >= 0) and (i + 1 < len(self.city)) and
                    (j-1 >= 0) and (j+1 < len(self.city[0]))):                    
                    if((self.city[i-1][j] == "-") and
                       (self.city[i+1][j] == "-") and
                       (self.city[i][j-1] == "|") and
                       (self.city[i][j+1] == "|")):
                        self.cityForTkinter[i][j] = ["yes", self.city[i][j]]
                    elif((self.city[i-1][j] == "O") and
                         (self.city[i+1][j] == "O") and
                         (self.city[i][j-1] == "|") and
                         (self.city[i][j+1] == "|")):
                        self.cityForTkinter[i][j] = ["yes", self.city[i][j]]
                    elif((self.city[i-1][j] == "O") and
                         (self.city[i+1][j] == "-") and
                         (self.city[i][j-1] == "|") and
                         (self.city[i][j+1] == "|")):
                        self.cityForTkinter[i][j] = ["yes", self.city[i][j]]
                    elif((self.city[i-1][j] == "-") and
                         (self.city[i+1][j] == "O") and
                         (self.city[i][j-1] == "|") and
                         (self.city[i][j+1] == "|")):
                        self.cityForTkinter[i][j] = ["yes", self.city[i][j]]
                    else:
                        self.cityForTkinter[i][j] = ["no", self.city[i][j]]
                else:
                    self.cityForTkinter[i][j] = ["no", self.city[i][j]]
                    
        return self.cityForTkinter
        
def createMapParser():
    parser = FileParser() 
    parser.generateNewMap() 
    x = parser.getCity()
    return parser.getCity()

