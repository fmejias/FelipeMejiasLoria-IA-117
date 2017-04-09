#Import of the standard Python interface to the Tk GUI toolkit
from tkinter import*

master=Tk()
master.geometry("400x300")

frame1=Frame(master, width=200, height=150, background="Blue")
frame1.grid(row=0, column=0)

frame2=Frame(master, width=200, height=150, background="Red")
frame2.grid(row=1, column=0)

frame3=Frame(master, width=200, height=150, background="Green")
frame3.grid(row=0, column=1)

frame4=Frame(master, width=200, height=150, background="Yellow")
frame4.grid(row=1, column=1)

master.mainloop()
