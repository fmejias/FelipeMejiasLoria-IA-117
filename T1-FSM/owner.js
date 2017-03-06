"use strict";
/**
 * This class is going to describe an Owner
 */
module.exports = class Owner {
  constructor() {
    this.ownerName = undefined;
    this.id = undefined;

  }

    /**
   * This method is going to assign the owner name and the owner id
   *
   */

  assignOwnerInformation(ownerName, id){
    this.ownerName = ownerName;
    this.id = id;
  }

  /**
   * This method prints the attributes of the Owner Object
   */
  printOwnerInformation() {
    console.log("El nombre del Owner es: " + this.ownerName + "\n");
    console.log("El id del Owner es: " + this.id + "\n");
  }

}