/*
  The toJSONClass() will be used to instantiate an object in the scenario editor
  HTML given values to replace the name, turn, point and author. After it is 
  instantiated, it's method will be called whenever an onclick even occurs 
  to one of it's related buttons. After this occurs, the hashmap hashJSON
  will be updated with the new objects. Once the submit method is used, the 
  JSON file will be formed using the hashmap and then sent to the back end.
*/

function toJSONClass() {


    //TODO: 
        //Create xHTTP request and create a file that contains the JSON info
        //figure out how to get values from the map for the location editor

    //Scenario properties
    this.name = 'NULL';
    this.turn_num = 20;
    this.point_num = 20;
    this.author = 'NULL';

    this.charKey = 0;
    this.eventKey = 0;
    this.locKey = 0;

    //hashMap to contain input, passed from 
    this.hashJSON = [];

    //Character related methods
    this.add_char = function() {    

        //Fetch the desired attributes for the character
        var charName = document.getElementById('charNameBox').value;
        var isKey = document.getElementById('keyCharBox').value;
        var charNotes = document.getElementById('charComment').value;

        //Create a character object to match with the fixture.json format
        var charObj = {
            model:"editor.character",
            pk:charKey, 
            fields:{
                name: charName,
                key: isKey,
                notes: charNotes
            }
        };

        //Add the character object to the hashmap where the pk will be used
        //to determine this objects location
        hashJSON[charKey] = charObj;

        //Need to add the character object to the table as well...
        var newCharElement = document.getElementById("charsTable").insertRow(0);
        newCharElement.innerHTML = charName;
        
        //incrememnt the key associated with character objects. 
        this.charKey++;
    }

    this.edit_char = function() {
        
        var charName = document.getElementById('charNameBox').value;
        var isKey = document.getElementById('keyCharBox').value;
        var charNotes = document.getElementById('charComment').value;
        

//TODO: Need to change the charKey so that it matches with the desired char
//maybe using getElementById(table element).selected()["key"] or something

        //check that the entry already exists
        if(charKey in hashJSON){
                //Use key value to locate the object in the hashmap and then set  
                //it to a new object using the hashmap
                hashJSON[charKey] = {
                    model:"editor.character",
                    key:charKey,
                    fields:{
                        name: charName,
                        key: isKey,
                        notes: charNotes
                    }
                };

            //also need to edit that specified value in the table 
            var editCharElement = document.getElementById("charsTable").item(charKey);
            editCharElement.innerHTML = charName;
        }


    }

    this.del_char = function() {

    //TODO: Again, need to fix things here...
        //Check that the key is in hashJSON and delete it if so. 
        if(charKey in hashJSON){
            delete hashJSON[charKey];

            //delete the row from the table as well
            document.getElementById("charsTable").deleteRow(charKey);
        }
    }

    //Event related methods
    this.add_event = function() {
        
        var eventName = document.getElementById('eventNameBox').value;
        var isKey = document.getElementById('eventKeyBox').value;
        var isSecret = document.getElementById('eventSecretBox').value;
        
        /*
        Need to account for the more complex ones... 

        var eventSnip = document.getElementById('').value;
        var tagTurn = document.getElementById('').value;
        var tagType = document.getElementById('').value;
        var tagTarget = document.getElementById('').value;
        */

        //Create an event object to match with the fixture.json format
        var eventObj = {
            model:"editor.event",
            pk:eventKey,
            fields:{
                name: eventName,
                key: isKey,
                secret: isSecret
                /*
                snippet: eventSnip,
                turn: tagTurn,
                type: tagType,
                target: tagTarget
                */
            }
        };

        //Add the character object to the hashmap where the pk will be used
        //to determine this objects location
        hashJSON[eventKey] = eventObj;

         
        var newEventElement = document.getElementById("eventTable").insertRow(0);
        newEventElement.innerHTML = eventName;
        
        this.eventKey++;
    }

    this.edit_event = function() {
        
        var eventName = document.getElementById('eventNameBox').value;
        var isKey = document.getElementById('eventKeyBox').value;
        var isSecret = document.getElementById('eventSecretBox').value;
        
        if(eventKey in hashJSON){
            hashJSON[eventKey] = {
                model:"editor.event",
                pk:eventKey,
                fields:{
                    name: eventName,
                    key: isKey,
                    secret: isSecret
                    /*
                    snippet: eventSnip,
                    turn: tagTurn,
                    type: tagType,
                    target: tagTarget
                    */
                }
            };

            var editEventElement = document.getElementById("eventTable").item(eventKey);
            editEventElement.innerHTML = eventName;
        
        }
    }

    this.del_event = function() {
        
        if(eventKey in hashJSON){
            delete hashJSON[eventKey];
            //delete the table entry
            document.getElementById("eventTable").deleteRow(eventKey);

        }
    }

    //Location related methods
    this.add_loc = function() {
        
        
//TODO: figure out how to get the values from the map...

        var locName = "test";
        var locCoordX = 0;
        var locCoordY = 0;

        //Create a location object to match with the fixture.json format
        var locObj = {
            model:"editor.location",
            pk:locKey,
            fields:{
                name: locName,
                x: locCoordX,
                y: locCoordY
            }
        };

        hashJSON[locKey] = locObj;

        var newLocElement = document.getElementById("locsTable").insertRow(0);
        newLocElement.innerHTML = charName;
        
        this.locKey++;

    }

    this.edit_loc = function() {
       
        var locName = "test";
        var locCoordX = 0;
        var locCoordY = 0;
        
        //check that the entry already exists
        if(locKey in hashJSON){
                this.hashJSON[pk] = {
                    model:"editor.location",
                    pk:locKey,
                    fields:{
                        name: locName,
                        x: locCoordX,
                        y: locCoordY
                    }
                };

            var editLocElement = document.getElementById("locsTable").item(locKey);
            editLocElement.innerHTML = locName;

        }

    }

    this.del_loc = function() {
        
        if(locKey in hashJSON){
            delete hashJSON[locKey];
            document.getElementById("locsTable").deleteRow(locKey);
        }
    }


    //Final method to submit the JSON currently stored in hashJSON
    this.submitJSON = function(){
        
        //Create a final array that will contain the JSON objects
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


var currEdit = new toJSONCLass();
