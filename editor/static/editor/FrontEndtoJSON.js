/*  INTELL The Craft of Intelligence
 *    https://github.com/dylan-wright/cs499-intell/
 *    https://intellproject.com/
 *
 *    editor/static/editor/FrontEndtoJSON.js
 *      js controller for front end aspect of the editor
 *      Modules:
 *        toJSONClass
 */

/*  toJSONClass:
 *
 *  The toJSONClass() will be used to instantiate an object in the scenario editor
 *  HTML given values to replace the name, turn, point and author. After it is 
 *  instantiated, it's method will be called whenever an onclick even occurs 
 *  to one of it's related buttons. After this occurs, the hashmap hashJSON
 *  will be updated with the new objects. Once the submit method is used, the 
 *  JSON file will be formed using the hashmap and then sent to the back end.
 *
 *    attributes
 *      name -- Scenario title
 *      turn_num - number of turns in a scenario
 *      point_num - number of INTELL points provided initially
 *      author - author name
 *
 *      hashKey - used to identify where an object is located in hashJSON
 *      charKey - Keeps track of char objects
 *      eventKey - Keeps track of event objects   
 *      locKey - Keeps track of location objects   
 *      descKey - Keeps track of char description objects   
 *      descbyKey - Keeps track of describedby (relationship) objects   
 *      happatKey - Keeps track of happenedat (relationship)  objects   
 *      involvKey - Keeps track of involved (relationship)  objects    
 *
 *      eventTags[] - collection of event tags stored in the event object
 *      charHash[] - arrays for tab keys 
 *      eventHash[] - ""
 *      hashJSON[] - Primary hashMap that is used to contain all of the objects
 *          created by the user and send, so that they can be sent to the back
 *          end
 *
 *    methods
 *      add_char, edit_char, del_char - methods used to interract with char tab
 *      add_event, edit_event, del_event - methods used to interract with the 
 *          top half of the edit tab
 *      add_eventTag, edit_eventTag, del_eventTag - methods used to interract 
 *          with the bottom half of the event tab. 
 #      add_loc, edit_loc, del_loc -  methods used to interract with the location
 *          tab
 #      
 *      submitJSON - Method that takes the hashJSON method, generates a JSON
 *          message and then sends the results to the back end database
 *
 #      populateTagTargets - Small helper method that populates the "Target" 
 *          field based on the previously created objects and the Tag Type
 *      selChar - event listener that would change tab fields based on the 
 *          char element selected on the character tag
 *      selLoc - similar to selChar, but for location tab instead
 *      selEvent, selTag - similar to the previous tabs but are used to interract
 *          with both tables in the event tab.
 */

/* In progress:
 *
 *  Currently the functionality for the edit/delete methods are still in 
 *  progress. 
 *
 *  Also, there are still some issues with the saveJSON method that are currently
 *  being worked out.
 *
 *  For the record, most functions other than the add methods are still subject
 *  change and will likely to do so prior to the completion of this project
 */


/*

    toJSONClass() - Class that is used to instantiate and keep track of all of 
    the objects created by the user. 

*/

function toJSONClass() {


    //TODO:
        //Get add Event working
        //Get the edit/delete buttons working  
        //Input validation?
        //figure out how to get values from the map for the location editor
        //Use onreadystatechange

    //Scenario properties
    this.name = 'NULL';
    this.turn_num = 20;
    this.point_num = 20;
    this.author = 'NULL';

    //Unique keys for each of the tabs to uniquely identify objects in the 
    //hashJSON structure
    this.hashKey = 0;
    this.charKey = 0;
    this.eventKey = 0;
    this.locKey = 0;

    //need event related keys as well...
    this.descKey = 0;
    this.descbyKey = 0;
    this.happatKey = 0;
    this.involvKey = 0;
    
    //Collection of event tags that will be stored in an event object
    this.eventTags = [];

	//key hashing arrays for the tab keys so that they can be used in the hashJSON structure
	this.charHash = [];
	this.eventHash = [];
	this.locHash = [];
	
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
        this.hashJSON[this.hashKey] = charObj;

		//put the value into the hash array for later use
		this.charHash[this.charKey] = this.hashKey;
		
        //Need to add the character object to the table as well...
        var newCharElement = document.getElementById("charsTableBody").insertRow(0);
        cell = newCharElement.insertCell(0);
        cell.innerHTML = charName;

        //EventListener used when a row in the character table is selected 
        newCharElement.addEventListener("click", function(){selChar(charObj);});
        		
        //incrememnt the keys associated with character object and hash location. 
        this.hashKey++;
        this.charKey++;



    }

    this.edit_char = function() {
        
        var charName = document.getElementById('charNameBox').value;
        var isKey = document.getElementById('keyCharBox').checked;
        var charNotes = document.getElementById('charComment').value;
        

//TODO: Need to change the charKey so that it matches with the desired char
//maybe using getElementById(table element).selected()["key"] or something

        //check that the entry already exists
        if(this.hashKey in this.hashJSON){
                //Use key value to locate the object in the hashmap and then set  
                //it to a new object using the hashmap
                this.hashJSON[this.hashKey] = {
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
        if(this.hashKey in this.hashJSON){
            delete this.hashJSON[this.hashKey];

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
       
        //Get values stored in the current fields 
        var eventName = document.getElementById('eventNameBox').value;
        var isKey = document.getElementById('eventKeyBox').checked;
        var isSecret = document.getElementById('eventSecretBox').checked;
        var eventSnip = document.getElementById('snippet').value;
        var secretSnip = document.getElementById('secretSnippet').value;
        var tagTurn = document.getElementById('turnTagSel').value;
	
        //TODO: add some input validation based event tags 


        //Create an event object to match with the fixture.json format
        var eventObj = {
            model:"editor.event",
            pk:this.eventKey,

            fields:{
                name: eventName,
                turn: tagTurn
            },

            description:{
                descmodel:'editor.description',
                descpk:this.descKey,
                key: isKey,
                secret: isSecret,
                snippet: eventSnip,
                secretSnippet: secretSnip,
                describedby:{
                    descbymodel:'editor.describedby',
                    descbypk:this.descbyKey
                }
            },

            tags:this.eventTags


        };

        //Add the character object to the hashmap where the pk will be used
        //to determine this objects location
        this.hashJSON[this.hashKey] = eventObj;
		
		//put the value into the hash array for later use
		this.eventHash[this.eventKey] = this.hashKey;

        //Update the events table with the new event object 
        var newEventElement = document.getElementById("eventsTableBody").insertRow(0);
        eventNameCell = newEventElement.insertCell(0);
        eventNameCell.innerHTML = eventObj.fields.name;

        //EventListener used when a row in the events table is selected 
        newEventElement.addEventListener("click", function(){selEvent(eventObj);});
		
        this.eventKey++;
        this.hashKey++;
    }

    this.edit_event = function() {
        
        var eventName = document.getElementById('eventNameBox').value;
        var isKey = document.getElementById('eventKeyBox').checked;
        var isSecret = document.getElementById('eventSecretBox').value;
        
        

        if(this.hashKey in this.hashJSON){
            hashJSON[this.hashKey] = {
                model:"editor.event",
                pk:this.eventKey,
                fields:{
                    name: eventName,
                    key: isKey,
                    secret: isSecret
                }
            };

            var editEventElement = document.getElementById("eventsTableBody").item(eventKey);
            editEventElement.innerHTML = eventName;
        
        }
    }

    this.del_event = function() {
        
        if(this.hashKey in this.hashJSON){
            delete this.hashJSON[this.hashKey];
            //delete the table entry
            document.getElementById("eventsTableBody").deleteRow(eventKey);

        }
    }

    this.add_eventTag = function(){
        
        var tagTypeinput = document.getElementById('tagTypeSel').value;
        var currModel = '';
        var currTagKey = 0;
        var currTargetKey = 0;
        var selTarget = document.getElementById('targetSel').value;

		//TODO: FIX THIS LATER. Either by changing the hashMap or by provided more info
		//when table is populated.

       //Could use a for loop that simply looks through every one of the objects 		
       //and then breaks when it finds it		
        for(var key in this.hashJSON){		
             		
             //go through each json object until the desired target is found		
             if(this.hashJSON[key].fields.name != null){		
                 		
                 if(selTarget == this.hashJSON[key].fields.name)		
 		
                     //bad programmer		
                     //once the target is found assign it to currTargetKey		
                     currTargetKey = selTarget;		
                     break;		
             }		
 		
         }		
 		
 		
 		
        //might be able to store the target.pk else somehow. 


/*
        //The current target key can be found using the hashMap
        var key = 0;
        while(selTarget != this.hashJSON[key].fields.name)
        {
            key++;
        }
        //If the selected target is found in hashJSON then you have the key
        //info needed for the target pk
        currTargetKey = selTarget;
*/

        //check if user type is character or location and match values based on result
        
        //If selected index=0, then character was selected and involved tag is used
        if(tagType.selectedIndex == 0){
            currModel = 'editor.involved';
            currTagKey= this.involvKey;
            this.invlvKey++;
            //this.hashKey++;
        }

        else{
            currModel = 'editor.happenedat';
            currTagKey = this.happatKey;
            this.happatKey++;
            //this.hashKey++;
        }       

        //The event tag object 
        var eventTagObj = {

            tagmodel: currModel,
            tagpk: currTagKey,
            targetpk: currTargetKey
        };

        //Update the table with the new tag element 
        var newEventTagElement = document.getElementById("eventTagTable").insertRow(0);
        TagNum = newEventTagElement.insertCell(0);
        TargetNum = newEventTagElement.insertCell(1);
        TagNum.innerHTML = eventTagObj.tagpk;
        TargetNum.innerHTML = eventTagObj.targetpk;

        this.eventTags.push(eventTagObj);

        
    }

	//IN PROGRESS
    this.edit_eventTag = function(){

    }

	//IN PROGRESS
    this.del_eventTag = function(){

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

        this.hashJSON[this.hashKey] = locObj;
		
		//put the value into the hash array for later use
		this.locHash[this.locKey] = this.hashKey;

        var newLocElement = document.getElementById("locsTableBody").insertRow(0);
        nameCell = newLocElement.insertCell(0);
        xCell = newLocElement.insertCell(1);
        yCell = newLocElement.insertCell(2);
		
        //EventListener used when a row in the locations table is selected 
        newLocElement.addEventListener("click", function(){selLoc(locObj);});
        
        nameCell.innerHTML = locName;
        xCell.innerHTML = locCoordX;
        yCell.innerHTML = locCoordY;
        
        this.locKey++;
        this.hashKey++;

    }

    this.edit_loc = function() {
       
        var locName = "test";
        var locCoordX = 0;
        var locCoordY = 0;
        
        //check that the entry already exists
        if(this.hashKey in this.hashJSON){
                this.hashJSON[hashKey] = {
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
        
        if(this.locKey in this.hashJSON){
            delete this.hashJSON[this.hashKey];
            document.getElementById("locsTableBody").deleteRow(this.locKey);
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

        scenariomodel = {
            "model": "editor.scenario",
            "pk": null,
            "fields": {
                "name": this.name,
                "turn_num": this.turn_num,
                "point_num": this.point_num
            }
        };
        finalarr.push(scenariomodel);

        //Iterate through each object in the hashMap
        for(var key in this.hashJSON){
            
            var currModel = this.hashJSON[key].model;

            //if element is a character/location then just push as is
            if(currModel == "editor.character" || currModel == "editor.location"){ 
                finalarr.push(this.hashJSON[key]);
            }

            //Else, it's some other event object 
            else{

                var currJSONobj = this.hashJSON[key];
                //first create the event object
                //Matching all fields as specified in fixture.json
                JSONevent = {
                    "model": currJSONobj.model,
                    "pk": currJSONobj.pk,
                    "fields": {
                        "turn": currJSONobj.fields.turn
                    }
                };
                finalarr.push(JSONevent);

                //then create the description object 
                JSONdesc = {
                    "model": currJSONobj.description.descmodel,
                    "pk": currJSONobj.description.descpk,
                    "fields": {
                        "text": currJSONobj.description.snippet,
                        "hidden": currJSONobj.description.secret
                    }
                };
                finalarr.push(JSONdesc);

                //then create the described by objects
                JSONdescby = {
                    "model": currJSONobj.description.describedby.descbymodel,
                    "pk": currJSONobj.description.describedby.descbypk,
                    "fields": {
                        "event_id": currJSONobj.pk,
                        "description_id": currJSONobj.description.pk
                    }
                };
                finalarr.push(JSONdescby);

                //Iterate through the tags and create those objects
                var JSONtag = {};
                for(var element in currJSONobj.tags){

                    //The tags can only be involved or happened at, so match those
                    //formats based on the model
                    if(currJSONobj.tags[element].tagmodel == 'editor.involved'){

                        JSONtag = {
                            "model": currJSONobj.tags[element].tagmodel,
                            "pk": currJSONobj.tags[element].tagpk,
                            "fields": {
                                "event_id": currJSONobj.pk,
                                "character_id": currJSONobj.tags[element].targetpk
                            }
                        };

                    }

                    else{

                         JSONtag = {
                            "model": currJSONobj.tags[element].tagmodel,
                            "pk": currJSONobj.tags[element].tagpk,
                            "fields": {
                                "event_id": currJSONobj.pk,
                                "location_id": currJSONobj.tags[element].targetpk
                            }
                        };                       
                    }

                    finalarr.push(JSONtag);
                }

            }
        }

        //Generate the JSON file using stringify on the JSON array after the 
        //hashmap has been iterated through
        var fileUpload = JSON.stringify(finalarr);

        //Trying to send the current hashmap to the dump request webpage
        var xhttp = new XMLHttpRequest();
        //xhttp.open('POST', "../accept_ajax_scenario/", false);
        xhttp.open('POST', "../dump_request/", false);
        xhttp.send(fileUpload);

        //Print out the results of the dump in the dump location at the bottom
        //of the webpage
        document.getElementById('dumpLoc').innerHTML = xhttp.responseText;
    }


    //method to populate the target selection when character/location is slected
    this.populateTagTargets = function(){
        var loopKey = 0;
        //store the element for the type and target selectors
        var targetSel = document.getElementById('targetSel');
        var tagType = document.getElementById('tagTypeSel');
    
        //clear the selector options list
        targetSel.innerHTML = '';

        //loop through each element in hashJSON and find the
		//characters or locations depending on which is selected in tagType
        for(var key in this.hashJSON)
        {
			if(this.hashJSON[key].model=="editor.character" && tagType.selectedIndex == 0)
			{
				var tarOption = document.createElement("option");
				tarOption.text = this.hashJSON[key].fields.name;
				targetSel.add(tarOption);
			}
			else if (this.hashJSON[key].model=="editor.location" && tagType.selectedIndex == 1)
			{
				var tarOption = document.createElement("option");
				tarOption.text = this.hashJSON[key].fields.name;
				targetSel.add(tarOption);
			}
        }
    }   


}

//instantiate the toJSONClass to utilize the needed methods
var currEdit = new toJSONClass();

var prevChar;
var prevLoc;
var prevEvent;
var prevTag;

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

/*
    Used to handle highlighting and row selection for the location table
*/
function selLoc(locObj) {

    //Store current/total rows in order to determine which row is hilighted
    console.log(locObj.pk);
    var currRow = locObj.pk;
    var totalRows = document.getElementById('locsTableBody').rows.length -1;
    

    //Set fields to those associated with the selected object
    document.getElementById('locNameInput').value = locObj.fields.name;
    document.getElementById('locXinput').value = locObj.fields.x;
    document.getElementById('locYinput').value = locObj.fields.y;
    
    //Enable the edit/delete buttons and highlight the selected row
    document.getElementById('locEditBtn').disabled = false;
    document.getElementById('locDelBtn').disabled = false;

    //Highlight the currently selected item reseting the background of an object
    //that is no longer selected
    document.getElementById('locsTableBody').rows[totalRows-currRow].cells[0].style.backgroundColor='red';
	document.getElementById('locsTableBody').rows[totalRows-currRow].cells[1].style.backgroundColor='red';
	document.getElementById('locsTableBody').rows[totalRows-currRow].cells[2].style.backgroundColor='red';
    if (this.prevLoc != null && this.prevLoc != currRow) {
        document.getElementById('locsTableBody').rows[totalRows-this.prevLoc].cells[0].style.backgroundColor='white';
		document.getElementById('locsTableBody').rows[totalRows-this.prevLoc].cells[1].style.backgroundColor='white';
		document.getElementById('locsTableBody').rows[totalRows-this.prevLoc].cells[2].style.backgroundColor='white';
    }
    this.prevLoc = currRow;
}

/*
    Used to handle highlighting and row selection for the event table
*/
function selEvent(eventObj) {

    //Store current/total rows in order to determine which row is hilighted
    console.log(eventObj.pk);
    var currRow = eventObj.pk;
    var totalRows = document.getElementById('eventsTableBody').rows.length -1;
    
	var eventTags = eventObj.fields.tags;
	
    //Set fields to those associated with the selected object	
    document.getElementById('eventNameBox').value = eventObj.fields.name;
    document.getElementById('eventKeyBox').checked = eventObj.description.key;
    document.getElementById('eventSecretBox').checked = eventObj.description.secret;
	document.getElementById('snippet').value = eventObj.description.snippet;
	document.getElementById('secretSnippet').value = eventObj.description.secretSnippet;
	document.getElementById('turnTagSel').value = eventObj.fields.turn;
	
	//had to use jquery here to get the bootstrap object instead of the html
	//recolapse/reshow the secret snippet text area if the secret box is checked
	if(!eventObj.description.secret){
		$('#secretCollapse').collapse('hide')
	}
	
	else{
		$('#secretCollapse').collapse('show')
	}
    
    //Enable the edit/delete buttons and highlight the selected row
    document.getElementById('eventEditBtn').disabled = false;
    document.getElementById('eventDelBtn').disabled = false;

    //Highlight the currently selected item reseting the background of an object
    //that is no longer selected
    document.getElementById('eventsTableBody').rows[totalRows-currRow].cells[0].style.backgroundColor='red';
    if (this.prevEvent != null && this.prevEvent != currRow) {
        document.getElementById('eventsTableBody').rows[totalRows-this.prevEvent].cells[0].style.backgroundColor='white';
    }
    this.prevEvent = currRow;
	
	//load the selected eventObj tags into the global tags array
	this.currEdit.eventTags = eventOgj.tags;
	
	document.getElementById('eventsTagBody').innerHTML = '';
	
	//load the tags for the event into the tags table
	for(tag in eventObj.tags){
		//Update the event tags table with the event tags objects
        var newEventElement = document.getElementById("eventsTagBody").insertRow(0);
        tagTypeCell = newEventElement.insertCell(0);
		tagTargetCell = newEventElement.insertCell(1);
        if(tag.tagmodel == "editor.involved"){
			tagTypeCell.innerHTML = "Character";
			tagTargetCell.innerHTML = this.currEdit.hashJSON[this.currEdit.charHash[targetpk]].fields.name;
		}
		else if(tag.tagmodel == "editor.happenedat"){
			tagTypeCell.innerHTML = "Location";
			tagTargetCell.innerHTML = this.currEdit.hashJSON[this.currEdit.locHash[targetpk]].fields.name;
		}
	}
	
}

/*
    Used to handle highlighting and row selection for the event tag table
*/

function selTag(tagObj) {

    //Store current/total rows in order to determine which row is hilighted
    console.log(locObj.pk);
    var currRow = locObj.pk;
    var totalRows = document.getElementById('locsTableBody').rows.length -1;
    

    //Set fields to those associated with the selected object
    document.getElementById('locNameInput').value = locObj.fields.name;
    document.getElementById('locXinput').value = locObj.fields.x;
    document.getElementById('locYinput').value = locObj.fields.y;
    
    //Enable the edit/delete buttons and highlight the selected row
    document.getElementById('locEditBtn').disabled = false;
    document.getElementById('locDelBtn').disabled = false;

    //Highlight the currently selected item reseting the background of an object
    //that is no longer selected
    document.getElementById('locsTableBody').rows[totalRows-currRow].cells[0].style.backgroundColor='red';
    if (this.prevLoc != null && this.prevLoc != currRow) {
        document.getElementById('locsTableBody').rows[totalRows-this.prevLoc].cells[0].style.backgroundColor='white';
    }
    this.prevLoc = currRow;
}

