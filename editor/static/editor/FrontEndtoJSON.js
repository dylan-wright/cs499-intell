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
        //Storing title information as well
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
        var isKey = document.getElementById('keyCharBox').checked;
        var charNotes = document.getElementById('charComment').value;

        //Create a character object to match with the fixture.json format
        var charObj = {
            model:"editor.character",
            pk:this.charKey, 
            fields:{
                name: charName,
                key: isKey,
                notes: charNotes
            }
        };

        //Add the character object to the hashmap where the pk will be used
        //to determine this objects location
        this.hashJSON[this.charKey] = charObj;

        //Need to add the character object to the table as well...
        var newCharElement = document.getElementById("charsTableBody").insertRow(0);
        cell = newCharElement.insertCell(0);
        cell.innerHTML = charName;
        newCharElement.addEventListener("click", function(){selChar(charObj);});
        
        //incrememnt the key associated with character objects. 
        this.charKey++;


    }

    this.edit_char = function() {
        
        var charName = document.getElementById('charNameBox').value;
        var isKey = document.getElementById('keyCharBox').checked;
        var charNotes = document.getElementById('charComment').value;
        

//TODO: Need to change the charKey so that it matches with the desired char
//maybe using getElementById(table element).selected()["key"] or something

        //check that the entry already exists
        if(this.charKey in this.hashJSON){
                //Use key value to locate the object in the hashmap and then set  
                //it to a new object using the hashmap
                this.hashJSON[this.charKey] = {
                    model:"editor.character",
                    key:this.charKey,
                    fields:{
                        name: charName,
                        key: isKey,
                        notes: charNotes
                    }
                };

            //also need to edit that specified value in the table 
            var editCharElement = document.getElementById("charsTableBody").item(charKey);
            editCharElement.innerHTML = charName;
        }


    }

    this.del_char = function() {

    //TODO: Again, need to fix things here...
        //Check that the key is in hashJSON and delete it if so. 
        if(this.charKey in this.hashJSON){
            delete this.hashJSON[this.charKey];

            //delete the row from the table as well
            document.getElementById("charsTableBody").deleteRow(charKey);
        }
    }

    //Event related methods
    this.add_event = function() {
        
        var eventName = document.getElementById('eventNameBox').value;
        var isKey = document.getElementById('eventKeyBox').checked;
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
            pk:this.eventKey,
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
        this.hashJSON[this.eventKey] = eventObj;

         
        var newEventElement = document.getElementById("eventsTableBody").insertRow(0);
        newEventElement.innerHTML = eventName;
        
        this.eventKey++;
    }

    this.edit_event = function() {
        
        var eventName = document.getElementById('eventNameBox').value;
        var isKey = document.getElementById('eventKeyBox').checked;
        var isSecret = document.getElementById('eventSecretBox').value;
        
        if(this.eventKey in this.hashJSON){
            hashJSON[eventKey] = {
                model:"editor.event",
                pk:this.eventKey,
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

            var editEventElement = document.getElementById("eventsTableBody").item(eventKey);
            editEventElement.innerHTML = eventName;
        
        }
    }

    this.del_event = function() {
        
        if(this.eventKey in this.hashJSON){
            delete this.hashJSON[this.eventKey];
            //delete the table entry
            document.getElementById("eventsTableBody").deleteRow(eventKey);

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
            pk:this.locKey,
            fields:{
                name: locName,
                x: locCoordX,
                y: locCoordY
            }
        };

        this.hashJSON[this.locKey] = locObj;

        var newLocElement = document.getElementById("locsTableBody").insertRow(0);
        newLocElement.innerHTML = locName;
        
        this.locKey++;

    }

    this.edit_loc = function() {
       
        var locName = "test";
        var locCoordX = 0;
        var locCoordY = 0;
        
        //check that the entry already exists
        if(this.locKey in this.hashJSON){
                this.hashJSON[locKey] = {
                    model:"editor.location",
                    pk:locKey,
                    fields:{
                        name: locName,
                        x: locCoordX,
                        y: locCoordY
                    }
                };

            var editLocElement = document.getElementById("locsTableBody").item(locKey);
            editLocElement.innerHTML = locName;

        }

    }

    this.del_loc = function() {
        
        if(locKey in hashJSON){
            delete hashJSON[locKey];
            document.getElementById("locsTableBody").deleteRow(locKey);
        }
    }



    //Serialize the fields, place into an array
    //Serialize the object, place into an arry
    


    //Final method to submit the JSON currently stored in hashJSON
    this.submitJSON = function(){
        
        //Create a final array that will contain the JSON objects
        var finalarr = [];
        
        //Iterate through each object in the hashMap
        for(var key in this.hashJSON){
            
            var JSONarr = [];
            
            //Get the key values of the hashmap
            var value = this.hashJSON[key];

            JSONarr.push(value.model);
            JSONarr.push(value.pk);
            JSONarr.push(value.fields);
            //JSONarr.push(fieldarr);
            finalarr.push(JSONarr);
        }

        //Generate the JSON file using stringify on the JSON array
        //after the hashmap has been iterated through
        //var fileUpload = JSON.stringify(JSONarr);
        var fileUpload = JSON.stringify(finalarr);
        console.log(fileUpload);


        //Trying to send the current hashmap to the dump request webpage
        var xhttp = new XMLHttpRequest();
        xhttp.open('POST', "../dump_request/", false);
        xhttp.send(fileUpload);

        //document.getElementById('charsIntrBody').innerHTML = xhttp.responseText;
        //console.log(xhttp.responseText);
        document.getElementById('dumpLoc').innerHTML = xhttp.responseText;
    }


}
var currEdit = new toJSONClass();

var prevChar;
//Function used to select an element based on the row selected 
function selChar(charObj) {

    //Store current/total rows in order to determine which row is hilighted
    console.log(charObj.pk);
    var currRow = charObj.pk;
    var totalRows = document.getElementById('charsTableBody').rows.length -1;
    

    //Set fields to those associated with the selected object
    document.getElementById('charNameBox').value = charObj.fields.name;
    document.getElementById('keyCharBox').checked = charObj.fields.key;
    document.getElementById('charComment').value = charObj.fields.notes;
    
    //Enable the edit/delete buttons and highlight the selected row
    document.getElementById('charEditBtn').disabled = false;
    document.getElementById('charDelBtn').disabled = false;

    //Highlight the currently selected item
    document.getElementById('charsTableBody').rows[totalRows-currRow].cells[0].style.backgroundColor='red';
    if (this.prevChar != null && this.prevChar != currRow) {
        document.getElementById('charsTableBody').rows[totalRows-this.prevChar].cells[0].style.backgroundColor='white';
    }
    this.prevChar = currRow;
}
