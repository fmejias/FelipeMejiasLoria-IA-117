###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################



###########################################################################################################
# MapParser Class:
# Attributes:
# 1-) mapFile: Contains the name of the file with the map
# 2-) maxNumberOfCharacters: Contains the maximum number of characters in a line
# Methods:
# 1-) printMap: This method is in charge of print the Map for the Taxi Simulation
# 2-) getMaxNumberOfCharacters: This method is use to get the maximun number of characters in a line of the file
##########################################################################################################

class MapParser:
    def __init__(self, mapFile):
        self.mapFile = "MapFiles/" + mapFile
        self.maxNumberOfCharacters = self.getMaxNumberOfCharacters()
        self.intermediateFile = "MapFiles/mapParse.txt"
        self.newFile = "MapFiles/mapFinalParse.txt"
        self.city = []
        self.cityForTkinter = []


    #This method is in charge of print the Map for the Taxi Simulation
    def printMap(self):
        mapFile = open(self.mapFile,'r') #Open the file with the map specification in read mode
        #Print all the content of the file
        for line in mapFile:
            print(line, end='')

        print()
        
        #Close the map file
        mapFile.close()

    #This method is use to get the maximun number of characters in a line of the file
    def getMaxNumberOfCharacters(self):
        charactersInEachLine = []
        mapFile = open(self.mapFile,'r') #Open the file with the map specification in read mode

        #Get all the content of the file
        for line in mapFile:
            charactersInEachLine.append(len(line.replace("\n",""))) #Append the number of characters in each line, withput counting the \n

        #Close the map file
        mapFile.close()
        
        #Get the maximum number
        return max(charactersInEachLine)

    #This method is use to create a new file of maxNumberOfCharacters x maxNumberOfCharacters
    def generateNewMap(self):
        newString = "*"
        newFile = open(self.intermediateFile,'w') #This is going to be the new file
        mapFile = open(self.mapFile,'r') #Open the file with the map specification in read mode

        #Go over all the content of the file
        for line in mapFile:
            if(len(line) < self.maxNumberOfCharacters):
                stringToAppend = newString * (self.maxNumberOfCharacters - len(line)+1)
                newMapString = line.replace("\n","") + stringToAppend + "\n"
                newFile.write(newMapString)
            else:
                newFile.write(line)

        #Close all the files
        newFile.close()
        mapFile.close()

        #Call inmediatly the reviewNewMap
        self.reviewNewMap()

    #This method is use to review the new map, and put the * that are ausent.
    def reviewNewMap(self):
        newString = "*"
        newFile = open(self.intermediateFile,'r') #Open the new file
        firstNewStringPosition = 0

        #Go over the new file
        for line in newFile:
            firstNewStringPosition = line.find("*")
            break

        newFile.close()
        newFile = open(self.intermediateFile,'r') #Open the new file
        finalMapFile = open(self.newFile,'w') #This is the final map
        
        #Go over the new file
        for line in newFile:
            j = line[firstNewStringPosition:self.maxNumberOfCharacters].find("|")
            k = line[firstNewStringPosition:self.maxNumberOfCharacters].find("-")
            newLine = ""
            if((line[firstNewStringPosition-1] == "|" or line[firstNewStringPosition-1] == "-") and line[firstNewStringPosition] == " " and j!= -1):
                for i in range(firstNewStringPosition,firstNewStringPosition+j):
                    newLine = newLine + newString

                #Add the row to the city matrix
                lineToAppend = line[0:firstNewStringPosition] + newLine + line[firstNewStringPosition+j:self.maxNumberOfCharacters]                    
                self.city.append(list(lineToAppend))
                self.cityForTkinter.append(list(lineToAppend))
                newLine = line[0:firstNewStringPosition] + newLine + line[firstNewStringPosition+j:self.maxNumberOfCharacters] + "\n"
                finalMapFile.write(newLine)

            elif((line[firstNewStringPosition-1] == "|" or line[firstNewStringPosition-1] == "-") and line[firstNewStringPosition] == " " and k!= -1):
                for x in range(firstNewStringPosition,firstNewStringPosition+k):
                    newLine = newLine + newString

                #Add the row to the city matrix
                lineToAppend = line[0:firstNewStringPosition] + newLine + line[firstNewStringPosition+k:self.maxNumberOfCharacters] 
                self.city.append(list(lineToAppend))
                self.cityForTkinter.append(list(lineToAppend))
                newLine = line[0:firstNewStringPosition] + newLine + line[firstNewStringPosition+k:self.maxNumberOfCharacters] + "\n"
                finalMapFile.write(newLine)
 
            else:
                newLine = line
                finalMapFile.write(newLine)

                #Add the row to the city matrix
                lineToAppend = line.replace("\n","")
                self.city.append(list(lineToAppend))
                self.cityForTkinter.append(list(lineToAppend))

        #Close all of the files
        newFile.close()
        finalMapFile.close()
                
    #This method is in charge of print the new map, after parse it.
    def printNewMap(self):
        newFile = open(self.newFile,'r') #Open the file with the map specification in read mode

        #Print all the content of the file
        for line in newFile:
            print(line, end='')

        #Close the map file
        newFile.close()

    #This method is use to get the matrix of the city
    def getCity(self):
        for i in range(0, len(self.city)):
            for j in range(0,len(self.city[0])):
                if( (i - 1 >= 0) and (i + 1 < len(self.city)) and (j-1 >= 0) and (j+1 < len(self.city[0]))):                    
                    if((self.city[i-1][j] == "-") and (self.city[i+1][j] == "-") and (self.city[i][j-1] == "|") and (self.city[i][j+1] == "|")):
                        self.cityForTkinter[i][j] = ("yes", self.city[i][j])
                    else:
                        self.cityForTkinter[i][j] = ("no", self.city[i][j])
                else:
                    self.cityForTkinter[i][j] = ("no", self.city[i][j])
                    
        return self.cityForTkinter
        

#This method creates an instance of the class MapParser
def createMapParser():
    parser = MapParser("mapa1.txt") #Creates the MapParser Object
    parser.generateNewMap() #This instruction call the method of the MapParser Object that generates the new map
    x = parser.getCity()
    return parser.getCity() #Returns the city matrix
