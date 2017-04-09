#This import is need it to use the _thread module
import _thread

#This import is need it to show the first window
import screen1

#This import is need it to show the second window
import screen2

#Here, we initialize the threads
_thread.start_new_thread(screen1.display , ())
_thread.start_new_thread(screen2.display , ())

#We create an infinite loop
#while 1:
 #   pass
