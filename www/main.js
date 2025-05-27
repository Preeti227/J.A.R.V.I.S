$(document).ready(function () {
  $(".text").textillate({
    loop: true,
    sync: true,

    in: {
      effect: "bounceIn",
    },
    out: {
      effect: "bounceOut",
    },
  });
  //Siri configuration
  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 200,
    style: "ios9",
    amplitude: "1",
    speed: "0.30",
    autostart: true,
  });
  //mic button
  $("#MicBtn").click(function () {
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
  });
});
