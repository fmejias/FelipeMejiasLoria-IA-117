import TaxiSimulationGraphicalInterface
import numpy as np
import threading
import random
from neuralnetwork import buildNeuralNetwork, LossHistory
import os.path

NUM_INPUT = 4
GAMMA = 0.9

neuralNetworkNumberOfNeurons = [164, 150]
saved_model = 'savedmodels/164-150-100-50000.h5'
neuralNetworkModel = buildNeuralNetwork(NUM_INPUT, neuralNetworkNumberOfNeurons, saved_model)
state = 0
firstStateCalculated = False

def simulateAutonomousTaxi():
    global neuralNetworkModel
    global firstStateCalculated
    global state

    if(firstStateCalculated == False):
        rewardStateList = TaxiSimulationGraphicalInterface.makeMove(0)
        reward = rewardStateList[0]
        state = np.array([rewardStateList[1]])
        firstStateCalculated = True

    action = (np.argmax(neuralNetworkModel.predict(state, batch_size=1)))
    rewardStateList = TaxiSimulationGraphicalInterface.makeMove(action)
    state = np.array([rewardStateList[1]])

#ESte metodo se esta llamando cada segundo para entrenar a la red cada segundo
def autonomousTaxiThread():
    simulateAutonomousTaxi()
    threading.Timer(0.1, autonomousTaxiThread).start()

