"use strict";
/**
 * This class is going to describe a State
 */
module.exports = class State {
  constructor() {
    this.stateName = undefined;
    this.stateValue = undefined; //The state value can be: "activo" or "inactivo"
    this.eventList = undefined;

  }

   /**
   * This method is going to assign the state name, the state value and the event list
   *
   */

  assignStateInformation(name, stateValue, eventList){
    this.stateName = name;
    this.stateValue = stateValue; //The state value can be: "active" or "inactive"
    this.eventList = eventList;
  }

  /**
   * This method receives the name of the event and must check if the state has that event on the List of events, also check if thats the actual state
   */
  accepts(event, states) {
    var x = 0;
    var n = 0;
    for (n = 0; n < states.length; n++){
      for (x = 0; x < states[n].eventList.length; x++){
        if( (states[n].eventList[x].eventName == event) && (states[n].stateValue == "activo") ){
          return states[n].eventList[x].nextState;
      }
    }
    }
    
  }


  /**
   * This method gets the next state
   */
  searchNextState(name, states) {
    var p = 0;
    for (p = 0; p < states.length; p++){
        if( (states[p].stateName == name)){
       //   console.log("El siguiente estado es: " + states[p].stateName);
          return states[p];
      }
     // if( this.name == name){
      //  return this.name == name;
    //  }
    
  }

}

  /**
   * This method receives the state machine, so it has to go over the list of states of the machine and activate that state as the actual state
   * to do that, we have to get the name of this state and loop over the list of states until we find that state and activate as the actual state
   */
  onEnter(eventEmitter, fsm, newStateName) {
    var y = 0;
    for (y = 0; y < fsm._states.length; y++){
      if( (fsm._states[y].stateName == newStateName) ){
        fsm._states[y].stateValue = "activo";
        console.log("El estado que acaba de pasar a activo es: " + fsm._states[y].stateName);
        
      }
    }     
  }

  /**
   * Si el estado esta activo se llama con cada ciclo
   * En este método va a ir el contador especial para
   */
  onUpdate(eventEmitter, fsm) {     
  }


  /**
   * This method is in charge of deactivate the actual state, is going to receive the fsm, then we have to go over the list of states
   * till we find the state that we have to deactive
   */
  onExit(eventEmitter, fsm) {     
    var i = 0;
    for (i = 0; i < fsm._states.length; i++){
      if( (fsm._states[i].stateValue == "activo") ){
        fsm._states[i].stateValue = "inactivo";
        console.log("El estado que acaba de pasar a inactivo es: " + fsm._states[i].stateName);
      }
    }
  }
}