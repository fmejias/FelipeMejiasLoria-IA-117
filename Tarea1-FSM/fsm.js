"use strict";

/**
 * Finite state machine implementation.
 */
module.exports = class Fsm {
  constructor() {
    this._owner = undefined;  //Owner of the state machine (The owner is an object type Owner)
    this._states = undefined; //States of the state machine (The states are represent by an array)
    this._current = undefined; //This atribute represents the actual state of the machine
  }
  
  //This method returns the Owner id
  id() {
    return this._owner.id;
  }
  
  //This method returns the object Owner
  owner() {
    return this._owner;
  } 

  /**
   * This method is going to assign the owner, the list of states 
   *
   */

  assignFSMInformation(owner, states, currentState){
    this._owner = owner;  //Owner of the state machine (The owner is an object type Owner)
    this._states = states; //States of the state machine (The states are represent by an array)
    this._current = currentState; //This atribute represents the actual state of the machine
  }

  /**
   * This method prints the attributes of the FSM Object
   */
  printFSMInformation() {
    console.log("El nombre del owner de la FSM es: " + this._owner.ownerName + "\n");
    console.log("El nombre del estado actual es: " + this._current.stateName + "\n");
    var i = 0;
    for (i = 0; i < this._states.length; i++){
        console.log("El nombre un estado de la maquina es: " + this._states[i].stateName + "\n"); 
      
    }
  }

  /**
   * Ciclo:
   * 1. Si el mensaje es "update"
   *   - mensaje especial para hacer update de los estados
   * 2. Si el mensaje no es "update"
   *   - recorrer los estados y ver si alguna lo reconoce
   *   - si lo reconoce activar el estado
   */
  onMessage(eventEmitter, event) {    
    if (event.msg === "update") {
      if (this._current) {
        this._current.onUpdate(eventEmitter, this);
        //Esto se agrega para estar verificando el estado actual de la maquina, así como el mensaje recibido
        console.log("El mensaje recibido es: " + event.msg + "\n");
        console.log("El estado actual de la máquina de estados es: " + this._current.stateName + "\n");
      }
    } else {
      const state = this._current.accepts(event.msg, this._states); //Revisa todos los estados hasta encontrar el que responde al evento y sea el estado actual
      const accepted = state && state !== this._current.stateName;
      console.log("El nombre del estado actual es: " + this._current.stateName);
      console.log("El mensaje recibido es: " + event.msg);
      console.log("El nombre del nuevo estado es: " + state);
      if (accepted) {
        if (this._current) {
          this._current.onExit(eventEmitter, this);
        }
        this._current = this._current.searchNextState(state, this._states);
        this._current.onEnter(eventEmitter, this, this._current.stateName);

        
      }
      console.log("\n");
    }
  }  
}