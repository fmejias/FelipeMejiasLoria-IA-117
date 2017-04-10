###########################################Artificial Intelligence###############################################                    
####################################Professor: Ing. Luis Carlos##################################################
#################################################################################################################
########################################Student: Felipe Mejias Loria ############################################
#################################################################################################################

#This import is need it to use the _thread module
import _thread

#This import is necessary to call functions of the ConsoleGraphicalInterface module
import ConsoleGraphicalInterface

#This import is necessary to call functions of the TaxiSimulationGraphicalInterface module
import TaxiSimulationGraphicalInterface

#Call the function in charge of display the console window
#ConsoleGraphicalInterface.displayConsole()

#Call the function in charge of display the taxi simulation window
#TaxiSimulationGraphicalInterface.displayTaxiSimulation()

#Here, we initialize the threads
_thread.start_new_thread(TaxiSimulationGraphicalInterface.displayTaxiSimulation, ())
_thread.start_new_thread(ConsoleGraphicalInterface.displayConsole, ())

