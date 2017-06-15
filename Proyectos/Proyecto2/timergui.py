from tkinter import*

timerWindow = ""
time = []

class TimerWindow:
    class __TimerWindow:
        def __init__(self, master):
            
            self.timer = [5, 0, 0] 
            self.pattern = '{0:02d}:{1:02d}:{2:02d}'
            self.patternOutput = '{0:02d}:{1:02d}' 
            self.start = True
            self.master = master
            self.frame = Frame(self.master, width=1250, height=50, background="Black")
            self.frame.pack()
            self.taxiClockButton = Button(self.frame,
                                          text="Clock",width= 15, height = 1,
                                          bg= "Black",fg='White',font = ('Kalinga','16'),
                                          relief='sunken')
            self.taxiClockButton.place(x=10,y=5)
            self.timeLabel=Label(self.frame,width= 10, height = 1, bg= "Black",
                                 text="00:00:00",fg='White',font = ('Kalinga','20'),
                                 relief='sunken')
            self.timeLabel.place(x=220,y=5)
            self.stopTimeButton = Button(self.frame, text="Detener",width= 15,
                                         height = 1, bg= "Black",fg='White',
                                         font = ('Kalinga','16'),relief='sunken',
                                         command = self.stopTimer)
            self.stopTimeButton.place(x=630,y=5)
            self.startTimeButton = Button(self.frame, text="Iniciar",width= 15,
                                          height = 1, bg= "Black",fg='White',
                                          font = ('Kalinga','16'),relief='sunken',
                                          command = self.startTimer)
            self.startTimeButton.place(x=830,y=5)
            self.forwardHoursButton = Button(self.frame, text="Adelantar hora",
                                             width= 15, height = 1, bg= "Black",
                                             fg='White',font = ('Kalinga','16'),relief='sunken',
                                            command = self.advanceHours)
            self.forwardHoursButton.place(x=430,y=5)
            self.forwardMinutesButton = Button(self.frame, text="Adelantar minutos",
                                               width= 15, height = 1, bg= "Black",
                                               fg='White',font = ('Kalinga','16'),relief='sunken',
                                            command = self.advanceMinutes)
            self.forwardMinutesButton.place(x=1030,y=5)
            self.update_time()
            
        def update_time(self):
            if(self.start == True):
                self.timer[2] += 1
                if (self.timer[2] >= 60):
                    self.timer[1] += 1
                    self.timer[2] = 0
                if (self.timer[1] >= 60):
                    self.timer[0] += 1
                    self.timer[1] = 0
                if (self.timer[0] >= 24):
                    self.timer[0] = 0

                timeString = self.pattern.format(self.timer[0],
                                                 self.timer[1], self.timer[2])
                self.timeLabel.configure(text=timeString)
                self.master.after(1000, self.update_time)

        def stopTimer(self):
            self.start = False
            self.master.after(1000, self.update_time)

        def startTimer(self):
            self.start = True
            self.master.after(1000, self.update_time)

        def advanceHours(self):
            self.timer[0] += 1
            timeString = self.pattern.format(self.timer[0],
                                             self.timer[1], self.timer[2])
            self.timeLabel.configure(text=timeString)
            self.master.after(1000, self.update_time)

        def advanceMinutes(self):
            self.timer[1] += 1
            timeString = self.pattern.format(self.timer[0],
                                             self.timer[1], self.timer[2])
            self.timeLabel.configure(text=timeString)
            self.master.after(1000, self.update_time)

        def getTime(self):
            return self.patternOutput.format(self.timer[0],
                                             self.timer[1])
        
    instance = None
    def __init__(self, master):
        if not TimerWindow.instance:
            TimerWindow.instance = TimerWindow.__TimerWindow(master)
        else:
            TimerWindow.instance.master = master
    def __getattr__(self, name):
        return getattr(self.instance, name)

def displayTimer():
    global timerWindow 
    master = Tk()
    master.wm_title("Clock") 
    timerWindow = TimerWindow(master) 
    master.geometry("1250x50") 
    master.geometry("+0+638")
    master.resizable(width=NO,height=NO) 
    master.mainloop() 

def returnTime():
    global timerWindow
    global time
    time = timerWindow.getTime()
    return time
