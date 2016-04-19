var Waiting = (function () {
  var settings = {
    games: [],
    timers: [],
    buttons: {
      joinButton: document.getElementById("joinBtn"),
      playButton: document.getElementById("playBtn"),
      createButton: document.getElementById("createBtn"),
    },
    createModalBody: document.getElementById("createModalBody"),
  }

  function bindUIActions () {
    settings.buttons.joinButton.addEventListener("click", function () {

    });
    settings.buttons.playButton.addEventListener("click", function () {

    });
    settings.buttons.createButton.addEventListener("click", function () {
       create();
    });
  }

  function update () {
  }

  function create () {
    var xhttp = new XMLHttpRequest();
    //TODO: make async true
    xhttp.open("GET", "create/", false);
    xhttp.send();
    response = xhttp.responseText;
    settings.createModalBody.innerHTML = response;
    
    $("#gameModal").modal();
  }

  return {
    init: function () {
      //window.setInterval(update, 1000);
      bindUIActions ();
    }
  }
})();

(function() {
  Waiting.init();
})();
