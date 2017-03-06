"use strict";
/**
 * This class is going to describe an Event, to analyze the transitions between states
 */
module.exports = class Event {
  constructor() {
    this.eventName = "";
    this.nextState = "";

  }

  /**
   * This method is going to assign the event name and the next state
   *
   */

  assignEventInformation(eventName, nextState){
    this.eventName = eventName;
    this.nextState = nextState;
  }


  /**
   * This method prints the attributes of the Event Object
   */
  printEventInformation() {
    console.log("El nombre del evento es: " + this.eventName + "\n");
    console.log("El nombre del siguiente estado al que apunta es: " + this.nextState + "\n");
  }

}