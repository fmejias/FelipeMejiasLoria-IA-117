
/*
 * Definition of the classes
 *
 */
var FSM = require('./fsm');
var State = require('./state');
var Owner = require('./owner');
var Event = require('./event');

/**
*First, we have to create the Event Emitter and the FSM
*/
const eventEmitter = require ('./event-emiter');
var state_machine = new FSM();

/**
*Second, we have to create the states of the FSM
*/
var state_1 = new State();
var state_2 = new State();

/**
*Third, we have to create the owner the FSM
*/
var owner_1 = new Owner();
owner_1.assignOwnerInformation("FSM1", 1);


/*
 * Now, we have to create the Event Objects of the first state (Apagado)
 *
 */
 var event_1 = new Event();
 event_1.assignEventInformation("apagar", "Apagado");

 var event_2 = new Event();
 event_2.assignEventInformation("encender", "Encendido"); 

/*
 * Now, we have to create the Event Objects of the second state (Encendido)
 *
 */

 var event_3 = new Event();
 event_3.assignEventInformation("apagar", "Apagado");

 var event_4 = new Event();
 event_4.assignEventInformation("encender", "Encendido");

 /*
  * Now we have to add the Event Objects to an array, so we can add it to the list of events of each state
  * State 1 = Apagado , State2 = Encendido
  */

  var listOfEventsState1 = [event_1, event_2];
  var listOfEventsState2 = [event_3, event_4];

/*
 * Now, we have to add the information of the states
 *
 */
 state_1.assignStateInformation("Apagado", "activo", listOfEventsState1);
 state_2.assignStateInformation("Encendido", "inactivo", listOfEventsState2);
 
 /*
  * Then. we have to create the list of sttes
  */
 var listOfStates = [state_1, state_2];

 /*
  * Now, we have to update the state machine attributes
  *
  */
  state_machine.assignFSMInformation(owner_1, listOfStates,  state_1);

//Then, after we create the state machine and the Event Emitter, we have to register the FSM into the Event Emitter
eventEmitter.register(state_machine);


/**
 * Principal cycle
 */

//We define a new variable to change messages
var message = "encender";

//This function is changing the message
function changeMessage(){
	if(message == "encender"){
		message = "apagar";
	}
	else{
		message = "encender";
	}
}

setInterval(() => {
  eventEmitter.update();
  eventEmitter.send(message);
  changeMessage();
}, 1000); 

