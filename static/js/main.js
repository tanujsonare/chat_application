const chatElement = document.querySelector("#chat");
const chatOpen = document.querySelector("#chat_open");
const joinChat = document.querySelector("#join_chat");
const chatWelcome = document.querySelector("#chat_welcome");
const chatIcon = document.querySelector("#chat_icon");

chatOpen.onclick = function(e){
    e.preventDefault();
    chatIcon.classList.add("hidden");
    chatWelcome.classList.remove('hidden');
}