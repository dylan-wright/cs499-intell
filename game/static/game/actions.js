/*  INTELL The Craft of Intelligence
 *    https://github.com/dylan-wright/cs499-intell/
 *    https://intellproject.com/
 *
 *    static/game/actions.js
 *      js controller for front end
 *      Modules:
 *        Actions
 */

/*  Actions
 *    module for controlling behavior of clicking various action buttons
 *    should ensure only one button is active at a time and present
 *    user with options based on clicked button. Then confirm to send
 *    AJAX/JSON request to server. Action will be proccessed when game turn
 *    is over. Results will be sent back to user with new snippets when
 *    requested/ready
 *
 *    attributes
 *      settings
 *    methods
 *      init
 *      bindUIActions
 *      setActiveButton
 *      actionJSON
 *      sendAction
 *    action modal methods
 *      tail
 *      investigate
 *      check
 *      misinf
 *      recruit
 *      apprehend
 *      research
 *      terminate
 */
var s;
Actions = {
  /*  settings
   *    module wide settings used to access various attributes
   *    in module methods
   */
  settings: {
    buttons: {
      tailButton: document.getElementById("tailBtn"),
      investigateButton: document.getElementById("investigateBtn"),
      checkButton: document.getElementById("checkBtn"),
      misinfButton: document.getElementById("misInfoBtn"),
      recruitButton: document.getElementById("recruitBtn"),
      apprehendButton: document.getElementById("apprehendBtn"),
      researchButton: document.getElementById("researchBtn"),
      terminateButton: document.getElementById("terminateBtn"),
    },
    activeButton: document.getElementById("researchBtn")
  },

  /*  init
   *    function to initialize all members and bind
   *    ui actions
   *    called by global js initializer
   */
  init: function() {
    s = this.settings;
    this.bindUIActions();
  },

  /*  bindUIActions
   *    used to bind user actions to js functions
   *    mainly used to attach event listeners to buttons
   */
  bindUIActions: function() {
    s.buttons.tailButton.addEventListener("click", function(){
      Actions.setActiveButton(s.buttons.tailButton);
      Actions.tail();
    });
    s.buttons.investigateButton.addEventListener("click", function(){
      Actions.setActiveButton(s.buttons.investigateButton);
      Actions.investigate();
    });
    s.buttons.checkButton.addEventListener("click", function(){
      Actions.setActiveButton(s.buttons.checkButton);
      Actions.check();
    });
    s.buttons.misinfButton.addEventListener("click", function(){
      Actions.setActiveButton(s.buttons.misinfButton);
      Actions.misinf();
    });
    s.buttons.recruitButton.addEventListener("click", function(){
      Actions.setActiveButton(s.buttons.recruitButton);
      Actions.recruit();
    });
    s.buttons.apprehendButton.addEventListener("click", function(){
      Actions.setActiveButton(s.buttons.apprehendButton);
      Actions.apprehend();
    });
    s.buttons.researchButton.addEventListener("click", function(){
      Actions.setActiveButton(s.buttons.researchButton);
      Actions.research();
    });
    s.buttons.terminateButton.addEventListener("click", function(){
      Actions.setActiveButton(s.buttons.terminateButton);
      Actions.terminate();
    });
  },

  /*  setActiveButton
   *    used to toggle button when clicked
   *    called as part of each button's event listener
   *    also replaces the active button in the settings
   */
  setActiveButton: function(clickedButton) {
    //replace .active with "" in prev clicked button
    s.activeButton.className = 
        s.activeButton.className.replace(/(?:^|\s)active(?!\S)/g, '');

    //add .active to class name of clicked button and make active
    clickedButton.className += " active";
    s.activeButton = clickedButton;
  },

  /*  actionJSON
   *    returns the JSON for the current action
   */
  actionJSON: function(){
    //the action name is the button id minus "btn"
    retObj = {"action": s.buttons.activeButton.slice(0,-3)};
    return JSON.stringify(retObj);
  },

  /*  sendAction
   *    send an AJAX request to /game/play/pk/submit_action/
   *    include return value of actionJSON (json rep of action
   */
  sendAction: function() {
    var csrftoken = Cookies.get("csrftoken");
    var xhttp = new XMLHttpRequest();
    //TODO: make async true (add handler)
    xhttp.open("POST", "submit_action/", false);
    xhttp.setRequestHeader("X-CSRFtoken", csrftoken);
    xhttp.send(this.actionJSON());
    response = xhttp.responseText;
  },

  /*  button click handlers
   *    all open a modal
   */
  tail: function(){
    $("#tailModal").modal();
  },
  investigate: function(){
    $("#investigateModal").modal();
  },
  check: function(){
    $("#checkModal").modal();
  },
  misinf: function() {
    $("#misinfModal").modal();
  },
  recruit: function() {
    $("#recruitModal").modal();
  },
  apprehend: function(){
    $("#apprehendModal").modal();
  },
  research: function(){
    $("#researchModal").modal();
  },
  terminate: function(){
    $("#terminateModal").modal();
  }
};

//TODO: move to global js file?
(function() {
  Actions.init();
})();
