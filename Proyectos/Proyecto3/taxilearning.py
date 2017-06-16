import TaxiSimulationGraphicalInterface
import numpy as np
import threading
import random
import csv
from neuralnetwork import buildNeuralNetwork, LossHistory
import os.path

#Definicion de las constantes del numero de sensores 
NUM_INPUT = 4
GAMMA = 0.9

#Variables globales
neuralNetworkNumberOfNeurons = [164, 150]
parameters = {
    "batchSize": 100,
    "buffer": 50000,
    "neuralNetwork": neuralNetworkNumberOfNeurons
}
neuralNetworkModel = buildNeuralNetwork(NUM_INPUT, neuralNetworkNumberOfNeurons)
epsilon = 1
filename = params_to_filename(parameters)
time = 0

#Metodo para entrenar a la red
def trainNeuralNetwork():
    global neuralNetworkModel
    global epsilon
    global time
    
    #Parametros necesarios para el entrenamiento de la red
    framesToObserveBeforeTraining = 1000 
    
    framesToTrain = 1000000  # Number of frames to play.
    batchSize = parameters['batchSize']
    buffer = parameters['buffer']
    t = 0
    listOfExperiences = []  # stores tuples of (S, A, R, S').
    loss_log = []

    #Crea una instancia de la simulacion del taxi
    taxiSimulationState = taxisimulation.GameState()

    #Obtiene el estado inicial de la simulacion para poder empezar a calcular las experiencias
    reward, state = TaxiSimulationGraphicalInterface.makeMove(0)


    #Cuando el ciclo se cumpla ya se el carro puede manejar sin chocar con ningun obstaculo
    while t < framesToTrain:

        t += 1
        
        #Elige una accion a realizar(Mover a la izquierda, a la derecha o no hacer nada)
        if random.random() < epsilon or t < framesToObserveBeforeTraining:
            action = np.random.randint(0, 3)  #Elige una accion a realizar random
        else: #Cuando ya se tiene entrenada a la red
            #Obtiene todos los valores Q del estado en el que se encuentra calculados por la red
            qval = neuralNetworkModel.predict(state, batch_size=1) #Calcular el arreglo de los valores Q
            action = (np.argmax(qval))  #Obtiene el Q mas alto, osea la accion que debe realizar

        #Realiza la accion calculada en la instruccion anterior y se obtiene el nuevo estado
        reward, new_state = taxiSimulationState.frame_step(action)

        #Se almacena la experiencia
        listOfExperiences.append((state, action, reward, new_state))

        #Una vez que se ha calculado bastante experiencia, se empieza a entrenar la red
        if t > framesToObserveBeforeTraining:

            #Una vez que tengamos bastantes experiencias almacenadas, sacamos del buffer la experiencia mas vieja
            if len(listOfExperiences) > buffer:
                listOfExperiences.pop(0)

            #Se seleccionan de forma random 100 experiencias para generar los datos de entrenamiento
            trainingData = random.sample(listOfExperiences, batchSize)

            #Se obtienen los valores con los que se va a entrenar a la red(X,Y)
            X_train, y_train = calculateTrainingData(trainingData, neuralNetworkModel)

            #Se entrena a la red con los datos calculados en la instruccion anterior
            history = LossHistory()
            neuralNetworkModel.fit(
                X_train, y_train, batch_size=batchSize,
                nb_epoch=1, verbose=0, callbacks=[history]
            )

            #Almacena el error obtenido para graficarlo al final de la ejecucion 
            loss_log.append(history.losses)

        #Se actualiza el estado por el estado siguiente calculado para la experiencia
        #Esto es necesario para que la experiencia se vaya calculando con el estado de cada movimiento realizado
        state = new_state

        #Se disminuye el epsilon conforme transcurre el tiempo
        if epsilon > 0.1 and t > framesToObserveBeforeTraining:
            epsilon -= (1/framesToTrain)

        #Guarda el modelo cada 25000 frames
        if t % 25000 == 0:
            neuralNetworkModel.save_weights('savedmodels/' + filename + '-' +
                               str(t) + '.h5',
                               overwrite=True)
            print("Saving model %s - %d" % (filename, t))


#Este metodo calcula los datos con los que se va entrenando a la red
def calculateTrainingData(experiences, model):
    xTrainingData = []
    yTrainingData = []
    # Loop through our batch and create arrays for X and y
    # so that we can fit our model at every step.
    for memory in experiences:
        # Get stored values.
        old_state_m, action_m, reward_m, new_state_m = memory
        # Get prediction on old state.
        old_qval = model.predict(old_state_m, batch_size=1)
        # Get prediction on new state.
        newQ = model.predict(new_state_m, batch_size=1)
        # Get our best move. I think?
        maxQ = np.max(newQ)
        y = np.zeros((1, 3)) #Retorna un arreglo de ceros
        y[:] = old_qval[:] #Le asigna a y el arreglo de salida de la red para el estado viejo. El Q es un arreglo de 3. Se ve asi: y = [[x,y,z]]
        # Check for terminal state.
        if reward_m != -500:  # non-terminal state
            update = (reward_m + (GAMMA * maxQ))
        else:  # terminal state
            update = reward_m
        # Update the value for the action we took.
        y[0][action_m] = update #Como y = [[x,y,z]], por eso hay que hacer y[0], para obtener este arreglo
        xTrainingData.append(old_state_m.reshape(NUM_INPUT,))
        yTrainingData.append(y.reshape(3,))

    xTrainingData = np.array(xTrainingData)
    yTrainingData = np.array(yTrainingData)

    return xTrainingData, yTrainingData

def params_to_filename(params):
    return str(params['neuralNetwork'][0]) + '-' + str(params['neuralNetwork'][1]) + '-' + \
            str(params['batchSize']) + '-' + str(params['buffer'])


#ESte metodo se esta llamando cada segundo para entrenar a la red cada segundo
def trainNeuralNetworkThread():
    trainNeuralNetwork()
    threading.Timer(1, trainNeuralNetworkThread).start()


