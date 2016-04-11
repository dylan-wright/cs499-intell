/*  INTELL The Craft of Intelligence
 *    https://github.com/dylan-wright/cs499-intell/
 *    https://intellproject.com
 *
 *    game/static/game/snippets.js
 *      js controller for front end
 *      Modules:
 *        Snippets
 */

/*  Snippets
 *    module for controlling behavior of loading and viewing snippets
 *    in snippet browser. Uses AJAX/JSON to communicate with the
 *    server and get objects
 *
 *    attributes
 *      settings
 *    methods
 *      init
 *      bindUIActions
 */

var Snippets = (function () {
  /*  settings
   *    module wide settings used to access various attributes in 
   *    module methods
   */
  var settings = {
    snippetTable: document.getElementById("snippetTable"),
  };

  /*  bindUIActions
   *    used to bind user actions to js functions
   *    mainly used to attah event listeners to buttons
   */
  function bindUIActions () {

  };

  /*  addSnippet
   *    add snippet to the table
   */
  function addSnippet (snippet) {
    var tbody = settings.snippetTable.children[0];
    var row = tbody.insertRow(0);
    var textCell = row.insertCell(0)
    textCell.innerHTML = snippet.fields.text;
  }

  /*  clearSnippets
   *    remove all rows from the snippet table
   */
  function clearSnippets () {
    var tbody = settings.snippetTable.tBodies[0];
    while (tbody.rows.length != 0) {
      tbody.deleteRow(0);
    }
  }

  /*  getSnippets
   *    send ajax request to server requesting JSON
   *    snippets
   */
  function getSnippets () {
    var csrftoken = Cookies.get("csrftoken")
    var xhttp = new XMLHttpRequest();
    //TODO: make async true
    xhttp.open("POST", "get_snippets/", false);
    xhttp.setRequestHeader("X-CSRFtoken", csrftoken);
    xhttp.send();
    response = xhttp.responseText;
    models = JSON.parse(response);
    var i;
    for (i = 0; i < models.length; i++) {
      addSnippet(models[i]);
    }
    return models;
  }

  /*  getCharacters
   *    send ajax request to server requesting JSON
   *    characters
   */
  function getCharacters () {
    var csrftoken = Cookies.get("csrftoken");
    var xhttp = new XMLHttpRequest();
    //TODO: make async true
    xhttp.open("GET", "get_characters/", false);
    xhttp.send();
    response = xhttp.responseText;
    characters = JSON.parse(response);
    return characters;
  }

  /*  getLocations
   *    send ajax request to server requesting JSON
   *    locations
   */
  function getLocations () {
      var xhttp = new XMLHttpRequest();
      //TODO: make async true
      xhttp.open("GET", "get_locations/", false);
      xhttp.send();
      response = xhttp.responseText;
      locations = JSON.parse(response);
      return locations;
  }

  return {
    /*  init
     *    function to initialize all members and bind
     *    ui actions
     *    called by global js initializer
     */
    init: function () {
      bindUIActions();
      clearSnippets();
      getSnippets();
    },

    characters: getCharacters(),
    locations: getLocations(),
    descriptions: getSnippets(),
  };
})();
