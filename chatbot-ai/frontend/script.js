const chatBox = document.getElementById('chat-box');

function appendMessage(sender, text) {
    const message = document.createElement('div');
    message.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const question = input.value;
    appendMessage("You", question);
    input.value = "";

    const res = await fetch("https://your-backend-url.onrender.com/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
    });

    const data = await res.json();
    appendMessage("Bot", data.answer);
}
