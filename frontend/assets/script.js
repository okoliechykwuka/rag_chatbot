const chatInput = document.querySelector(".chat-input textarea");
const sendBtn = document.querySelector(".chat-input span");
const fileUpload = document.querySelector("#file-upload");
const chatBox = document.querySelector(".chatbox");
const chatBotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const maximiseBtn = document.querySelector(".maximise-btn");
const minimiseBtn = document.querySelector(".minimise-btn");

let message;

const createChatElement = (message, className) => {
    const chat = document.createElement("li");
    chat.classList.add("chat", className);
    
    let chatContent;
    if (className === "outgoing") {
        chatContent = `<p>${message}</p>`;
    } else {
        chatContent = `<span class="material-symbols-outlined">smart_toy</span>
                       <p>${message}</p>`;
    }

    chat.innerHTML = chatContent;
    return chat;
}

const handleChat = async () => {
    message = chatInput.value.trim();
    if (!message) return;

    const chatLi = createChatElement(message, "outgoing");
    chatBox.appendChild(chatLi);
    chatBox.scrollTo(0, chatBox.scrollHeight);

    chatInput.value = "";

    const think = createChatElement("Thinking....", "incoming");
    chatBox.appendChild(think);
    chatBox.scrollTo(0, chatBox.scrollHeight);

    try {
        const response = await fetch('http://127.0.0.1:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        const botResponse = createChatElement(data.response, "incoming");
        chatBox.removeChild(think);
        chatBox.appendChild(botResponse);
        chatBox.scrollTo(0, chatBox.scrollHeight);
    } catch (error) {
        console.error('Error:', error);
        chatBox.removeChild(think);
        const errorResponse = createChatElement('Sorry, something went wrong.', "incoming");
        chatBox.appendChild(errorResponse);
        chatBox.scrollTo(0, chatBox.scrollHeight);
    }
};
const handleFileUpload = async () => {
    const file = fileUpload.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
        const loadingIcon = document.createElement('span');
        loadingIcon.classList.add('material-symbols-outlined', 'loading-icon');
        loadingIcon.textContent = 'hourglass_top';
        document.body.appendChild(loadingIcon);

        const response = await fetch('http://127.0.0.1:8000/upload', {
            method: 'POST',
            body: formData
        });

        document.body.removeChild(loadingIcon);

        if (response.ok) {
            const result = await response.json();
            const fileLi = createChatElement(`File uploaded: ${file.name}`, "outgoing");
            chatBox.appendChild(fileLi);
            chatBox.scrollTo(0, chatBox.scrollHeight);
        } else {
            const errorLi = createChatElement('Error uploading file.', "incoming");
            chatBox.appendChild(errorLi);
            chatBox.scrollTo(0, chatBox.scrollHeight);
        }
    } catch (error) {
        console.error('Error:', error);
        const errorLi = createChatElement('Error uploading file.', "incoming");
        chatBox.appendChild(errorLi);
        chatBox.scrollTo(0, chatBox.scrollHeight);
    }
}

chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        handleChat();
    }
});


sendBtn.addEventListener("click", handleChat);

fileUpload.addEventListener("change", handleFileUpload);

chatBotToggler.addEventListener("click", () => {
    document.body.classList.toggle("show-chatbot");  // Toggle instead of add
});

closeBtn.addEventListener("click", () => {
    document.body.classList.remove("show-chatbot");
});

maximiseBtn.addEventListener("click", () => {
    document.body.classList.add("fullscreen");
    maximiseBtn.style.opacity = "0";
    minimiseBtn.style.opacity = "1";
});

minimiseBtn.addEventListener("click", () => {
    document.body.classList.remove("fullscreen");
    minimiseBtn.style.opacity = "0";
    maximiseBtn.style.opacity = "1";
});
