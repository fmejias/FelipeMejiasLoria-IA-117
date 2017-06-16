from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import RMSprop
from keras.layers.recurrent import LSTM
from keras.callbacks import Callback

from tensorflow.python.ops import control_flow_ops as tf_control_flow_ops
import tensorflow as tf

tf_control_flow_ops = tf

#Esta clase se utiliza en cada fase de entrenamiento para obtener el error obtenido y poder graficarlo
class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))


#Esta funcion es la encargada de crear la red neuronal
#Entradas: 1-) Numero de sensores
#Entradas: 2-) Numero de neuronas de la primera y la segunda capa: [164, 150]
def buildNeuralNetwork(sensorsNumber, numberOfNeurons):

    #Crear el tipo de modelo de la red neuronal, en este caso el modelo secuencial
    model = Sequential()

    #Primer paso: Crear la primera capa y asegurarse que tenga el numero de entradas correcto.
    #Esta es la primera capa, osea la capa de entrada.
    #Entradas de la primera capa: input_shape(num_sensors), osea el numero de sensores es el numero de entradas de la red
    #Numero de neuronas de esta capa: 164
    #Funcion de activacion: Activation(relu), osea la funcion rectificadora
    model.add(Dense(numberOfNeurons[0], kernel_initializer='lecun_uniform', input_shape=(sensorsNumber,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    #Esta es la segunda capa.
    #Numero de neuronas de esta capa: 150
    model.add(Dense(numberOfNeurons[1], kernel_initializer='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    #Esta es la capa de salida.
    #Numero de neuronas de esta capa son 3, y por tanto tiene 3 salidas
    #Las salidas son: 
    model.add(Dense(3, kernel_initializer='lecun_uniform'))
    model.add(Activation('linear'))

    #Se define el optimizador de la red, el cual se utiliza para calcular el gradiente y es necesario para la compilacion del modelo
    #El optimizador es el encargado de elegir entre los diferentes pesos
    rms = RMSprop()

    #Una vez definido el modelo se manda a compilar la red. El parametro loss indica la funcion que calcula el error
    model.compile(loss='mse', optimizer=rms)

    return model

