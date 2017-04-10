###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################

#Import of the standard Python interface to the Tk GUI toolkit
from tkinter import*
from PIL import ImageTk, Image


#Import from the MapParser module the city matrix
import MapParser

#Import to generate random numbers
from random import randint

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
        self.height = 650
        
        #Initialize the city matrix, get the number of rows of the city and the number of columns of the city
        self.city = MapParser.createMapParser()
        self.rows = len(self.city)
        self.columns = len(self.city[0])

        #Initialize the list of Labels that are going to compose the Window
        self.listOfLabels = []

        #Set all of the images
        self.taxiImage = PhotoImage(file="ProjectImages/taxi1.png")
        self.wallImage = PhotoImage(file="prueba.png")
        self.img = Image.open("barrera4.png")
        
        
        #Set the master as the root
        self.master = master

        #Here, we call the function in charge of build the city
        self.buildCity()

    #This method is in charge of build the city
    def buildCity(self):
        widthOfEachFrame = self.width // self.columns
        heightOfEachFrame = self.height // self.rows
        colors = ["Red", "Green", "Yellow", "Blue"]

        #Go over all the city matrix
        for i in range (0, self.rows):
            for j in range (0,self.columns):
                randomIndex = randint(0,3)
                frame=Frame(self.master, width=widthOfEachFrame, height=heightOfEachFrame, background=colors[randomIndex])
                frame.grid(row=i, column=j)

                #Resize the image with the size of the square
                displayImage = self.img.resize((widthOfEachFrame, heightOfEachFrame), Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)

                #Create the Label and add it to the List of Labels
                label = Label(frame, image = displayImage)
                label.image = displayImage
                label.place(x=0,y=0)
                self.listOfLabels.append(label) #Add the Label to the list
        


#This function display the taxi simulation
def displayTaxiSimulation():
    master = Tk()#Create the principle window
    master.wm_title("Taxi Simulation") #Add a title to the window
    taxiSimulationWindow = TaxiSimulationWindow(master) #Add the taxi simulation frame to the principle window
    master.geometry("1100x650") #Set the size of the root
    master.geometry("+0+10") #Set the position of the root on the screen
    master.resizable(width=NO,height=NO) #Set the window as no resizable
    master.mainloop() #Starts the mainloop of the console window
