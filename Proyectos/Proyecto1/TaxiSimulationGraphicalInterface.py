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

#Import of the module ConsoleGraphicalInterface to get the actual instruction
import ConsoleGraphicalInterface

#Import of the module CityObjects to create the City Graph
import CityObjects

#Import the module to copy list
import copy

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

        #This contains the actual instruction
        self.actualInstruction = ""

        #This is used to save the old coordinates of the taxi
        self.oldCoordinates = []
        self.taxiNode = 0

        #This indicates to do the animation
        self.doAnimation = False
        self.updateTime = 1000

        #List with the travel of the taxi
        self.travelList = []

        #This indicates if there is an instruction executing at the time
        self.executingInstruction = False

        #Establish all the possible instructions
        self.travelInstruction = "pasear"
        self.searchInstruction = "buscar"
        self.showInstruction = "mostrar"
        self.animateInstruction = "animar"
        self.routeInstruction = "ruta"
        self.randomClientsInstruction = "clientes"
        self.specificClientInstruction = "cliente"
        self.parkInstruction = "parquear"
        
        #Create a City Graph Object
        self.cityGraph = CityObjects.createCityGraph(self.city)

        #Initialize the matrix of Labels that are going to compose the Window
        self.matrixOfLabels = self.city

        #Set all of the images
        self.taxiRightImage = Image.open("ProjectImages/taxiDerecha.png")
        self.taxiLeftImage = Image.open("ProjectImages/taxiIzquierda.png")
        self.taxiUpImage = Image.open("ProjectImages/taxiArriba.png")
        self.taxiDownImage = Image.open("ProjectImages/taxiAbajo.png")
        self.wallHorizontalImage = Image.open("ProjectImages/barreraHorizontal2.png")
        self.wallVerticalImage = Image.open("ProjectImages/barreraVertical2.png")
        self.streetImage = Image.open("ProjectImages/calle.png")
        self.waterImage = Image.open("ProjectImages/rio.png")
        self.cuadraSinIdentificacionImage = Image.open("ProjectImages/cuadraSinIdentificacion.png")
        self.cuadraIdentificada = ""
        
        #Set the master as the root
        self.master = master
        self.widthOfEachFrame = 0
        self.heightOfEachFrame = 0

        #This is going to be the Frame with the Button and Label that shows: Calculating route or Taxi on the way!
        self.taxiStateFrame = Frame(self.master, width=self.width, height=(self.height + 50) - (self.height), background="White")
        self.taxiStateFrame.place(x=0,y=(self.height))
        self.taxiStateButton = Button(self.taxiStateFrame, text="Taxi State",width= 20, height = 1, bg= "Black",fg='White',font = ('Kalinga','16'),relief='sunken')
        self.taxiStateButton.place(x=10,y=5)
        self.taxiStateLabel=Label(self.taxiStateFrame,width= 50, height = 1, bg= "Black",text='Welcome to the Taxi Simulation',fg='White',font = ('Kalinga','16'),relief='sunken')
        self.taxiStateLabel.place(x=350,y=10)

        #Here, we call the function in charge of build the city
        self.buildCity()

        #This instruction is in constant review for the instruction of the console
        self.getConsoleInstruction()

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
        elif(esCuadra == "no" and imageValue == " "):
            #Resize the image with the size of the square
            displayImage = self.streetImage.resize((width, height), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)
        elif(imageValue == "D"):
            #Resize the image with the size of the square
            displayImage = self.taxiRightImage.resize((width, height), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)
        elif(esCuadra == "yes"):
            if(imageValue == " "):
                #Resize the image with the size of the square
                displayImage = self.cuadraSinIdentificacionImage.resize((width, height), Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
            else:
                imagePath = "ProjectImages/" + imageValue + ".png"
                self.cuadraIdentificada = Image.open(imagePath)
                #Resize the image with the size of the square
                displayImage = self.cuadraIdentificada.resize((width, height), Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
        else:
            #Resize the image with the size of the square
            displayImage = self.streetImage.resize((width, height), Image.ANTIALIAS)
            displayImage = ImageTk.PhotoImage(displayImage)
            
        return displayImage


    #This function is in charge of get the instruction from the Console Window every updateTime
    def getConsoleInstruction(self):

        #This is to not assign animar as an instruction
        instruction = ConsoleGraphicalInterface.returnInstruction().split()
        if(len(instruction) > 1):
            if(instruction[1] != self.animateInstruction):
                self.actualInstruction = instruction #Get a list with the strings of the instruction
                
        #This part select the according method to execute depends on the instruction inserted by the user
        if(len(self.actualInstruction) > 1 and self.executingInstruction == False):
            if(self.actualInstruction[1] == self.travelInstruction):
                print("Entro aqui")
                self.doTravelInstruction()
            elif(self.actualInstruction[1] == self.searchInstruction):
                self.executingInstruction = True
                self.doSearchInstruction()
            elif(self.actualInstruction[1] == self.showInstruction):
                self.executingInstruction = True
                self.doShowInstruction()
            elif(self.actualInstruction[1] == self.routeInstruction):
                self.executingInstruction = True
                self.doRouteInstruction()
            elif(self.actualInstruction[1] == self.randomClientsInstruction):
                self.executingInstruction = True
                self.doRandomClientsInstruction()
            elif(self.actualInstruction[1] == self.specificClientInstruction):
                self.executingInstruction = True
                self.doSpecificClientInstruction()
            elif(self.actualInstruction[1] == self.specificClientInstruction):
                self.executingInstruction = True
                self.doSpecificClientInstruction()
            elif(self.actualInstruction[1] == self.parkInstruction):
                self.executingInstruction = True
                self.doParkInstruction()

        #If the user dont insert nothing for the first time
        else:
            if(self.executingInstruction == False):
                self.master.after(self.updateTime, self.getConsoleInstruction)    


        
    #This function is in charge of doing the travel instruction
    def doTravelInstruction(self):
        actualInstruction = ConsoleGraphicalInterface.returnInstruction().split() #Get a list with the strings of the instruction
        if(self.executingInstruction == False):
            self.executingInstruction = True
            #Do the travel instruction, and save the travel in the travelList
            routeToTravel = self.cityGraph.taxiTravel()
            self.travelList = routeToTravel[:]
            self.master.after(self.updateTime, self.doTravelInstruction)
        elif(actualInstruction[1] == "animar" and self.doAnimation == False and actualInstruction[2] != "0"):
            self.doAnimation = True
            self.updateTime = int(actualInstruction[2])
            self.master.after(self.updateTime, self.doTravelInstruction)
        elif(actualInstruction[1] == "animar" and actualInstruction[2] == "0"):
            self.doAnimation = False
            self.master.after(self.updateTime, self.doTravelInstruction)
        elif(self.doAnimation == True):
            #Do the animation
            if(self.travelList != []):
                i = self.travelList[0][0]
                j = self.travelList[0][1]

                #Initialize all of the variables
                taxiX = 0
                taxiY = 0

                #This part check when to used old variables
                if(self.taxiNode == 0):
                    self.taxiNode = self.cityGraph.searchTaxiNode()
                    taxiX = self.taxiNode.getX()
                    taxiY = self.taxiNode.getY()
                else:
                    taxiX = self.oldCoordinates[0]
                    taxiY = self.oldCoordinates[1]
                
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

                #Resize the image with the size of the square
                displayImage = self.resizeImage("no", "D", self.widthOfEachFrame, self.heightOfEachFrame)
                frame=Frame(self.master, width=self.widthOfEachFrame, height=self.heightOfEachFrame, background="White")
                frame.grid(row=i, column=j)
                
                #Create the Label and add it to the List of Labels
                label = Label(frame, image = displayImage)
                label.image = displayImage
                label.place(x=0,y=0)

                #Add the Label to the matrix
                self.matrixOfLabels[i][j] = label

                #Save the old coordinates
                self.oldCoordinates = [i,j]

                #Delete an item of the list
                del self.travelList[0]

                #Repeat the function with this timer
                self.master.after(self.updateTime, self.doTravelInstruction)
                
            #If the taxi get to its destination
            else:
                self.executingInstruction = False
                self.doAnimation = False
                print("El taxi ha llegado a su destino")
                self.cityGraph.updateInitialAndFinalValue() #Update the initial and the final node value
                self.master.after(self.updateTime, self.getConsoleInstruction)
            
        else:
            self.master.after(self.updateTime, self.doTravelInstruction)
            
         
        
    #This function is in charge of the taxi simulation
    def taxiSimulation(self):
        #Do the animation if is ok
        if(self.doAnimation == True):
            print()
        else:
            self.master.after(self.updateTime, self.doTravelInstruction)

#This function display the taxi simulation
def displayTaxiSimulation():
    master = Tk()#Create the principle window
    master.wm_title("Taxi Simulation") #Add a title to the window
    taxiSimulationWindow = TaxiSimulationWindow(master) #Add the taxi simulation frame to the principle window

    #This is used to build the City Graph
#    cityGraph = CityObjects.prueba(taxiSimulationWindow.city) #This returns the city graph
#    destinationNode = cityGraph.searchNodeByValue("B") #This is going to be the destination node
#    cityGraph.DFS(destinationNode) #This is the search algorithm
#    cityGraph.printRoute() #This function print the route
    
    master.geometry("1100x650") #Set the size of the root
    master.geometry("+0+10") #Set the position of the root on the screen
    master.resizable(width=NO,height=NO) #Set the window as no resizable
    master.mainloop() #Starts the mainloop of the console window
