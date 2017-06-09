###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################

#Import of the standard Python interface to the Tk GUI toolkit
from tkinter import*

##Declaration of some global variables to comunicate with the Threads
timerWindow = ""
time = []

###########################################################################################################
# TimerWindow Class:
# Attributes: masterWindow, frameWindow, instruction. 
# Methods:
#
##########################################################################################################

class TimerWindow:
    def __init__(self, master):

        #####Variables need it for the timer ######
        self.timer = [5, 0, 0] #[hours,minutes,seconds]
        self.pattern = '{0:02d}:{1:02d}:{2:02d}' 
        self.start = True

        #Set the master as the root
        self.master = master

        #Here, we create a frame
        self.frame = Frame(self.master, width=1100, height=50, background="Black")
        self.frame.pack()

        #Buttons and labels for the timer GUI
        self.taxiClockButton = Button(self.frame, text="Clock",width= 15, height = 1, bg= "Black",fg='White',font = ('Kalinga','16'),relief='sunken')
        self.taxiClockButton.place(x=10,y=5)
        self.timeLabel=Label(self.frame,width= 10, height = 1, bg= "Black",text="00:00:00",fg='White',font = ('Kalinga','20'),relief='sunken')
        self.timeLabel.place(x=220,y=5)
        self.stopTimeButton = Button(self.frame, text="Detener",width= 15, height = 1, bg= "Black",fg='White',font = ('Kalinga','16'),relief='sunken',
                                     command = self.stopTimer)
        self.stopTimeButton.place(x=630,y=5)
        self.startTimeButton = Button(self.frame, text="Iniciar",width= 15, height = 1, bg= "Black",fg='White',font = ('Kalinga','16'),relief='sunken',
                                      command = self.startTimer)
        self.startTimeButton.place(x=830,y=5)
        self.forwardTimeButton = Button(self.frame, text="Adelantar hora",width= 15, height = 1, bg= "Black",fg='White',font = ('Kalinga','16'),relief='sunken',
                                        command = self.advanceHours)
        self.forwardTimeButton.place(x=430,y=5)

        ##Call the clock function
        self.update_time()

    #This method updates the time label
    def update_time(self):
        if(self.start == True):
            #Increment the seconds of the timer
            self.timer[2] += 1

            #Update the seconds, minutes and hours
            if (self.timer[2] >= 60):
                self.timer[1] += 1
                self.timer[2] = 0
            if (self.timer[1] >= 60):
                self.timer[0] += 1
                self.timer[1] = 0
            if (self.timer[0] >= 24):
                self.timer[0] = 0

            # We create our time string here
            timeString = self.pattern.format(self.timer[0], self.timer[1], self.timer[2])

            # Update the time
            self.timeLabel.configure(text=timeString)

            #Call the update function again
            self.master.after(1000, self.update_time)

    #This method stop the timer
    def stopTimer(self):
        self.start = False
        self.master.after(1000, self.update_time)

    #This method start the timer
    def startTimer(self):
        self.start = True
        self.master.after(1000, self.update_time)

    #This method advance the hours
    def advanceHours(self):
        #Advance the hours
        self.timer[0] += 1
        
        # We create our time string here
        timeString = self.pattern.format(self.timer[0], self.timer[1], self.timer[2])

        # Update the time
        self.timeLabel.configure(text=timeString)

        #Call the update function again
        self.master.after(1000, self.update_time)
        
    #This method return the time
    def getTime(self):
        return self.timer

#This function display the timer
def displayTimer():
    global timerWindow #Declaration of the global Timer Window object
    master = Tk()#Create the principle window
    master.wm_title("Clock") #Add a title to the window
    timerWindow = TimerWindow(master) #Add the timer frame to the principle window
    master.geometry("1100x50") #Set the size of the root
    master.geometry("+0+638") #Set the position of the root on the screen
    master.resizable(width=NO,height=NO) #Set the window as no resizable
    master.mainloop() #Starts the mainloop of the timer window

#This function returns the actual time
def returnTime():
    global timerWindow
    global time
    time = timerWindow.getTime()
    time = str(time[0]) + ":" + str(time[1]) 
    return time
