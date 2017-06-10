###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################

#This import is need it to use the _thread module
import _thread

#This import is necessary to call functions of the TaxiSimulationGraphicalInterface module
import TaxiSimulationGraphicalInterface

#This import is necessary to call functions of the TimerGraphicalInterface module
import TimerGraphicalInterface

#This import is necessary to call functions of the CongestionMaps module
import CongestionMaps

#Here, we initialize the main threads
_thread.start_new_thread(TaxiSimulationGraphicalInterface.displayTaxiSimulation, ())
_thread.start_new_thread(TimerGraphicalInterface.displayTimer, ())
_thread.start_new_thread(CongestionMaps.generateCongestionMaps, ())



