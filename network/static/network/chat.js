let socket = null;

document.addEventListener("DOMContentLoaded", () => { 
  const users = [
    document.querySelector("#sumbit").name,
    document.querySelector("#to").innerHTML
  ];
  users.sort();
  
  const roomname = `${users[0]}_${users[1]}`;

  socket = new WebSocket(
    "ws://" 
    + window.location.host 
    + "/ws/chat/"
    + roomname
    + '/');
  
  socket.onopen = function(event) {
    console.log(`WebSocket connection opened on: ${roomname}`);
  };
  
  socket.onmessage = function(event) {
    const invis = document.getElementById("no_messages")
    if (invis){
      invis.remove();
    }

    data = JSON.parse(event.data);
    console.log(data);
    document.querySelector("#messages_block").innerHTML = `
    <div>
      <h4>${data.sender}</h4>
      <p>${data.message}</p>
    </div>` 
    + document.querySelector("#messages_block").innerHTML;
  };
  
  socket.onclose = function(event) {
    console.log("WebSocket connection closed");
  };
  const form = document.getElementById("form");
  form.addEventListener('submit', (event) => {
    event.preventDefault();
  });
  form.addEventListener('submit', send);
});

function send() {
  const btn = document.querySelector("#sumbit");
  let message = document.getElementById("message");
  socket.send(JSON.stringify({
    "message": message.value,
    "from": btn.name,
    "to": document.querySelector("#to").innerHTML,
  }));
  message.value = "";
}