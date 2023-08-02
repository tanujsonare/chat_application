const chatElement = document.querySelector("#chat");
const chatOpen = document.querySelector("#chat_open");
const joinChat = document.querySelector("#join_chat");
const chatWelcome = document.querySelector("#chat_welcome");
const chatIcon = document.querySelector("#chat_icon");

chatOpen.onclick = function(e){
    chatIcon.classList.add("hidden");
    chatWelcome.classList.remove('hidden');
    e.stopPropagation();   // Prevent click event from propagating to the body
}

document.addEventListener('click', function(event) {
    if (!chatWelcome.classList.contains("hidden")){
        if (!chatWelcome.contains(event.target)) {
            chatIcon.classList.remove("hidden");
            chatWelcome.classList.add('hidden');
        }
    }
});