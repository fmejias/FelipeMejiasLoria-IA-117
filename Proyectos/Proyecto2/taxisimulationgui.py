from tkinter import*
from PIL import ImageTk, Image
import copy
import time
import random

import fileparser
import timergui
import taxistrategy
import cityobjects
import buildings
import taxi

taxiSimulationWindow = None
cityGraph = ""

class TaxiSimulationWindow:
    class __TaxiSimulationWindow:
        def __init__(self, master): 
            self.width = 1100
            self.height = 600
            self.city = fileparser.createMapParser()
            self.rows = len(self.city)
            self.columns = len(self.city[0])
            self.clientsParser = fileparser.FileParser()
            self.taxiStrategy = taxistrategy.TaxiStrategy()
            self.actualTime = "0:00"
            self.updateTime = 50
            self.travelList = []
            self.cityGraph = cityobjects.createCityGraph(self.city)
            self.apartmentController = buildings.ApartmentController(self.cityGraph.searchAllWorkplaces())
            self.workplaceController = buildings.WorkplaceController(self.cityGraph.searchAllWorkplaces())
            self.taxiController = taxi.TaxiController(self.cityGraph.searchAllTaxisId())
            self.listOfApartmentPositions = self.cityGraph.searchAllApartmentsPosition()
            self.listOfWorkplacesPositions = self.cityGraph.searchAllWorkplacesPosition()
            self.listOfApartmentsThatNeedToWork = []
            self.listOfWorkplacesThatNeedToGoHome = []
            self.matrixOfLabels = self.city
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
            self.master = master
            self.widthOfEachFrame = 0
            self.heightOfEachFrame = 0

            self.buildCity()
            self.buildingsInformationFrame = Frame(self.master, width=260,
                                                   height=600, background="peru")
            self.buildingsInformationFrame.place(x=1085, y = 0)
            self.buttonBuildingInformation = Button(self.buildingsInformationFrame,
                                                    text="Horarios en los edificios", width= 25,
                                                    height = 1, bg= "#A6420B",fg='white',font = ('Kalinga','12'))
            self.buttonBuildingInformation.place(x=10,y=5)
            
            self.createApartmentsAndClients()
            self.createBuildingsInformation()
            self.paintNumberOfClients()
            self.startWorking()

        def createApartmentsAndClients(self):
            listOfNumberOfClientsAndApartmentNames = self.clientsParser.parseClients()
            listOfAllWorkplaces = self.cityGraph.searchAllWorkplaces()

            for i in range(0, len(listOfNumberOfClientsAndApartmentNames)):
                apartmentName = listOfNumberOfClientsAndApartmentNames[i][0]
                apartmentClients = listOfNumberOfClientsAndApartmentNames[i][1]
                workplace = random.choice(listOfAllWorkplaces)
                self.apartmentController.addApartment(apartmentName, apartmentClients, workplace)
            self.workplaceController = self.apartmentController.getWorkplaceController()

        def createBuildingsInformation(self):
            buildingsList = self.cityGraph.searchAllBuildings()
            frameX = 5
            frameY = 60

            for i in range(0,len(buildingsList)):
                buildingInformation1 = Frame(self.buildingsInformationFrame,
                                             width=250, height=150, background="moccasin")
                buildingInformation1.place(x=frameX, y = frameY)
                buildingImage = Image.open("ProjectImages/" + "apartamento"
                                           + buildingsList[i] + ".png")
                buildingImage = buildingImage.resize((80, 71), Image.ANTIALIAS)
                buildingImage = ImageTk.PhotoImage(buildingImage)
                leaveArriveSchedule = self.apartmentController.getLeaveArriveSchedule(buildingsList[i])
                buildingName = "Edificio " + buildingsList[i]
                labelTitle = Label(buildingInformation1, text=buildingName,
                                   width= 10,height = 2, bg= "moccasin",
                                   fg='black',font = ('Kalinga','12'))
                labelTitle.grid(row=0, column = 0)
                labelOut = Label(buildingInformation1,
                                 text="Salida: " + leaveArriveSchedule[0] + " am",
                                 width= 15,height = 2, bg= "moccasin",
                                 fg='black',font = ('Kalinga','12'))
                labelOut.grid(row=0,column=1)
                labelImage = Label(buildingInformation1,
                                   image=buildingImage, bg= "moccasin",
                                   fg='black',font = ('Kalinga','12'))
                labelImage.image = buildingImage
                labelImage.grid(row=1, column = 0)
                labelIn = Label(buildingInformation1,
                                text="Entrada: " + leaveArriveSchedule[1] + " pm",
                                width= 15,height = 4, bg= "moccasin",fg='black',
                                font = ('Kalinga','12'))
                labelIn.grid(row=1,column=1)
                frameY = frameY + 140

        def paintNumberOfClients(self):
            listOfCoordinatesOfApartments = self.cityGraph.searchAllApartmentsPosition()
            listOfNumberOfClients = self.clientsParser.parseClients()

            for i in range(0, len(listOfCoordinatesOfApartments)):
                apartment = listOfCoordinatesOfApartments[i][0] 
                x = listOfCoordinatesOfApartments[i][1][0]
                y = listOfCoordinatesOfApartments[i][1][1]
                numberOfClients = 0

                for j in range(0, len(listOfNumberOfClients)):
                    if(listOfNumberOfClients[j][0] == apartment):
                        numberOfClients = listOfNumberOfClients[j][1]
                        break

                imagePath = "ProjectImages/" + numberOfClients + ".png"
                self.clientsNumber = Image.open(imagePath)
                displayImage = self.clientsNumber.resize((self.widthOfEachFrame,
                                                          self.heightOfEachFrame),
                                                         Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
                frame=Frame(self.master, width=self.widthOfEachFrame,
                            height=self.heightOfEachFrame, background="White")
                frame.grid(row=x, column=y+1)
                label = Label(frame, image = displayImage)
                label.image = displayImage
                label.place(x=0,y=0)
                self.matrixOfLabels[x][y+1] = label

        def buildCity(self):
            self.widthOfEachFrame = self.width // self.columns
            self.heightOfEachFrame = self.height // self.rows
            
            for i in range (0, self.rows):
                for j in range (0,self.columns):
                    frame=Frame(self.master, width=self.widthOfEachFrame,
                                height=self.heightOfEachFrame, background="White")
                    frame.grid(row=i, column=j)
                    displayImage = self.resizeImage(self.city[i][j][0],
                                                    self.city[i][j][1],
                                                    self.widthOfEachFrame,
                                                    self.heightOfEachFrame)
                    label = Label(frame, image = displayImage)
                    label.image = displayImage
                    label.place(x=0,y=0)
                    self.matrixOfLabels[i][j] = label
            
        def resizeImage(self,esCuadra,imageValue,width,height):
            displayImage = 0
            if(imageValue == "-"):
                displayImage = self.wallHorizontalImage.resize((width, height),
                                                               Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
            elif(imageValue == "|"):
                displayImage = self.wallVerticalImage.resize((width, height),
                                                             Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
            elif(imageValue == "*"):
                displayImage = self.waterImage.resize((width, height),
                                                      Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
            elif(imageValue == "V"):
                displayImage = self.routeImage.resize((width, height),
                                                      Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)        
            elif(imageValue == "O"):
                displayImage = self.clientImage.resize((width, height),
                                                       Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
            elif(esCuadra == "no" and imageValue == " "):
                displayImage = self.streetImage.resize((width, height),
                                                       Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
            elif(imageValue.isdigit() == True):
                imagePath = "ProjectImages/" + "taxi" + imageValue + ".png"
                self.taxi = Image.open(imagePath)
                displayImage = self.taxi.resize((width, height),
                                                Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
            elif(esCuadra == "yes"):
                if(imageValue == " "):
                    displayImage = self.cuadraSinIdentificacionImage.resize((width, height),
                                                                            Image.ANTIALIAS)
                    displayImage = ImageTk.PhotoImage(displayImage)
                elif(imageValue.isupper() == True): 
                    imagePath = "ProjectImages/" + "apartamento" + imageValue + ".png"
                    self.cuadraIdentificada = Image.open(imagePath)
                    displayImage = self.cuadraIdentificada.resize((width, height),
                                                                  Image.ANTIALIAS)
                    displayImage = ImageTk.PhotoImage(displayImage)
                else:
                    imagePath = "ProjectImages/" + "trabajo" + imageValue + ".png"
                    self.cuadraIdentificada = Image.open(imagePath)
                    displayImage = self.cuadraIdentificada.resize((width, height),
                                                                  Image.ANTIALIAS)
                    displayImage = ImageTk.PhotoImage(displayImage)
            else:
                displayImage = self.streetImage.resize((width, height),
                                                       Image.ANTIALIAS)
                displayImage = ImageTk.PhotoImage(displayImage)
                
            return displayImage

        def startWorking(self):
            self.actualTime = timergui.returnTime()
            self.checkClientsToGoToWorkToGoHome(self.actualTime)
            self.master.after(self.updateTime, self.enableTaxisServices)

        def searchClientsInApartment(self):
            apartmentsWithClientsOutside = self.listOfApartmentsThatNeedToWork

            for i in range(0, len(apartmentsWithClientsOutside)):
                apartmentName = apartmentsWithClientsOutside[i][0]
                taxiNearClient = self.cityGraph.pickAClient(apartmentName)
                
                if(taxiNearClient != ""):
                    taxiHaveClient = self.taxiController.getTaxiWithClient(taxiNearClient)

                    if(taxiHaveClient == False):
                        listOfClients = self.apartmentController.getClientsToGoToWork(
                            apartmentName, self.actualTime)
                        client = listOfClients[0]
                        client.goToWork()
                        destinationOfClient = client.getDestinationBlock()
                        taxiRoad = self.cityGraph.travelWithClientRoad(
                            destinationOfClient, taxiNearClient)
                        self.apartmentController.clientGrabbedATaxi(apartmentName)
                        self.taxiController.setTaxiRoad(taxiRoad, taxiNearClient)
                        self.taxiController.setTaxiWithClient(taxiNearClient)
                        
                        for j in range(0, len(self.listOfApartmentPositions)):
                            apartment = self.listOfApartmentPositions[j][0] 
                            x = self.listOfApartmentPositions[j][1][0]
                            y = self.listOfApartmentPositions[j][1][1]

                            if(apartment == apartmentName):
                                self.paintWall(x-1,y)
                                break
                            
                        del listOfClients[0]

        def searchClientsInWorkplaces(self):
            workplacesWithClientsOutside = self.listOfWorkplacesThatNeedToGoHome
            for i in range(0, len(workplacesWithClientsOutside)):
                workplaceName = workplacesWithClientsOutside[i][0]
                taxiNearClient = self.cityGraph.pickAClient(workplaceName) 

                if(taxiNearClient != ""):
                    taxiHaveClient = self.taxiController.getTaxiWithClient(taxiNearClient)

                    if(taxiHaveClient == False):
                        listOfClients = self.workplaceController.getClientsToGoHome(
                            workplaceName, self.actualTime)
                        client = listOfClients[0]
                        client.goToWork()
                        destinationOfClient = client.getInitialBlock()
                        taxiRoad = self.cityGraph.travelWithClientRoad(
                            destinationOfClient, taxiNearClient)
                        self.workplaceController.clientGrabbedATaxi(workplaceName)
                        self.taxiController.setTaxiRoad(taxiRoad, taxiNearClient)
                        self.taxiController.setTaxiWithClient(taxiNearClient)
                        
                        for j in range(0, len(self.listOfWorkplacesPositions)):
                            workplace = self.listOfWorkplacesPositions[j][0] 
                            x = self.listOfWorkplacesPositions[j][1][0]
                            y = self.listOfWorkplacesPositions[j][1][1]

                            if(workplace == workplaceName):
                                self.paintWall(x-1,y)
                                break

                        del listOfClients[0]
            
        def searchClients(self):
            if(self.actualTime == "07:00" or
               self.actualTime == "08:00" or
               self.actualTime == "09:00"):
                self.searchClientsInApartment() 
            elif(self.actualTime == "12:00"):
                self.searchClientsInWorkplaces() 

        def enableTaxisServices(self):
            actualPositions = self.cityGraph.searchAllTaxisPosition()
            self.searchClients()
            newPositions = self.taxiStrategy.generateMovements(
                actualPositions, self.cityGraph.returnCityGraph(), self.taxiController)
            self.taxiController.checkAlreadyInDestination()
            self.cityGraph.updateTaxisPosition(newPositions)

            for i in range(0, len(actualPositions)):
                taxiX = actualPositions[i][1][0]
                taxiY= actualPositions[i][1][1]
                displayImage = self.resizeImage("no", " ",
                                                self.widthOfEachFrame, self.heightOfEachFrame)
                frame=Frame(self.master, width=self.widthOfEachFrame,
                            height=self.heightOfEachFrame, background="White")
                frame.grid(row=taxiX, column=taxiY)
                label = Label(frame, image = displayImage)
                label.image = displayImage
                label.place(x=0,y=0)
                self.matrixOfLabels[taxiX][taxiY] = label

            for j in range(0, len(newPositions)):
                taxiX = newPositions[j][1][0]
                taxiY= newPositions[j][1][1]
                taxiName = newPositions[j][0]
                displayImage = self.resizeImage("no",
                                                taxiName, self.widthOfEachFrame, self.heightOfEachFrame)
                frame=Frame(self.master, width=self.widthOfEachFrame,
                            height=self.heightOfEachFrame, background="White")
                frame.grid(row=taxiX, column=taxiY)
                label = Label(frame, image = displayImage)
                label.image = displayImage
                label.place(x=0,y=0)
                self.matrixOfLabels[taxiX][taxiY] = label

            self.master.after(self.updateTime, self.startWorking)

        def paintClient(self,x,y):
            displayImage = self.resizeImage("no", "O",
                                            self.widthOfEachFrame, self.heightOfEachFrame)
            frame=Frame(self.master, width=self.widthOfEachFrame,
                        height=self.heightOfEachFrame, background="White")
            frame.grid(row=x, column=y)
            label = Label(frame, image = displayImage)
            label.image = displayImage
            label.place(x=0,y=0)
            self.matrixOfLabels[x][y] = label

        def paintWall(self,x,y):
            displayImage = self.resizeImage("no", "-",
                                            self.widthOfEachFrame, self.heightOfEachFrame)
            frame=Frame(self.master, width=self.widthOfEachFrame,
                        height=self.heightOfEachFrame, background="White")
            frame.grid(row=x, column=y)
            label = Label(frame, image = displayImage)
            label.image = displayImage
            label.place(x=0,y=0)
            self.matrixOfLabels[x][y] = label

        def checkClientsToGoToWorkToGoHome(self, time):
            self.listOfApartmentsThatNeedToWork = self.apartmentController.checkClientsToGoToWork(time)
            self.listOfWorkplacesThatNeedToGoHome = self.workplaceController.checkClientsToGoHome(time)
            listOfClientsToErase = self.apartmentController.checkClientsToEraseFromApartment()

            for i in range(0, len(self.listOfApartmentsThatNeedToWork)):
                putAClient = self.listOfApartmentsThatNeedToWork[i][1]
                apartmentName = self.listOfApartmentsThatNeedToWork[i][0]
                if(putAClient == True):
                    for j in range(0, len(self.listOfApartmentPositions)):
                        apartment = self.listOfApartmentPositions[j][0] 
                        x = self.listOfApartmentPositions[j][1][0]
                        y = self.listOfApartmentPositions[j][1][1]

                        if(apartment == apartmentName):
                            self.paintClient(x-1,y)
                            break

            for i in range(0, len(self.listOfWorkplacesThatNeedToGoHome)):
                putAClient = self.listOfWorkplacesThatNeedToGoHome[i][1]
                workplaceName = self.listOfWorkplacesThatNeedToGoHome[i][0]
                if(putAClient == True):
                    for j in range(0, len(self.listOfWorkplacesPositions)):
                        workplace = self.listOfWorkplacesPositions[j][0] 
                        x = self.listOfWorkplacesPositions[j][1][0]
                        y = self.listOfWorkplacesPositions[j][1][1]

                        if(workplace == workplaceName):
                            self.paintClient(x-1,y)
                            break

        def getCityGraph(self):
            return self.cityGraph.returnCityGraph()

    instance = None
    def __init__(self, master):
        if not TaxiSimulationWindow.instance:
            TaxiSimulationWindow.instance = TaxiSimulationWindow.__TaxiSimulationWindow(master)
        else:
            TaxiSimulationWindow.instance.master = master
    def __getattr__(self, name):
        return getattr(self.instance, name)
        
def displayTaxiSimulation():
    global taxiSimulationWindow
    global cityGraph
    master = Tk()
    master.wm_title("Taxi Simulation") 
    taxiSimulationWindow = TaxiSimulationWindow(master) 
    master.geometry("1350x600") 
    master.geometry("+0+10") 
    master.resizable(width=NO,height=NO) 
    master.mainloop() 

def returnCityGraph():
    global taxiSimulationWindow
    global cityGraph
    if(taxiSimulationWindow is not None):
        cityGraph = taxiSimulationWindow.getCityGraph()
    else:
        cityGraph = []
    return cityGraph
