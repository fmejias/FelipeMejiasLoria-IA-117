
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
var state_1 = new State(); //This state is going to be: Descansando
var state_2 = new State(); //This state is going to be: Enojado
var state_3 = new State(); //This state is going to be: Molesto 
var state_4 = new State(); //This state is going to be Furioso

/**
*Third, we have to create the owner the FSM
*/
var owner_1 = new Owner();
owner_1.assignOwnerInformation("FSM1", 1);


/*
 * Now, we have to create the Event Objects of the first state (Descansando)
 *
 */
 var event_1 = new Event();
 event_1.assignEventInformation("Herido", "Enojado");

 var event_2 = new Event();
 event_2.assignEventInformation("Elemento en su area", "Molesto"); 

 var event_3 = new Event();
 event_3.assignEventInformation("Elemento fuera de su area", "Descansando"); 

 var event_4 = new Event();
 event_4.assignEventInformation("Sanando", "Descansando"); 

/*
 * Now, we have to create the Event Objects of the second state (Enojado)
 *
 */

 var event_5 = new Event();
 event_5.assignEventInformation("Sanando", "Molesto");

 var event_6= new Event();
 event_6.assignEventInformation("Herido", "Furioso");

 var event_7 = new Event();
 event_5.assignEventInformation("Elemento en su area", "Enojado");

 var event_8= new Event();
 event_6.assignEventInformation("Elemento fuera de su area", "Enojado");

 /*
 * Now, we have to create the Event Objects of the third state (Molesto)
 *
 */

 var event_9 = new Event();
 event_9.assignEventInformation("Herido", "Enojado");

 var event_10= new Event();
 event_10.assignEventInformation("Sanando", "Descansando");

 var event_11 = new Event();
 event_11.assignEventInformation("Elemento en su area", "Molesto");

 var event_12= new Event();
 event_12.assignEventInformation("Elemento fuera de su area", "Descansando");

 /*
 * Now, we have to create the Event Objects of the fourth state (Furioso)
 *
 */

 var event_13 = new Event();
 event_13.assignEventInformation("Sanando", "Enojado");

 var event_14= new Event();
 event_14.assignEventInformation("Herido", "Furioso");

 var event_15 = new Event();
 event_15.assignEventInformation("Elemento en su area", "Furioso");

 var event_16 = new Event();
 event_16.assignEventInformation("Elemento fuera de su area", "Furioso");

 /*
  * Now we have to add the Event Objects to an array, so we can add it to the list of events of each state
  * State 1 = Descansando , State2 = Enojado, State3 = Molesto, State4 = Furioso
  */

  var listOfEventsState1 = [event_1, event_2, event_3, event_4];
  var listOfEventsState2 = [event_5, event_6, event_7, event_8];
  var listOfEventsState3 = [event_9, event_10, event_11, event_12];
  var listOfEventsState4 = [event_13, event_14, event_15, event_16];

/*
 * Now, we have to add the information of the states
 *
 */
 state_1.assignStateInformation("Descansando", "activo", listOfEventsState1);
 state_2.assignStateInformation("Enojado", "inactivo", listOfEventsState2);
 state_3.assignStateInformation("Molesto", "inactivo", listOfEventsState3);
 state_4.assignStateInformation("Furioso", "inactivo", listOfEventsState4);
 
 /*
  * Then. we have to create the list of sttes
  */
 var listOfStates = [state_1, state_2, state_3, state_4];

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
var message = "Herido";

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

