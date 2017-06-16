from tkinter import*
from PIL import ImageTk, Image

import MapParser
import CityObjects

import copy
import time

taxiSimulationWindow = None

class TaxiSimulationWindow:
    def __init__(self, master):
        #Establish the width and height of the First Window
        self.width = 1100
        self.height = 600
        
        #Initialize the city matrix, get the number of rows of the city and the number of columns of the city
        self.city = MapParser.createMapParser()
        self.rows = len(self.city)
        self.columns = len(self.city[0])

        #This is used to save the old coordinates of the taxi
        self.oldCoordinates = []
        self.taxiNode = 0
        
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
        self.clientImage = Image.open("ProjectImages/cliente1.jpg")
        self.routeImage = Image.open("ProjectImages/ruta1.png")
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
            displayImage = self.wallHorizontalImage.resize((width, height), Image.ANTIALIAS)
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

    ##This method is in charge of make a move of the taxi
    def makeMove(self, action):
        taxiNode = self.cityGraph.searchTaxi()
        x = taxiNode.getX()
        y = taxiNode.getY()
        reward = 0
        state = []
        if(action == 1):
            self.paintStreet(x,y)
            self.paintTaxi(x,y+1)
            time.sleep(0.1)
            
            reward = self.cityGraph.calculateReward(action)
            self.cityGraph.updateTaxiCoordinates(action)
            state = copy.deepcopy(self.cityGraph.calculateState())
            
            #If the taxi crashed with something
            if(reward == -500):
                self.cityGraph.updateTaxiWallCoordinates(2)
                self.paintWall(x,y+1)
                self.paintTaxi(x,y)
                time.sleep(0.1)
                
        elif(action == 2):
            self.paintStreet(x,y)
            self.paintTaxi(x,y-1)
            time.sleep(0.1)
            reward = self.cityGraph.calculateReward(action)
            self.cityGraph.updateTaxiCoordinates(action)
            state = copy.deepcopy(self.cityGraph.calculateState())
            
            #If the taxi crashed with something
            if(reward == -500):
                self.cityGraph.updateTaxiWallCoordinates(1)
                self.paintWall(x,y-1)
                self.paintTaxi(x,y)
                time.sleep(0.1)
                
        elif(action == 3):
            self.paintStreet(x,y)
            self.paintTaxi(x-1,y)
            time.sleep(0.1)
            
            reward = self.cityGraph.calculateReward(action)
            self.cityGraph.updateTaxiCoordinates(action)
            state = copy.deepcopy(self.cityGraph.calculateState())
            
            #If the taxi crashed with something
            if(reward == -500):
                self.cityGraph.updateTaxiWallCoordinates(4)
                self.paintWall(x-1,y)
                self.paintTaxi(x,y)
                time.sleep(0.1)
                
        elif(action == 4):
            self.paintStreet(x,y)
            self.paintTaxi(x+1,y)
            time.sleep(0.1)
            
            reward = self.cityGraph.calculateReward(action)
            self.cityGraph.updateTaxiCoordinates(action)
            state = copy.deepcopy(self.cityGraph.calculateState())
            
            #If the taxi crashed with something
            if(reward == -500):
                self.cityGraph.updateTaxiWallCoordinates(3)
                self.paintWall(x+1,y)
                self.paintTaxi(x,y)
                time.sleep(0.1)

        else: #Si no debe hacer nada
            reward = self.cityGraph.calculateReward(action)
            self.cityGraph.updateTaxiCoordinates(action)
            state = copy.deepcopy(self.cityGraph.calculateState())

        return [reward, state]


    #This method paint a wall
    def paintWall(self,x,y):
        #Paint the image of the wall
            
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
             
    ##This method paint the taxi again
    def paintTaxi(self,x, y):
        
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

    ##This method paint the taxi again
    def paintStreet(self,x, y):
        
        #Resize the image with the size of the square
        displayImage = self.resizeImage("no", " ", self.widthOfEachFrame, self.heightOfEachFrame)
        frame=Frame(self.master, width=self.widthOfEachFrame, height=self.heightOfEachFrame, background="White")
        frame.grid(row=x, column=y)
        
        #Create the Label and add it to the List of Labels
        label = Label(frame, image = displayImage)
        label.image = displayImage
        label.place(x=0,y=0)

        #Add the Label to the matrix
        self.matrixOfLabels[x][y] = label

#Despliega la interfaz grafica
def displayTaxiSimulation():
    global taxiSimulationWindow
    master = Tk()
    master.wm_title("Taxi Simulation") 
    taxiSimulationWindow = TaxiSimulationWindow(master) 
    master.geometry("1100x650") 
    master.geometry("+0+10") 
    master.resizable(width=NO,height=NO) 
    master.mainloop()

#Llamada por el hilo que se encarga de entrenar a la red neuronal
def makeMove(action):
    global taxiSimulationWindow
    state = [0,0,0,0]
    reward = 0
    rewardStateList = []
    if(taxiSimulationWindow is not None):
        rewardStateList = taxiSimulationWindow.makeMove(action)
    else:
        rewardStateList = [reward, state]
    return rewardStateList

