/*  INTELL The Craft of Intelligence
 *    https://github.com/dylan-wright/cs499-intell/
 *    https://intellproject.com
 *
 *  game/static/game/status.js
 *    js controller for front end
 *      Modules:
 *        Status
 */

/*  Status
 *    module for conrolling the behavior of various game status
 *    fields. 
 *
 *    attributes
 *      settings
 *    methods
 *      init
 *      bindUIActions
 */
var Status = (function () {
  /*  settings
   *    module wide settings used to access various attributes 
   *    in module methods
   */
  var settings = {
    timerDisplay: document.getElementById("timerDisplay"),
    turnDisplay: document.getElementById("turnDisplay"),
    pointsDisplay: document.getElementById("pointsDisplay"),
    messagesDisplay: document.getElementById("messagesDisplay"),
    timer: null,
    turn: null,
    points: null,
    messages: null,
  };

  
  /*  bindUIActions
   *    used to bind user actions to js functions
   *    mainly used to attach event listeners to buttons
   */
  function bindUIActions () {

  };

  /*  updateStatus
   *    update page elements
   */
  function updateStatus () {
    getStatus();
    settings.turnDisplay.innerHTML = settings.turn;
    settings.pointsDisplay.innerHTML = settings.points;
    settings.timerDisplay.timer = settings.timer;

    //populate the message table
    while (settings.messagesDisplay.children[1].rows.length != 0) {
      settings.messagesDisplay.children[1].deleteRow(0);
    }
    var i;
    var td, tr;
    for (i = 0; i < settings.messages.length; i+=1) {
      tr = settings.messagesDisplay.children[1].insertRow(0);
      td = tr.insertCell(0);
      td.innerHTML = settings.messages[i].fields.text;
      td = tr.insertCell(0);
      td.innerHTML = settings.messages[i].fields.turn;
    }
  };

  /*  getStatus
   *    query the server for a new next turn time
   *    turn and points
   */
  function getStatus () {
    var xhttp = new XMLHttpRequest();
    //TODO: make async true
    xhttp.open("GET", "get_status/", false);
    xhttp.send();
    var statusJSON = JSON.parse(xhttp.responseText);
    settings.turn = statusJSON.turn;
    settings.points = statusJSON.points;
    settings.timer = statusJSON.timer;
    settings.messages = JSON.parse(statusJSON.messages);
  };
  
  return {
    /*  init
     *    function to initialize all members and bind
     *    ui actions
     *    called by global js initializer
     */
    init: function () {
      //connect events
      bindUIActions();
      updateStatus();
    }
  };
})();
