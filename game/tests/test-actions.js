casper.test.comment('actions.js test');
var helper = require('./djangocasper.js');
helper.scenario('/game/play/1/',
  function () {
    //test modal opens and can be opened and closed
    tailModalGood = casper.evaluate(function(){
      $("#tailBtn").click();
      var modalVis = $("#tailModal").is(":visible");
      return modalVis;
    });
  },
  function () {
  }
);
helper.run()
