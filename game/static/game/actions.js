/*  INTELL The Craft of Intelligence
 *    https://github.com/dylan-wright/cs499-intell/
 *    https://intellproject.com/
 *
 *    game/static/game/actions.js
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
var Actions = (function () {
  /*  settings
   *    module wide settings used to access various attributes
   *    in module methods
   */
  var settings = {
    buttons: {
      tailButton: document.getElementById("tailBtn"),
      investigateButton: document.getElementById("investigateBtn"),
      checkButton: document.getElementById("checkBtn"),
      misinfButton: document.getElementById("misInfoBtn"),
      recruitButton: document.getElementById("recruitBtn"),
      apprehendButton: document.getElementById("apprehendBtn"),
      researchButton: document.getElementById("researchBtn"),
      terminateButton: document.getElementById("terminateBtn"),

      confirmTail: document.getElementById("confirmTail"),
      confirmInvestigate: document.getElementById("confirmInvestigate"),
      confirmCheck: document.getElementById("confirmInvestigate"),
      confirmMisinf: document.getElementById("confirmMisinf"),
      confirmRecruit: document.getElementById("confirmRecruit"),
      confirmApprehend: document.getElementById("confirmApprehend"),
      confirmResearch: document.getElementById("confirmResearch"),
      confirmTerminate: document.getElementById("confirmTerminate"),
    },
    activeButton: document.getElementById("researchBtn"),
    agentSelect: document.getElementById("agentSel"),
  };

  /*  bindUIActions
   *    used to bind user actions to js functions
   *    mainly used to attach event listeners to buttons
   */
  function bindUIActions () {
    //buttons for opening a modal
    settings.buttons.tailButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.tailButton);
      tail();
    });
    settings.buttons.investigateButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.investigateButton);
      investigate();
    });
    settings.buttons.checkButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.checkButton);
      check();
    });
    settings.buttons.misinfButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.misinfButton);
      misinf();
    });
    settings.buttons.recruitButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.recruitButton);
      recruit();
    });
    settings.buttons.apprehendButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.apprehendButton);
      apprehend();
    });
    settings.buttons.researchButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.researchButton);
      research();
    });
    settings.buttons.terminateButton.addEventListener("click", function() {
      setActiveButton(settings.buttons.terminateButton);
      terminate();
    });

    //buttons in a modal
    settings.buttons.confirmTail.addEventListener("click", function() {
      sendAction()
    });
    settings.buttons.confirmInvestigate.addEventListener("click", function() {
      sendAction()
    });
    settings.buttons.confirmCheck.addEventListener("click", function() {
      sendAction()
    });
    settings.buttons.confirmMisinf.addEventListener("click", function() {
      sendAction()
    });
    settings.buttons.confirmRecruit.addEventListener("click", function() {
      sendAction()
    });
    settings.buttons.confirmApprehend.addEventListener("click", function() {
      sendAction()
    });
    settings.buttons.confirmResearch.addEventListener("click", function() {
      sendAction()
    });
    settings.buttons.confirmTerminate.addEventListener("click", function() {
      sendAction()
    });
  };

  /*  setActiveButton
   *    used to toggle button when clicked
   *    called as part of each button's event listener
   *    also replaces the active button in the settings
   */
  function setActiveButton (clickedButton) {
    //replace .active with "" in prev clicked button
    settings.activeButton.className = 
        settings.activeButton.className.replace(/(?:^|\s)active(?!\S)/g, '');

    //add .active to class name of clicked button and make active
    clickedButton.className += " active";
    settings.activeButton = clickedButton;
  };

  /*  actionJSON
   *    returns the JSON for the current action
   */
  function actionJSON () {
    //agent is the agent selected in agentSel
    //the action name is the button id minus "btn"
    retObj = {
      "agent": settings.agentSelect.value,
      "action": settings.activeButton.id.slice(0,-3),
    };
    return JSON.stringify(retObj);
  };

  /*  sendAction
   *    send an AJAX request to /game/play/pk/submit_action/
   *    include return value of actionJSON (json rep of action
   */
  function sendAction () {
    var csrftoken = Cookies.get("csrftoken");
    var xhttp = new XMLHttpRequest();
    //TODO: make async true (add handler)
    xhttp.open("POST", "submit_action/", false);
    xhttp.setRequestHeader("X-CSRFtoken", csrftoken);
    xhttp.send(actionJSON());
    var response = xhttp.responseText;
  };

  /*  button click handlers
   *    all open a modal
   */
  function tail () {
    $("#tailModal").modal();
  };
  function investigate () {
    $("#investigateModal").modal();
  };
  function check () {
    $("#checkModal").modal();
  };
  function misinf () {
    $("#misinfModal").modal();
  };
  function recruit () {
    $("#recruitModal").modal();
  };
  function apprehend () {
    $("#apprehendModal").modal();
  };
  function research () {
    $("#researchModal").modal();
  };
  function terminate () {
    $("#terminateModal").modal();
  };
  
  return {
    /*  init
     *    function to initialize all members and bind
     *    ui actions
     *    called by global js initializer
     */
    init: function () {
      //connect buttons to events
      bindUIActions();
    }
  };
})();
