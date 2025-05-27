$(document).ready(function () {
  //Display hood
  eel.expose(ShowHood);
  function ShowHood() {
    $("#Oval").attr("hidden", false);
    $("SiriWave").attr("hidden", true);
  }
});
