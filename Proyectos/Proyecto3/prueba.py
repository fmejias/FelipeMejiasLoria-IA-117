import TaxiSimulationGraphicalInterface
import threading
import numpy as np

def getRewardState():
    action = np.random.randint(0, 4)  #Elige una accion a realizar random
    TaxiSimulationGraphicalInterface.makeMove(action)


def makeMove():
    getRewardState()
    threading.Timer(1, makeMove).start()
