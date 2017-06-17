import _thread

import TaxiSimulationGraphicalInterface
import taxilearning
#import autonomoustaxi

_thread.start_new_thread(TaxiSimulationGraphicalInterface.displayTaxiSimulation, ())
_thread.start_new_thread(taxilearning.trainNeuralNetworkThread, ())
#_thread.start_new_thread(autonomoustaxi.autonomousTaxiThread, ())




