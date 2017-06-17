from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import RMSprop
from keras.layers.recurrent import LSTM
from keras.callbacks import Callback

from tensorflow.python.ops import control_flow_ops as tf_control_flow_ops
import tensorflow as tf

tf_control_flow_ops = tf

class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))

def buildNeuralNetwork(sensorsNumber, numberOfNeurons, load=''):
    model = Sequential()
    model.add(Dense(numberOfNeurons[0], kernel_initializer='lecun_uniform', input_shape=(sensorsNumber,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(numberOfNeurons[1], kernel_initializer='lecun_uniform'))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(4, kernel_initializer='lecun_uniform'))
    model.add(Activation('linear'))

    rms = RMSprop()

    model.compile(loss='mse', optimizer=rms)

    if load:
        model.load_weights(load)

    return model

