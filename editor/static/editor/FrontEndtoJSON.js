/*
  The toJSONClass() will be used to instantiate an object in the scenario editor
  HTML given values to replace the name, turn, point and author. After it is 
  instantiated, it's method will be called whenever an onclick even occurs 
  to one of it's related buttons. After this occurs, the hashmap hashJSON
  will be updated with the new objects. Once the submit method is used, the 
  JSON file will be formed using the hashmap and then sent to the back end.
*/

function toJSONClass() {

    //Scenario properties
    this.name = 'NULL';
    this.turn_num = 20;
    this.point_num = 20;
    this.author = 'NULL';

    //hashMap to contain input, passed from 
    this.hashJSON = [];

    //Character related methods
    this.add_char = function(charName, isKey, charNotes) {

        //Create a character object to match with the fixture.json format
        var charObj = {
            model:"editor.character",
            pk:42,
            fields:{
                name: charName,
                key: isKey,
                notes: charNotes
            }
        };

        //Add the character object to the hashmap where the pk will be used
        //to determine this objects location
        this.hashJSON[pk] = charObj;

    }

    this.edit_char = function(charName, isKey, charNotes) {
        
        //check that the entry already exists
        if(pk in hashJSON){
                //Use key value to locate the object in the hashmap and then set  
                //it to a new object using the hashmap
                hashJSON[pk] = {
                    model:"editor.character",
                    pk:42,
                    fields:{
                        name: charName,
                        key: isKey,
                        notes: charNotes
                    }
                };
        }

    }

    this.del_char = function(charName, isKey, charNotes) {
        //Check that the key is in hashJSON and delete it if so. 
        if(pk in hashJSON){
            delete hashJSON[pk];
        }
    }

    //Event related methods
    this.add_event = function(eventName, isKey, isSecret, eventSnip, tagTurn,
    tagType, tagTarget) {
        
        //Create an event object to match with the fixture.json format
        var eventObj = {
            model:"editor.event",
            pk:42,
            fields:{
                name: eventName,
                key: isKey,
                secret: isSecret,
                snippet: eventSnip,
                turn: tagTurn,
                type: tagType,
                target: tagTarget
            }
        };

        //Add the character object to the hashmap where the pk will be used
        //to determine this objects location
        hashJSON[pk] = eventObj;
    }

    this.edit_event = function(eventName, isKey, isSecret, eventSnip, tagTurn,   
    tagType, tagTarget) {
        
        if(pk in hashJSON){
            hashJSON[pk] = {
                model:"editor.event",
                pk:42,
                fields:{
                    name: eventName,
                    key: isKey,
                    secret: isSecret,
                    snippet: eventSnip,
                    turn: tagTurn,
                    type: tagType,
                    target: tagTarget
                }
            };
        }
    }

    this.del_event = function(eventName, isKey, isSecret, eventSnip, tagTurn,   
    tagType, tagTarget) {
        
        if(pk in hashJSON){
            delete hashJSON[pk];
        }
    }

    //Location related methods
    this.add_loc = function(locName, locCoordX, locCoordY) {
        
        //Create a location object to match with the fixture.json format
        var locObj = {
            model:"editor.location",
            pk:42,
            fields:{
                name: locName,
                x: locCoordX,
                y: locCoordY
            }
        };

        hashJSON[pk] = locObj;

    }

    this.edit_loc = function(locName, locCoordX, locCoordY) {
       
        //check that the entry already exists
        if(pk in hashJSON){
                this.hashJSON[pk] = {
                    model:"editor.location",
                    pk:42,
                    fields:{
                        name: locName,
                        x: locCoordX,
                        y: locCoordY
                    }
                };
        }

    }

    this.del_loc = function(locName, locCoordX, locCoordY) {
        
        if(pk in hashJSON){
            delete hashJSON[pk];
        }
    }


    //Final method to submit the JSON currently stored in hashJSON
    this.submitJSON = function(){
        
        //Create a final array tat will contain the JSON objects
        var JSONarr = [];

        //Iterate through each object in the hashMap
        for(var key in hashJSON){
            
            //Get the key values of the hashmap
            var value = hashJSON[key];


            //Iterate through each filed in the value of the hashmap
            for(var field in value){ 
                //push each object to the JSON array
                JSONarr.push(value[field]);
            }

        }

        //Generate the JSON file using stringify on the JSON array
        //after the hashmap has been iterated through
        var JSONfile = JSON.stringify(JSONarr);


    }



}


