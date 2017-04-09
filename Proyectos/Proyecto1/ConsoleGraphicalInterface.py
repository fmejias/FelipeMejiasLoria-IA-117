###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################

#Import of the standard Python interface to the Tk GUI toolkit
from tkinter import*

###########################################################################################################
# ConsoleWindow Class:
# Attributes: masterWindow, frameWindow, instruction. 
# Methods:
#
##########################################################################################################

class ConsoleWindow:
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
        self.master.bind('<Return>', self.getInstruction) #This is use to get the instruction when I pressed Enter key

        #Here, we create a frame
        self.frame = Frame(self.master, width=200, height=600, background="Black")
        self.frame.pack()

        #This label is used to set the title= "Console Window"
        self.label = Label(self.frame , text = "Console Window" , font = ("Helvetica",12), background = "Black", fg = "White")
        self.label.place(x = 0, y = 0)

        #Here we create the initial entry
        e1=Entry(self.frame, width=200, background = "Black", fg = "White")
        e1.place(x = self.x, y = self.y)

        #Insert initial text to the entry
        e1.delete(0, END)
        e1.insert(0, "> ")

        #Update the actual entry
        self.actualEntry = e1

    #This method get the instruction when I press the Enter Key
    def getInstruction(self,event):
        #Update the y coordinate
        self.y = self.y + 20

        #Get the actual instruction
        instruction = self.actualEntry.get()
        print("La instrucción es: ", instruction)

        #Here we create an entry
        e=Entry(self.frame, width=200, background = "Black", fg = "White")
        e.place(x = self.x, y = self.y)

        #Insert initial text to the entry
        e.delete(0, END)
        e.insert(0, "> ")

        #Update the actual entry
        self.actualEntry = e
        


#This function display the console
def displayConsole():
    master = Tk()#Create the principle window
    master.wm_title("Console Window") #Add a title to the window
    consoleWindow = ConsoleWindow(master) #Add the console frame to the principle window
    master.geometry("200x600") #Set the size of the root
    master.geometry("+1100+50") #Set the position of the root on the screen
    master.resizable(width=NO,height=NO) #Set the window as no resizable
    master.mainloop() #Starts the mainloop of the console window
