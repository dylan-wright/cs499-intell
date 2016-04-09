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

  return {
    /*  init
     *    function to initialize all members and bind
     *    ui actions
     *    called by global js initializer
     */
    init: function () {
      bindUIActions();
    }
  };
})();
