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
    currGamesBody: document.getElementById("currGamesBody"),
    currGamesRow: null,
    pendGamesBody: document.getElementById("pendGamesBody"),
    pendGamesRow: null,
  }

  function bindUIActions () {
    settings.buttons.joinButton.addEventListener("click", function () {
      if (settings.pendGamesRow != null) {
        var key = settings.pendGamesBody.rows[settings.pendGamesRow].dataset.value;
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", window.location.pathname+key+"/join/", false);
        xhttp.send();
        //refresh
        window.location.pathname = window.location.pathname;
      }
    });
    settings.buttons.playButton.addEventListener("click", function () {
      if (settings.currGamesRow != null) {
        var key = settings.currGamesBody.rows[settings.currGamesRow].dataset.value;
        window.location.pathname = "/game/play/"+key+"/";
      }
    });
    settings.buttons.createButton.addEventListener("click", function () {
       create();
    });

    var i;
    var rows = settings.currGamesBody.rows;
    for (i = 0; i < rows.length; i += 1) {
      (function (rowIndex) {
        settings.currGamesBody.rows[rowIndex].addEventListener("click", function () {
          if (settings.currGamesRow != null) {
            settings.currGamesBody.rows[settings.currGamesRow].className = "";
          }
          settings.currGamesBody.rows[rowIndex].className = "active";
          settings.currGamesRow = rowIndex;
        });
      })(i);
    }

    rows = settings.pendGamesBody.rows;
    for (i = 0; i < rows.length; i += 1) {
      (function (rowIndex) {
        settings.pendGamesBody.rows[rowIndex].addEventListener("click", function () {
          if (settings.pendGamesRow != null) {
            settings.pendGamesBody.rows[settings.pendGamesRow].className = "";
          }
          settings.pendGamesBody.rows[rowIndex].className = "active";
          settings.pendGamesRow = rowIndex;
        });
      })(i);
    }
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
