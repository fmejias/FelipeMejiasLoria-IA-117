###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################

#Import of the standard Python interface to the Tk GUI toolkit
from tkinter import*

###########################################################################################################
# TaxiSimulationWindow Class:
# Attributes: masterWindow, frameWindow, instruction. 
# Methods:
# .
##########################################################################################################

class TaxiSimulationWindow:
    def __init__(self, master):

        #Initialize the instruction variable
        self.instruction = ""

        #Initialize the variables to position the entries
        self.x = 0
        self.y = 20

        #Initialize the variable that contains the actual instruction entry
        self.actualEntry = ""

        #Set the master as the root
        self.master = master

        #Here, we create a frame
        self.frame = Frame(self.master, width=1000, height=600, background="White")
        self.frame.pack()



#This function display the taxi simulation
def displayTaxiSimulation():
    master = Tk()#Create the principle window
    master.wm_title("Taxi Simulation Window") #Add a title to the window
    taxiSimulationWindow = TaxiSimulationWindow(master) #Add the taxi simulation frame to the principle window
    master.geometry("1000x600") #Set the size of the root
    master.geometry("+10+50") #Set the position of the root on the screen
    master.resizable(width=NO,height=NO) #Set the window as no resizable
    master.mainloop() #Starts the mainloop of the console window
