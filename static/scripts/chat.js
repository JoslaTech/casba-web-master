// Build send message with HTML
function buildMessageSend(text) {
  var element = document.createElement('div');

  element.classList.add('message', 'sent');

  element.innerHTML = text +
  '<span class="metadata">' +
  '<span class="time">' + moment().format('h:mm A') + '</span>'
  '</span>';

  return element;
}

// Build receive message with HTML
function buildMessageRecieve(text) {
  var element = document.createElement('div');

  element.classList.add('message', 'received');

  element.innerHTML = text +
  '<span class="metadata">' +
  '<span class="time">' + moment().format('h:mm A') + '</span>'
  '</span>';

  return element;
}

// Build hello message attachment
function buildCapabilitiesAttachment() {
  var element = document.createElement('div');

  element.classList.add('message', 'attachment');

  element.innerHTML = '<div class="capabilities-attachment">' +
    '<a type="submit" class="btn btn-primary btn-lg btn-md btn-sm btn-xs attachment"><span class="glyphicon glyphicon-user"></span>    Fund Transfer</a>' +
    '<a type="submit" class="btn btn-primary btn-lg btn-md btn-sm btn-xs attachment"><span class="glyphicon glyphicon-user"></span>    Airtime Topup</a>' +
    '<a type="submit" class="btn btn-primary btn-lg btn-md btn-sm btn-xs attachment"><span class="glyphicon glyphicon-user"></span>   Pay Bills</a>' +
  '</div>';

  return element;
}

// Build account message attachment
function buildAccountTypeAttachment() {
  var element = document.createElement('div');

  element.classList.add('message', 'attachment');

  element.innerHTML = '<div class="accountType-attachment">' +
    '<a type="submit" class="btn btn-primary btn-lg btn-md btn-sm btn-xs attachment savingsAccount"><span class="glyphicon glyphicon-user"></span>    Savings</a>' +
    '<a type="submit" class="btn btn-primary btn-lg btn-md btn-sm btn-xs attachment"><span class="glyphicon glyphicon-user"></span>    Current</a>' +
  '</div>';

  return element;
}

// Build beneficiary message attachment
function buildAccountDestinationAttachment() {
  var element = document.createElement('div');

  element.classList.add('message', 'attachment');

  element.innerHTML = '<div class="accountType-attachment">' +
    '<a type="submit" class="btn btn-primary btn-lg btn-md btn-sm btn-xs attachment kenneth"><span class="glyphicon glyphicon-user"></span>    Kenneth</a>' +
    '<a type="submit" class="btn btn-primary btn-lg btn-md btn-sm btn-xs attachment"><span class="glyphicon glyphicon-user"></span>    Micheal</a>' +
  '</div>';

  return element;
}


// JQUERY Begins Here....
$(document).ready(function(){

  var conversation = document.querySelector('#conversations');
  var inputChat = document.querySelector('#inputChat');

  // Initialise websocket
  var socket = io.connect('http://' + document.domain + ':' + location.port);

  socket.on('connect', function() {
		console.log('User has connected!');
	});

  // Initialise watson conversation
  var text = "Hello"

  socket.emit('my event', {data: text});

  // ChatBot response message
  socket.on('my response', function(msg) {
    var text = msg.data;
    var user = msg.user;
    var intent = msg.intent;
    var entity = msg.entity;
    var entity_value = msg.entity_value;

    //Preprocessing
    text = text.replace('userName', (user.fName.charAt(0).toUpperCase() + user.fName.slice(1)).bold());

    if (intent != "....") {
      if (intent == "hello") {
        if (entity == "account") {
          var message = buildMessageRecieve(text);
          conversation.appendChild(message);
          var attachment = buildAccountDestinationAttachment();
          conversation.appendChild(attachment);
        } else if (entity == "bank") {
          var message = buildMessageRecieve(text);
          conversation.appendChild(message);
        } else if (entity == "sys-number") {
          var message = buildMessageRecieve(text);
          conversation.appendChild(message);
        } else {
          var message = buildMessageRecieve(text);
          conversation.appendChild(message);
          var attachment = buildCapabilitiesAttachment();
          conversation.appendChild(attachment);
        }
      } else if (intent == "capabilities") {
        var message = buildMessageRecieve(text);
        conversation.appendChild(message);
        var attachment = buildCapabilitiesAttachment();
        conversation.appendChild(attachment);
      } else if (intent == "fund_transfer") {
        var message = buildMessageRecieve(text);
        conversation.appendChild(message);
        var attachment = buildAccountTypeAttachment();
        conversation.appendChild(attachment);
      } else {
        var message = buildMessageRecieve(text);
        conversation.appendChild(message);
      }
    } else {
      var message = buildMessageRecieve(text);
      conversation.appendChild(message);
    }

    conversation.scrollTop = conversation.scrollHeight;

		console.log('Received message');
	});

  // Button Functions
  $('.conversations').on('click', '.savingsAccount', function() {
    $(this).closest('.message').fadeOut();
    var text = "Savings"

    var message = buildMessageSend(text);
    conversation.appendChild(message);

    conversation.scrollTop = conversation.scrollHeight;

    socket.emit('my event', {data: text});
  });

  // Button Functions
  $('.conversations').on('click', '.kenneth', function() {
    $(this).closest('.message').fadeOut();
    var text = "Kenneth"

    var message = buildMessageSend(text);
    conversation.appendChild(message);

    conversation.scrollTop = conversation.scrollHeight;

    socket.emit('my event', {data: "GTB"});
  });

  // User click to send input
  $("#send").on("click", function(e){
    var text = inputChat.value;
    if (inputChat.value) {
      var message = buildMessageSend(text);
      conversation.appendChild(message);
    }

    socket.emit('my event', {data: text});

    inputChat.value = '';
    conversation.scrollTop = conversation.scrollHeight;

    e.preventDefault();
  });

  //User press enter to send input
  $('#inputChat').keypress(function (e) {
    var key = e.which;
    var text = inputChat.value;

    if(key == 13)  // the enter key code
    {
      if (inputChat.value) {
        var message = buildMessageSend(text);
        conversation.appendChild(message);
      }

      //socket.send(text);
      socket.emit('my event', {data: text});

      inputChat.value = '';
      conversation.scrollTop = conversation.scrollHeight;

      e.preventDefault();
    }
  });

});
