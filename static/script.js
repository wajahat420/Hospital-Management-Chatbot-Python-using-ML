function showDetails(itemID){
  ids = ["h4-1","h4-2","h4-3","h4-4","h4-5","h4-6","h4-7"]
  id = document.getElementById(itemID)

  // console.log("id",itemID)
    if (id.className == ""){
        id.className  = "d-none"
    }else{
      id.className  = ""
      for(i=0;i<ids.length;i++){
        otherId = document.getElementById(ids[i])
        if(itemID != ids[i]){
            // console.log("ids[i]",ids[i])
            otherId.className  = "d-none"
          }
      }
    }


  
}
var messages = [];

function  myFunction() {

  var text = $("#text").val();
  messages.push(text);
  document.getElementById("text").value = "";
  id = document.getElementById("message")
  // console.log("text",text)
  if (text == ""){
    return
  }
  // Speak Question
  $.ajax({
    url: "/textTospeech",
    type: "POST",
    data: { text: text }
    }).done((res) => {
        messages.push(res);
        // var html = "<div class='right'>	<div>"  + messages[messages.length - 1] + " </div>	</div>";
        // $(".message").append(html);
        id.scrollTop = id.scrollHeight ;

        for (i = messages.length - 2; i < messages.length; i++) {
            if (i % 2 == 1) {
              var html = "<div class='left'>	<div>"  + messages[i] + " </div>	</div>";
            } else {
              var html = "<div class='right'>	<div> " + messages[i] + " </div>	</div>";
            }
            $(".message").append(html);
            id.scrollTop = id.scrollHeight ;
        }
    });
  // Speak answer 
    $.ajax({
      url: "/speak",
      type: "GET",
    })
}

function voiceRecord() {
  console.log("working...........")
  id = document.getElementById("message")

  $.ajax({
      url: "/speechToText",
      type: "GET",
  }).done((res) => {
  
    console.log("before")
      messages.push(res.ques);
      messages.push(res.ans);
      console.log("after")

      var html1 = "<div class='right'>	<div>" + res.ques + " </div>	</div>";
      $(".message").append(html1);
      

      id.scrollTop = id.scrollHeight;

  });
  $.ajax({
      url: "/speak",
      type: "GET",
  }).done(() => {

    var html2 = "<div class='left'>	<div> " + messages[messages.length - 1] + " </div>	</div>";
    $(".message").append(html2);

    id.scrollTop = id.scrollHeight;
    // console.log("message", messages)

});


}




