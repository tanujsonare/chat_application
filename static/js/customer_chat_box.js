var chatWebSocket;
const chatRoomUuid = localStorage.getItem("chatroomuuid");
const chatName = localStorage.getItem("chatName");
const chatText = document.querySelector("#message_content");
const sendMessageButton = document.querySelector("#send_message");
const messageBox = document.querySelector("#message_box");

$(document).ready(function () {
    if (chatRoomUuid){
        chatWebSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`)
        chatWebSocket.onopen = function(e){
            console.log("chat socket open");
        }
        chatWebSocket.onclose = function(e){
            console.log("chat socket close");
        }
        if(chatWebSocket){
            chatWebSocket.onmessage = function(e){
                console.log("On message calls");
                onNewMessage(JSON.parse(e.data));
            };
        }
    }
})

function sendMesage(){
    if (chatWebSocket){
        chatWebSocket.send(JSON.stringify({
            "type": "message",
            "name": chatName,
            "message": chatText.value,
            "agent": "",
        }))
        chatText.value = "";
        messageBox.scrollTo(0, messageBox.scrollHeight);
    }
}

function onNewMessage(data){
   if(data.type == "chat_message" && data.message){
        messageBox.innerHTML += `
        <div class="flex w-full max-w-md mt-2 space-x-3g">
            <div
                class="flex-shrink-0 h-10 w-10 rounded-full bg-indigo-500 text-center text-white mx-3 my-2 pt-2">
                ${data.initials}
            </div>
            <div class="my-1">
                <div class="p-3 rounded-xl bg-white">
                    ${data.message}
                </div>
                <span class="text-xs text-gray-800 leading-none">${data.created_at} ago</span>
            </div>
        </div>
        `
        messageBox.scrollTo(0, messageBox.scrollHeight);
   }
}

sendMessageButton.addEventListener("click", function(e){
    sendMesage();
});