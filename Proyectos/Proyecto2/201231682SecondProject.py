import _thread

import taxisimulationgui
import timergui
import congestionmaps

_thread.start_new_thread(taxisimulationgui.displayTaxiSimulation, ())
_thread.start_new_thread(timergui.displayTimer, ())
_thread.start_new_thread(congestionmaps.generateCongestionMaps, ())



