import TaxiSimulationGraphicalInterface
import numpy as np
import threading
import random
import csv
from neuralnetwork import buildNeuralNetwork, LossHistory
import os.path

NUM_INPUT = 4
GAMMA = 0.9

neuralNetworkNumberOfNeurons = [164, 150]
parameters = {
    "batchSize": 100,
    "buffer": 50000,
    "neuralNetwork": neuralNetworkNumberOfNeurons
}
neuralNetworkModel = buildNeuralNetwork(NUM_INPUT, neuralNetworkNumberOfNeurons)
epsilon = 1
time = 0
state = 0
listOfExperiences = []
loss_log = []
firstStateCalculated = False
calculatingTrainingData = False

def trainNeuralNetwork():
    global neuralNetworkModel
    global epsilon
    global firstStateCalculated
    global time
    global state
    global listOfExperiences
    global loss_log 
    global parameters
    global calculatingTrainingData

    filename = params_to_filename(parameters)
    timeToObserveBeforeTraining = 300
    timeToTrain = 1000
    batchSize = parameters['batchSize']
    buffer = parameters['buffer']
    action = 0

    if(firstStateCalculated == False):
        rewardStateList = TaxiSimulationGraphicalInterface.makeMove(0)
        reward = rewardStateList[0]
        state = np.array([rewardStateList[1]])
        firstStateCalculated = True

    time = time + 1

    if random.random() < epsilon or time < timeToObserveBeforeTraining:
        action = np.random.randint(0, 4)  
    else: 
        
        qval = neuralNetworkModel.predict(state, batch_size=1) 
        action = (np.argmax(qval))

    rewardStateList = TaxiSimulationGraphicalInterface.makeMove(action)
    reward = rewardStateList[0]
    newState = rewardStateList[1]
    newState = np.array([rewardStateList[1]])

    listOfExperiences.append((state, action, reward, newState))

    if time > timeToObserveBeforeTraining:
        if(calculatingTrainingData == False):
            print("Calculando datos de entrada")
            calculatingTrainingData = True

        if len(listOfExperiences) > buffer:
            listOfExperiences.pop(0)

        trainingData = random.sample(listOfExperiences, batchSize)

        xTrainingData, yTrainingData = calculateTrainingData(trainingData, neuralNetworkModel)

        history = LossHistory()
        neuralNetworkModel.fit(
            xTrainingData, yTrainingData, batch_size=batchSize,
            epochs=1, verbose=0, callbacks=[history]
        )

        loss_log.append(history.losses)

    state = newState

    if epsilon > 0.1 and time > timeToObserveBeforeTraining:
        epsilon -= (1/timeToTrain)

    if time == 600:
        neuralNetworkModel.save_weights('savedmodels/' + filename + '.h5',
                           overwrite=True)
        print("Saving model %s - %d" % (filename, time))

        log_results(filename, loss_log)

def log_results(filename, loss_log):
    with open('results/loss_data-' + filename + '.csv', 'w') as lf:
        wr = csv.writer(lf)
        for loss_item in loss_log:
            wr.writerow(loss_item)

def calculateTrainingData(experiences, model):
    xTrainingData = []
    yTrainingData = []
    for memory in experiences:
        old_state_m, action_m, reward_m, new_state_m = memory
        old_qval = model.predict(old_state_m, batch_size=1)
        newQ = model.predict(new_state_m, batch_size=1)
        maxQ = np.max(newQ)
        y = np.zeros((1, 4))
        y[:] = old_qval[:] 
        if reward_m != -500:  
            update = (reward_m + (GAMMA * maxQ))
        else: 
            update = reward_m
        y[0][action_m] = update 
        xTrainingData.append(old_state_m.reshape(NUM_INPUT,))
        yTrainingData.append(y.reshape(4,))

    xTrainingData = np.array(xTrainingData)
    yTrainingData = np.array(yTrainingData)

    return xTrainingData, yTrainingData

def params_to_filename(params):
    return str(params['neuralNetwork'][0]) + '-' + str(params['neuralNetwork'][1]) + '-' + \
            str(params['batchSize']) + '-' + str(params['buffer'])

def trainNeuralNetworkThread():
    trainNeuralNetwork()
    threading.Timer(0.3, trainNeuralNetworkThread).start()


