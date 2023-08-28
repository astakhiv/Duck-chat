const socket = new WebSocket("ws://" + window.location.host + "/");

socket.onopen = function(event) {
  console.log("WebSocket connection opened");
};

socket.onmessage = function(event) {
  const invis = document.getElementById("no_messages")
  console.log(invis);
  if (invis){
    invis.remove();
  }
  data = JSON.parse(event.data);
  console.log("Received message:", data);
  document.querySelector("#messages_block").innerHTML = `
  <div>
    <h4>${data.username}</h4>
    <p>${data.message}</p>
  </div>` + document.querySelector("#messages_block").innerHTML;
};

socket.onclose = function(event) {
  console.log("WebSocket connection closed");
};

document.addEventListener("DOMContentLoaded", () => { 
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