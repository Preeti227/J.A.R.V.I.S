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

  // Siri message animation
  $(".siri-message").textillate({
    loop: true,
    sync: true,
    in: {
      effect: "fadeInUp",
      sync: true,
    },
    out: {
      effect: "fadeOutUp",
      sync: true,
    },
  });
  //EXit button
  $(document).on("click", "#ExitBtn", function () {
    console.log("❌ Exit button clicked");
    try {
      eel.cancelExecution(); // No double parens
    } catch (e) {
      console.error("eel.cancelExecution() error:", e);
    }
    $("#SiriWave").attr("hidden", true);
    $("#Oval").attr("hidden", false);
  });
  // Mic button click event
  $("#MicBtn").click(function () {
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
    eel.allCommands(); // This will call takecommand() in Python
  });

  function doc_keyUp(e) {
    // this would test for whichever key is 40 (down arrow) and the ctrl key at the same time

    if (e.key === "j" && e.metaKey) {
      //eel.playAssistantSound();
      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      eel.allCommands()();
    }
  }
  document.addEventListener("keyup", doc_keyUp, false);

  function PlayAssistant(message) {
    if (message != "") {
      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      eel.allCommands(message);
      $("#chatbox").val("");
      $("#MicBtn").attr("hidden", false);
      $("#SendBtn").attr("hidden", true);
    }
  }
  //toggle function for hiding and displaying mic & send button
  function ShowHideButton(message) {
    if (message.length == 0) {
      $("#MicBtn").attr("hidden", false);
      $("#SendBtn").attr("hidden", true);
    } else {
      $("#MicBtn").attr("hidden", true);
      $("#SendBtn").attr("hidden", false);
    }
  }
  // key up event handler on text box
  $("#chatbox").keyup(function () {
    let message = $("#chatbox").val();
    ShowHideButton(message);
  });

  // send button event handler
  $("#SendBtn").click(function () {
    let message = $("#chatbox").val();
    PlayAssistant(message);
  });

  //Enter key event handler
  $("#chatbox").keypress(function (e) {
    key = e.which;
    if (key == 13) {
      let message = $("#chatbox").val();
      PlayAssistant(message);
    }
  });
});
