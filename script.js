const apiURL = "https://oda-ai.onrender.com/api/chat"; // Replace with your Python API URL

function addMessage(sender, text) {
  const box = document.getElementById("chat-box");
  const message = document.createElement("p");
  message.innerHTML = `<strong>${sender}:</strong> ${text}`;
  box.appendChild(message);
  box.scrollTop = box.scrollHeight;
}

function sendMessage() {
  const input = document.getElementById("user-input");
  const text = input.value.trim();
  if (!text) return;
  addMessage("You", text);
  input.value = "";

  fetch(apiURL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: text })
  })
    .then(res => res.json())
    .then(data => {
      addMessage("Oda", data.reply || "No reply");
    })
    .catch(err => {
      addMessage("Oda", "Error reaching server.");
      console.error(err);
    });
}


function sendMessage() {
  const input = document.getElementById("user-input");
  const text = input.value.trim();
  if (!text) return;
  addMessage("You", text);
  input.value = "";

  // Show thinking animation
  document.getElementById("thinking").style.display = "block";

  fetch(apiURL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  })
    .then(res => res.json())
    .then(data => {
      // Hide animation
      document.getElementById("thinking").style.display = "none";
      addMessage("Bot", data.reply || "No reply");
    })
    .catch(err => {
      document.getElementById("thinking").style.display = "none";
      addMessage("Bot", "Error reaching server.");
      console.error(err);
    });
}
