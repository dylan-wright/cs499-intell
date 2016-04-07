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
        //Get add Event and Location working
        //Get the edit/delete buttons working  
        //Input validation?
        //figure out how to get values from the map for the location editor

    //Scenario properties
    this.name = 'NULL';
    this.turn_num = 20;
    this.point_num = 20;
    this.author = 'NULL';

    //Unique keys for each of the tabs to uniquely identify objects in the 
    //hashJSON structure
    this.charKey = 0;
    this.eventKey = 0;
    this.locKey = 0;

    //hashMap to contain input received from the user  
    this.hashJSON = [];


    /*
        add_char takes no arguments and is called when the add button is selected
        in the character tab.

        It receives the values stored in each fo the fields for the character
        tab, creates a formalized character object and stores the result in the
        object's hash map.
    */
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

        //EventListener used when a row in the character table is selected 
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

    
    /*
        add_event takes no arguments and is called when the add button is selected
        in the event tab.

        it reacts similarly to the add_character method, but with the unique
        fields associated with the event tab
    */ 
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


    /*
        add_loc takes no arguments and is called when the add button is selected
        in the locations tab.

        it reacts similarly to the add_loc method, but with the unique
        fields associated with the location tab
    */
    this.add_loc = function() {
        
        var locName = document.getElementById('locNameInput').value;
        var locCoordX = document.getElementById('locXinput').value;
        var locCoordY = document.getElementById('locYinput').value;

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
        nameCell = newLocElement.insertCell(0);
        xCell = newLocElement.insertCell(1);
        yCell = newLocElement.insertCell(2);
        
        nameCell.innerHTML = locName;
        xCell.innerHTML = locCoordX;
        yCell.innerHTML = locCoordY;
        
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

    /*
        submitJSON method - takes no arguments but is cast on the current object
        to stringify all elements being currently stored in hashJSON in order
        to create a JSON object. 

        Also, the fields associated with the field tab are stored in the object 
        as well. 
    */
    this.submitJSON = function(){
        
        //Assign the values in the title field 
        this.name = document.getElementById('titleBox').value;
        this.turn_num = document.getElementById('turnSpin').value;
        this.point_num = document.getElementById('pointSpin').value;
        //Getting the author field populated? Can be done later


        //Create a final array that will contain the JSON objects
        var finalarr = [];
        
        //Iterate through each object in the hashMap
        for(var key in this.hashJSON){
            
            //Push each element of the hashmap to the array to match fixture.JSON
            finalarr.push(this.hashJSON[key]);
        }

        //Generate the JSON file using stringify on the JSON array after the 
        //hashmap has been iterated through
        var fileUpload = JSON.stringify(finalarr);

        //Trying to send the current hashmap to the dump request webpage
        var xhttp = new XMLHttpRequest();
        xhttp.open('POST', "../dump_request/", false);
        xhttp.send(fileUpload);

        //Print out the results of the dump in the dump location at the bottom
        //of the webpage
        document.getElementById('dumpLoc').innerHTML = xhttp.responseText;
    }


}

//instantiate the toJSONClass to utilize the needed methods
var currEdit = new toJSONClass();

var prevChar;

/*
    Used to handle highlighting and row selection for the character table
*/
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

    //Highlight the currently selected item reseting the background of an object
    //that is no longer selected
    document.getElementById('charsTableBody').rows[totalRows-currRow].cells[0].style.backgroundColor='red';
    if (this.prevChar != null && this.prevChar != currRow) {
        document.getElementById('charsTableBody').rows[totalRows-this.prevChar].cells[0].style.backgroundColor='white';
    }
    this.prevChar = currRow;
}
