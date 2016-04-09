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
    timer: null,
    turn: null,
    points: null,
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
    settings.turnDisplay.innerHTML = settings.turn;
    settings.pointsDisplay.innerHTML = settings.points;
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
  };
  
  return {
    /*  init
     *    function to initialize all members and bind
     *    ui actions
     *    called by global js initializer
     */
    init: function() {
      //for ease of actions
      //s = this.settings;
      //connect events
      bindUIActions();
      updateStatus();
    }
  };
})();
