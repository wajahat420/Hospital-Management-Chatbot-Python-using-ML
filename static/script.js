var messages = [];

function  myFunction() {
  var text = $("#text").val();
  messages.push(text);
  document.getElementById("text").value = "";
  $.ajax({
  url: "/send_and_receive",
  type: "POST",
  data: { text: text }
  }).done((res) => {
  messages.push(res);
  for (i = messages.length - 2; i < messages.length; i++) {
    if (i % 2 == 1) {
    var html = "<div class='left'>	<div>"  + messages[i] + " </div>	</div>";
    } else {
    var html = "<div class='right'>	<div> " + messages[i] + " </div>	</div>";
    }
  $(".message").append(html);
  }
  });
  }


