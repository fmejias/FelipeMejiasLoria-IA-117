from tkinter import *
import time

#This is the class of the first window
class SecondWindow():
    def __init__(self, master):

        #Set the master as the root
        self.master = master

        #Initialize the count variable
        self.count = 1

        #Here, we create a frame
        self.frame = Frame(master)
        self.frame.pack()

        #This label is used to set the title= "Conteo"
        self.label = Label(self.frame , text = "Conteo" , font = ("Helvetica",32))
        self.label.grid(row = 0)

        #This label is used to be updating every second
        self.reading_label = Label(self.frame, text = '0.0' , font = ("Helvetica",70))
        self.reading_label.grid(row = 1)
        
        self.update_reading()


    #This method update the root every second
    def update_reading(self):
        self.reading_label.configure(text = str(self.count))
        self.count = self.count + 1
        self.master.after(1000, self.update_reading)


#This function display the second window for the first time
def display():
    root = Tk() #Instantiate the top level window
    root.wm_title("Second Window") #Add a title to the window
    secondWindow = SecondWindow(root) #Add the first window to the root
    root.geometry("480x320") #Set the size of the root
    root.mainloop() #Starts the mainloop of the first window
