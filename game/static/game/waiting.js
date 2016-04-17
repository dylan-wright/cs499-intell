
var Waiting = (function () {
  var settings = {
    games: [],
    timers: [],
    buttons: {
      joinButton: document.getElementById("joinBtn"),
      playButton: document.getElementById("playBtn"),
    },
  }

  function bindUIActions () {
    settings.buttons.joinButton.addEventListener("click", function () {

    });
    settings.buttons.playButton.addEventListener("click", function () {

    });
  }

  function update () {
  }

  return {
    init: function () {
      //window.setInterval(update, 1000);
    }
  }
})();

(function() {
  Waiting.init();
})();
