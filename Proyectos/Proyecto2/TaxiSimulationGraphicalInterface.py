###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################

#Import of the standard Python interface to the Tk GUI toolkit
from tkinter import*

#Import of the Image module
from PIL import ImageTk, Image

#Import from the MapParser module the city matrix
import MapParser

#Import of the module TimerGraphicalInterface to get the actual instruction
import TimerGraphicalInterface

#Import of the module StateMachine to check all of the possible movements of the taxis
import StateMachine

#Import of the module CityObjects to create the City Graph
import CityObjects

#Import the module to copy list
import copy

#Import of the module to play a sound
import winsound

#Import of the module to implement a delay for the timer
import time

#Import of the module in charge of parse the clients file
import ClientsParser

#Import of the classes Apartment Controller and Workplace Controller
import Buildings

#Import of the Taxi Controller class
import Taxi

import random

##Declaration of some global variables to comunicate with the Threads
taxiSimulationWindow = None
cityGraph = ""

###########################################################################################################
# TaxiSimulationWindow Class:
# Attributes: masterWindow, frameWindow, instruction. 
# Methods:
# .
##########################################################################################################
class TaxiSimulationWindow:
    def __init__(self, master): 
        
        #Establish the width and height of the First Window
        self.width = 1100
        self.height = 600
        
        #Initialize the city matrix, get the number of rows of the city and the number of columns of the city
        self.city = MapParser.createMapParser()
        self.rows = len(self.city)
        self.columns = len(self.city[0])

        #This is an instance of the ClientsParser
        self.clientsParser = ClientsParser.ClientsParser()

        #Create the instance of the state machine
        self.stateMachine = StateMachine.StateMachine()

        #This variable is going to contain the actual time
        self.actualTime = "0:00"

        #This is used to save the old coordinates of the taxi
        self.oldCoordinates = []
        self.taxiNode = 0

        #This indicates to do the animation
        self.doAnimation = False
        self.updateTime = 50
        self.sameInstruction = False

        #List with the travel of the taxi
        self.travelList = []

        #This indicates if there is an instruction executing at the time
        self.executingInstruction = False

        #This indicates not to perform again the search algorithm
        self.routeAlreadyExecute = False
        
        #Create a City Graph Object
        self.cityGraph = CityObjects.createCityGraph(self.city)

        #Apartment controller, workplace controller and taxi controller
        self.apartmentController = Buildings.ApartmentController(self.cityGraph.searchAllWorkplaces())
        self.workplaceController = Buildings.WorkplaceController(self.cityGraph.searchAllWorkplaces())
        self.taxiController = Taxi.TaxiController(self.cityGraph.searchAllTaxisId())

        #This lists are use to paint the clients in the workplaces and apartments
        self.listOfApartmentPositions = self.cityGraph.searchAllApartmentsPosition()
        self.listOfWorkplacesPositions = self.cityGraph.searchAllWorkplacesPosition()
        self.listOfApartmentsThatNeedToWork = []
        self.listOfWorkplacesThatNeedToGoHome = []



        #Initialize the matrix of Labels that are going to compose the Window
        self.matrixOfLabels = self.city

        #Set all of the images
        self.taxiRightImage = Image.open("ProjectImages/taxiDerecha.png")
        self.wallHorizontalImage = Image.open("ProjectImages/barreraHorizontal2.png")
        self.wallVerticalImage = Image.open("ProjectImages/barreraVertical2.png")
        self.streetImage = Image.open("ProjectImages/calle.png")
        self.waterImage = Image.open("ProjectImages/rio.png")
        self.clientImage = Image.open("ProjectImages/cliente1.jpg")
        self.routeImage = Image.open("ProjectImages/ruta1.png")
        self.cuadraSinIdentificacionImage = Image.open("ProjectImages/cuadraSinIdentificacion.png")
        self.buildingImage = ""
        self.cuadraIdentificada = ""
        self.taxi = ""
        self.clientsNumber = ""
        
        #Set the master as the root
        self.master = master
        self.widthOfEachFrame = 0
        self.heightOfEachFrame = 0

        #Here, we call the function in charge of build the city
        self.buildCity()

        #Buildings information frame
        self.buildingsInformationFrame = Frame(self.master, width=260, height=600, background="peru")
        self.buildingsInformationFrame.place(x=1085, y = 0)

        self.buttonBuildingInformation = Button(self.buildingsInformationFrame, text="Horarios en los edificios", width= 25,
                                                height = 1, bg= "#A6420B",fg='white',font = ('Kalinga','12'))

        self.buttonBuildingInformation.place(x=10,y=5)

        #######Initial methods to call#######

        #Create all of the apartments and clients objects
        self.createApartmentsAndClients()

        #Create the panel with the building information
        self.createBuildingsInformation()

        #Paint the number of clients
        self.paintNumberOfClients()

        #This instruction is in charge of beginning the simulation
        self.startWorking()


    #This method is in charge of create all of the objects Apartments and Clients
    def createApartmentsAndClients(self):
        listOfNumberOfClientsAndApartmentNames = self.clientsParser.parseClients()
        listOfAllWorkplaces = self.cityGraph.searchAllWorkplaces()

        ##Iterate for all of the apartments on the map
        for i in range(0, len(listOfNumberOfClientsAndApartmentNames)):

            #Get the name and the number of clients
            apartmentName = listOfNumberOfClientsAndApartmentNames[i][0]
            apartmentClients = listOfNumberOfClientsAndApartmentNames[i][1]

            #Add random workplace to all of the clients of that apartment
            workplace = random.choice(listOfAllWorkplaces)

            #Create the apartment and all the clients of the apartment
            self.apartmentController.addApartment(apartmentName, apartmentClients, workplace)

        #Assign the new workplace controller
        self.workplaceController = self.apartmentController.getWorkplaceController()


    #This method is in charge of adding the buildings information(Search for all of the buildings and append a new frame to that board)
    def createBuildingsInformation(self):

        #Get the list of buildings
        buildingsList = self.cityGraph.searchAllBuildings()

        #Initial coordinates for the frames
        frameX = 5
        frameY = 60

        #Iterate about all of the frames
        for i in range(0,len(buildingsList)):
            
            #Create the new building frame
            buildingInformation1 = Frame(self.buildingsInformationFrame, width=250, height=150, background="moccasin")
            buildingInformation1.place(x=frameX, y = frameY)

            #Image information
            buildingImage = Image.open("ProjectImages/" + "apartamento" + buildingsList[i] + ".png")
            buildingImage = buildingImage.resize((80, 71), Image.ANTIALIAS)
            buildingImage = ImageTk.PhotoImage(buildingImage)

            #Get leave and arrive schedule
            leaveArriveSchedule = self.apartmentController.getLeaveArriveSchedule(buildingsList[i])
            
            #Label for the frame
            buildingName = "Edificio " + buildingsList[i]
            labelTitle = Label(buildingInformation1, text=buildingName, width= 10,height = 2, bg= "moccasin",fg='black',font = ('Kalinga','12'))
            labelTitle.grid(row=0, column = 0)

            labelOut = Label(buildingInformation1, text="Salida: " + leaveArriveSchedule[0] + " am", width= 15,height = 2, bg= "moccasin",
                             fg='black',font = ('Kalinga','12'))
            labelOut.grid(row=0,column=1)

            labelImage = Label(buildingInformation1, image=buildingImage, bg= "moccasin",fg='black',font = ('Kalinga','12'))
            labelImage.image = buildingImage
            labelImage.grid(row=1, column = 0)

            labelIn = Label(buildingInformation1, text="Entrada: " + leaveArriveSchedule[1] + " pm", width= 15,height = 4, bg= "moccasin",fg='black',font = ('Kalinga','12'))
            labelIn.grid(row=1,column=1)

            #Update the coordinates of x and y of the new frame
            frameY = frameY + 140

    #This method is in charge of paint the number of clients in the building
    def paintNumberOfClients(self):
        listOfCoordinatesOfApartments = self.cityGraph.searchAllApartmentsPosition()
        listOfNumberOfClients = self.clientsParser.parseClients()

        #Iterate for all the apartments
        for i in range(0, len(listOfCoordinatesOfApartments)):
            apartment = listOfCoordinatesOfApartments[i][0] #Name of the apartment
            x = listOfCoordinatesOfApartments[i][1][0]
            y = listOfCoordinatesOfApartments[i][1][1]
            numberOfClients = 0

            #Search the number of clients of the apartment
            for j in range(0, len(listOfNumberOfClients)):
                if(listOfNumberOfClients[j][0] == apartment):
                    numberOfClients = listOfNumberOfClients[j][1]
                    break

            #Paint the number of clients
                    
            #Resize the image with the size of the square
            imagePath = "ProjectImages/" + numberOfClients + ".png"
            self.clientsNumber = Image.open(imagePath)

            #Resize the image with the size of the square
            displayImage = self.clientsNumber.resize((self.widthOfEachFrame, self.heightOfEachFrame), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)

            frame=Frame(self.master, width=self.widthOfEachFrame, height=self.heightOfEachFrame, background="White")
            frame.grid(row=x, column=y+1)
            
            #Create the Label and add it to the List of Labels
            label = Label(frame, image = displayImage)
            label.image = displayImage
            label.place(x=0,y=0)
            
            #Add the Label to the matrix
            self.matrixOfLabels[x][y+1] = label
        

    #This method is in charge of build the city
    def buildCity(self):
        self.widthOfEachFrame = self.width // self.columns
        self.heightOfEachFrame = self.height // self.rows

        #Go over all the city matrix
        for i in range (0, self.rows):
            for j in range (0,self.columns):
                frame=Frame(self.master, width=self.widthOfEachFrame, height=self.heightOfEachFrame, background="White")
                frame.grid(row=i, column=j)

                #Resize the image with the size of the square
                displayImage = self.resizeImage(self.city[i][j][0], self.city[i][j][1], self.widthOfEachFrame, self.heightOfEachFrame)

                #Create the Label and add it to the List of Labels
                label = Label(frame, image = displayImage)
                label.image = displayImage
                label.place(x=0,y=0)

                #Add the Label to the matrix
                self.matrixOfLabels[i][j] = label
        
    #This method return the image resize
    def resizeImage(self,esCuadra,imageValue,width,height):
        displayImage = 0
        if(imageValue == "-"):
            #Resize the image with the size of the square
            displayImage = self.wallHorizontalImage.resize((width, height), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)
        elif(imageValue == "|"):
            #Resize the image with the size of the square
            displayImage = self.wallVerticalImage.resize((width, height), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)
        elif(imageValue == "*"):
            #Resize the image with the size of the square
            displayImage = self.waterImage.resize((width, height), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)
        elif(imageValue == "V"):
            #Resize the image with the size of the square
            displayImage = self.routeImage.resize((width, height), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)        
        elif(imageValue == "O"):
            #Resize the image with the size of the square
            displayImage = self.clientImage.resize((width, height), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)
        elif(esCuadra == "no" and imageValue == " "):
            #Resize the image with the size of the square
            displayImage = self.streetImage.resize((width, height), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)
        elif(imageValue.isdigit() == True):
            #Resize the image with the size of the square
            imagePath = "ProjectImages/" + "taxi" + imageValue + ".png"
            self.taxi = Image.open(imagePath)
            #Resize the image with the size of the square
            displayImage = self.taxi.resize((width, height), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)
        elif(esCuadra == "yes"):
            if(imageValue == " "):
                #Resize the image with the size of the square
                displayImage = self.cuadraSinIdentificacionImage.resize((width, height), Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
            elif(imageValue.isupper() == True): #Is a letter => Building
                imagePath = "ProjectImages/" + "apartamento" + imageValue + ".png"
                self.cuadraIdentificada = Image.open(imagePath)
                #Resize the image with the size of the square
                displayImage = self.cuadraIdentificada.resize((width, height), Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
            else:
                imagePath = "ProjectImages/" + "trabajo" + imageValue + ".png"
                self.cuadraIdentificada = Image.open(imagePath)
                #Resize the image with the size of the square
                displayImage = self.cuadraIdentificada.resize((width, height), Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
        else:
            #Resize the image with the size of the square
            displayImage = self.streetImage.resize((width, height), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)
            
        return displayImage


    #This function is in charge of start the application
    def startWorking(self):

        #Aqui va el codigo para estar revisando la hora
        self.actualTime = TimerGraphicalInterface.returnTime()

        #Check if a client has to go to work or has to go home
        self.checkClientsToGoToWorkToGoHome(self.actualTime)

        #Por mientras, que solo llame a la funcion que mueve los carros de forma autonoma
        self.master.after(self.updateTime, self.enableTaxisServices)

    #This method is in charge of check if a client is in front of the taxi
    def searchClients(self):
        apartmentsWithClientsOutside = self.listOfApartmentsThatNeedToWork

        #Iterate for all of the apartments
        for i in range(0, len(apartmentsWithClientsOutside)):
            apartmentName = apartmentsWithClientsOutside[i][0]
            taxiNearClient = self.cityGraph.pickAClient(apartmentName) #Get the taxi in front of the client

            if(taxiNearClient != ""):

                #Check if the taxi has already a client
                taxiHaveClient = self.taxiController.getTaxiWithClient(taxiNearClient)

                if(taxiHaveClient == False):
                    
                    #Get the list of clients waiting a taxi and extract a client
                    listOfClients = self.apartmentController.getClientsToGoToWork(apartmentName, self.actualTime)
                    client = listOfClients[0]
                    client.goToWork()
                    destinationOfClient = client.getDestinationBlock()

                    #Calculate the road for the taxi
                    taxiRoad = self.cityGraph.travelWithClientRoad(destinationOfClient, taxiNearClient)

                    #Decrement the actual number of clients in the building
                    self.apartmentController.clientGrabbedATaxi(apartmentName)

                    #Update the taxi controller
                    self.taxiController.setTaxiRoad(taxiRoad, taxiNearClient)
                    self.taxiController.setTaxiWithClient(taxiNearClient)

                    #Erase client
                    for j in range(0, len(self.listOfApartmentPositions)):
                        apartment = self.listOfApartmentPositions[j][0] #Name of the apartment
                        x = self.listOfApartmentPositions[j][1][0]
                        y = self.listOfApartmentPositions[j][1][1]

                        #Paint the client on the map
                        if(apartment == apartmentName):
                            self.paintWall(x-1,y)
                            break
                    
                    #Delete a client from the list
                    del listOfClients[0]
                
        

    #This function is in charge of enable the movement of the autonoumous taxis
    def enableTaxisServices(self):

        #Get the actual positions of the taxis
        actualPositions = self.cityGraph.searchAllTaxisPosition()

        #Aqui tengo que revisar si un taxi esta a la par de un cliente
        self.searchClients()

        #Get the new positions of the taxis
        newPositions = self.stateMachine.generateMovements(actualPositions, self.cityGraph.returnCityGraph(), self.taxiController)

        #Check if the taxi with the client gets to its destiny
        self.taxiController.checkAlreadyInDestination()

        #Update the new positions of the taxis in the object self.cityGraph
        self.cityGraph.updateTaxisPosition(newPositions)

        #Update the GUI - First refresh the old positions
        for i in range(0, len(actualPositions)):
            taxiX = actualPositions[i][1][0]
            taxiY= actualPositions[i][1][1]

            #Resize the image with the size of the square
            displayImage = self.resizeImage("no", " ", self.widthOfEachFrame, self.heightOfEachFrame)
            frame=Frame(self.master, width=self.widthOfEachFrame, height=self.heightOfEachFrame, background="White")
            frame.grid(row=taxiX, column=taxiY)
            
            #Create the Label and add it to the List of Labels
            label = Label(frame, image = displayImage)
            label.image = displayImage
            label.place(x=0,y=0)
            
            #Add the Label to the matrix
            self.matrixOfLabels[taxiX][taxiY] = label

        #Update the GUI - Draw the taxis in the new positions
        for j in range(0, len(newPositions)):
            taxiX = newPositions[j][1][0]
            taxiY= newPositions[j][1][1]
            taxiName = newPositions[j][0]

            #Resize the image with the size of the square
            displayImage = self.resizeImage("no", taxiName, self.widthOfEachFrame, self.heightOfEachFrame)
            frame=Frame(self.master, width=self.widthOfEachFrame, height=self.heightOfEachFrame, background="White")
            frame.grid(row=taxiX, column=taxiY)
            
            #Create the Label and add it to the List of Labels
            label = Label(frame, image = displayImage)
            label.image = displayImage
            label.place(x=0,y=0)
            
            #Add the Label to the matrix
            self.matrixOfLabels[taxiX][taxiY] = label

        #Refresh the screen again
        self.master.after(self.updateTime, self.startWorking)

    
    ##This method paint the taxi again
    def paintTaxi(self):
        x = self.cityGraph.searchTaxiNode().getX()
        y = self.cityGraph.searchTaxiNode().getY()
        
        #Resize the image with the size of the square
        displayImage = self.resizeImage("no", "D", self.widthOfEachFrame, self.heightOfEachFrame)
        frame=Frame(self.master, width=self.widthOfEachFrame, height=self.heightOfEachFrame, background="White")
        frame.grid(row=x, column=y)
        
        #Create the Label and add it to the List of Labels
        label = Label(frame, image = displayImage)
        label.image = displayImage
        label.place(x=0,y=0)

        #Add the Label to the matrix
        self.matrixOfLabels[x][y] = label

    ##This method paint a client on the map
    def paintClient(self,x,y):
        
        #Resize the image with the size of the square
        displayImage = self.resizeImage("no", "O", self.widthOfEachFrame, self.heightOfEachFrame)
        frame=Frame(self.master, width=self.widthOfEachFrame, height=self.heightOfEachFrame, background="White")
        frame.grid(row=x, column=y)
        
        #Create the Label and add it to the List of Labels
        label = Label(frame, image = displayImage)
        label.image = displayImage
        label.place(x=0,y=0)

        #Add the Label to the matrix
        self.matrixOfLabels[x][y] = label

    ##This method paint a horizontal wall on the map
    def paintWall(self,x,y):
        
        #Resize the image with the size of the square
        displayImage = self.resizeImage("no", "-", self.widthOfEachFrame, self.heightOfEachFrame)
        frame=Frame(self.master, width=self.widthOfEachFrame, height=self.heightOfEachFrame, background="White")
        frame.grid(row=x, column=y)
        
        #Create the Label and add it to the List of Labels
        label = Label(frame, image = displayImage)
        label.image = displayImage
        label.place(x=0,y=0)

        #Add the Label to the matrix
        self.matrixOfLabels[x][y] = label

    #This method checks if if hast to put a client to go to work
    def checkClientsToGoToWorkToGoHome(self, time):
        self.listOfApartmentsThatNeedToWork = self.apartmentController.checkClientsToGoToWork(time)
        self.listOfWorkplacesThatNeedToGoHome = self.workplaceController.checkClientsToGoHome(time)
        listOfClientsToErase = self.apartmentController.checkClientsToEraseFromApartment()

        #This part paint clients on the apartments
        for i in range(0, len(self.listOfApartmentsThatNeedToWork)):
            putAClient = self.listOfApartmentsThatNeedToWork[i][1]
            apartmentName = self.listOfApartmentsThatNeedToWork[i][0]
            if(putAClient == True):
                #Iterate for all the apartments
                for j in range(0, len(self.listOfApartmentPositions)):
                    apartment = self.listOfApartmentPositions[j][0] #Name of the apartment
                    x = self.listOfApartmentPositions[j][1][0]
                    y = self.listOfApartmentPositions[j][1][1]

                    #Paint the client on the map
                    if(apartment == apartmentName):
                        self.paintClient(x-1,y)
                        break

        #This part paint clients on the workplaces
        for i in range(0, len(self.listOfWorkplacesThatNeedToGoHome)):
            putAClient = self.listOfWorkplacesThatNeedToGoHome[i][1]
            workplaceName = self.listOfWorkplacesThatNeedToGoHome[i][0]
            if(putAClient == True):
                #Iterate for all the apartments
                for j in range(0, len(self.listOfWorkplacesPositions)):
                    workplace = self.listOfWorkplacesPositions[j][0] #Name of the apartment
                    x = self.listOfWorkplacesPositions[j][1][0]
                    y = self.listOfWorkplacesPositions[j][1][1]

                    #Paint the client on the map
                    if(workplace == workplaceName):
                        self.paintClient(x-1,y)
                        break

    #This method return the city graph
    def getCityGraph(self):
        return self.cityGraph.returnCityGraph()
        

#This function display the taxi simulation
def displayTaxiSimulation():
    global taxiSimulationWindow
    global cityGraph
    master = Tk()#Create the principle window
    master.wm_title("Taxi Simulation") #Add a title to the window
    taxiSimulationWindow = TaxiSimulationWindow(master) #Add the taxi simulation frame to the principle window
    master.geometry("1350x600") #Set the size of the root
    master.geometry("+0+10") #Set the position of the root on the screen
    master.resizable(width=NO,height=NO) #Set the window as no resizable
    master.mainloop() #Starts the mainloop of the console window

#This function returns the city graph
def returnCityGraph():
    global taxiSimulationWindow
    global cityGraph
    if(taxiSimulationWindow is not None):
        cityGraph = taxiSimulationWindow.getCityGraph()
    else:
        cityGraph = []
    return cityGraph
