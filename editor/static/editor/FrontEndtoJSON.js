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


    var classInstance = {};

    //Scenario properties
    classInstance.name = 'NULL';
    classInstance.turn_num = 20;
    classInstance.point_num = 20;
    classInstance.author = 'NULL';

    classInstance.charKey = 0;
    classInstance.eventKey = 0;
    classInstance.locKey = 0;

    //hashMap to contain input, passed from 
    classInstance.hashJSON = [];

    //Character related methods
    classInstance.add_char = function() {    

        //Fetch the desired attributes for the character
        var charName = document.GetElementByID('charNameBox').value;
        var isKey = document.GetElementByID('keyCharBox').value;
        var charNotes = document.GetElementByID('charComment').value;

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
        classInstance.hashJSON[charKey] = charObj;

        //Need to add the character object to the table as well...
        var newCharElement = document.getElementById("charsTable").insertRow(0);
        newCharElement.innerHTML = charName;
        
        //incrememnt the key associated with character objects. 
        classInstance.charKey++;
    }

    classInstance.edit_char = function() {
        
        var charName = document.GetElementByID('charNameBox').value;
        var isKey = document.GetElementByID('keyCharBox').value;
        var charNotes = document.GetElementByID('charComment').value;
        

//TODO: Need to change the charKey so that it matches with the desired char
//maybe using GetElementByID(table element).selected()["key"] or something

        //check that the entry already exists
        if(charKey in classInstance.hashJSON){
                //Use key value to locate the object in the hashmap and then set  
                //it to a new object using the hashmap
                classInstance.hashJSON[charKey] = {
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

    classInstance.del_char = function() {

    //TODO: Again, need to fix things here...
        //Check that the key is in hashJSON and delete it if so. 
        if(charKey in classInstance.hashJSON){
            delete classInstance.hashJSON[charKey];

            //delete the row from the table as well
            document.getElementById("charsTable").deleteRow(charKey);
        }
    }

    //Event related methods
    classInstance.add_event = function() {
        
        var eventName = document.GetElementByID('eventNameBox').value;
        var isKey = document.GetElementByID('eventKeyBox').value;
        var isSecret = document.GetElementByID('eventSecretBox').value;
        
        /*
        Need to account for the more complex ones... 

        var eventSnip = document.GetElementByID('').value;
        var tagTurn = document.GetElementByID('').value;
        var tagType = document.GetElementByID('').value;
        var tagTarget = document.GetElementByID('').value;
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
        classInstance.hashJSON[eventKey] = eventObj;

         
        var newEventElement = document.getElementById("eventTable").insertRow(0);
        newEventElement.innerHTML = eventName;
        
        classInstance.eventKey++;
    }

    classInstance.edit_event = function() {
        
        var eventName = document.GetElementByID('eventNameBox').value;
        var isKey = document.GetElementByID('eventKeyBox').value;
        var isSecret = document.GetElementByID('eventSecretBox').value;
        
        if(eventKey in classInstance.hashJSON){
            classInstnace.hashJSON[eventKey] = {
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

    classInstance.del_event = function() {
        
        if(eventKey in classInstance.hashJSON){
            delete classInstance.hashJSON[eventKey];
            //delete the table entry
            document.getElementById("eventTable").deleteRow(eventKey);

        }
    }

    //Location related methods
    classInstance.add_loc = function() {
        
        
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

        classInstance.hashJSON[locKey] = locObj;

        var newLocElement = document.getElementById("locsTable").insertRow(0);
        newLocElement.innerHTML = charName;
        
         classInstance.locKey++;

    }

    classInstance.edit_loc = function() {
       
        var locName = "test";
        var locCoordX = 0;
        var locCoordY = 0;
        
        //check that the entry already exists
        if(locKey in classInstance.hashJSON){
                classInstance.hashJSON[locKey] = {
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

    classInstance.del_loc = function() {
        
        if(locKey in classInstance.hashJSON){
            delete classInstance.hashJSON[locKey];
            document.getElementById("locsTable").deleteRow(locKey);
        }
    }


    //Final method to submit the JSON currently stored in hashJSON
    classInstance.submitJSON = function(){
        
        //Create a final array that will contain the JSON objects
        var JSONarr = [];

        //Iterate through each object in the hashMap
        for(var key in classInstance.hashJSON){
            
            //Get the key values of the hashmap
            var value = classInstance.hashJSON[key];


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

    return classInstance;
}


var currEdit = toJSONCLass();
