const apiUrl = "http://127.0.0.1:8000/chat";

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("message-input");
    input.addEventListener("keydown", async (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            await sendMessage();
        }
    });
});

async function sendMessage() {
    const input = document.getElementById("message-input");
    const message = input.value.trim();
    if (!message) return;

    addMessage("user", message);

    const payload = {
        conversation_id: "12095f44cb8411ef9643e658ca77ea8e",
        messages: [{ role: "user", content: message }],
        quote: true,
    };

    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
        const message_list = data.reply.split('\n\n');
        const chunk = message_list[message_list.length - 2];
        const par = chunk.split('data:');
        const temp = JSON.parse(par[1]);
        const msg = temp.data.answer;
        addMessage("chatbot", msg);
    } catch (error) {
        addMessage("chatbot", `Error: ${error.message}`);
    }

    input.value = "";
}

function addMessage(role, content) {
    const messagesDiv = document.getElementById("messages");
    const messageDiv = document.createElement("div");
    messageDiv.className = `${role}`;
    messageDiv.innerHTML = `<span class="${role}">${role}:</span> <span class="${role}">${content}</span>`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
